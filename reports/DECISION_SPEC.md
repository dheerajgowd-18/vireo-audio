# Engineering Decision Specification: Vireo Audio Support Analytics Engine

**Document Version:** 1.0.0  
**Effective Date:** 2026-09-30  
**Status:** Approved Technical Architecture  

---

## Overview

This specification formalizes the foundational data modeling, business logic, and architectural decisions governing the deterministic analytics engine for Vireo Audio's customer support performance evaluation. Every decision is grounded in empirical evidence extracted during the dataset audit, aligns strictly with operating policy (`support-policy.pdf` v3.2), and respects engineering resource constraints (~5-hour build cap, zero external API costs).

---

## Formal Decision Matrix

### Decision 1: Raw Data Preservation
* **Decision**: All source CSV files (`tickets.csv`, `agents.csv`, `customers.csv`, `orders.csv`, `products.csv`) are treated as strictly immutable read-only records. No source files are modified, rewritten, or deleted. All adjustments, data normalizations, and calculations are computed exclusively as derived fields in memory.
* **Evidence**: Source datasets contain legacy migration artifacts (e.g. UTC event log reconstruction in `legacy_fd`) and phone-system transcription dropouts. Silently altering or rewriting source files destroys auditability and prevents data provenance tracking.
* **Engineering Implication**: Data loaders in `src/data_loader.py` ingest raw strings and timestamps, preserving original columns (e.g., `resolved_at`, `customer_message`), and attach explicit derived columns (e.g., `resolved_at_reporting`, `handle_time_hours`).
* **Limitation**: In-memory representations require slightly more memory (~10–15 MB), which is negligible for 11,750 ticket rows.

---

### Decision 2: Agent Identification Key (`agent_id` Only)
* **Decision**: All joins, groupings, and aggregations referencing agents must key strictly on `agent_id`. Joining on `name` or using display names as unique identifiers is explicitly prohibited.
* **Evidence**: In `agents.csv`, two distinct agents share the exact display name **"Kavya Pandey"**:
  - `A3006`: Kavya Pandey (Tier 1 Chat Frontline, Indore site, Morning shift)
  - `A3029`: Kavya Pandey (Tier 1 Logistics, Bengaluru site, Morning shift)  
  Sameer Qureshi (IT Admin) documented that joining on name had previously corrupted internal reporting.
* **Engineering Implication**: `src/agent_analysis.py` merges `tickets` and `agents` on `agent_id`. Automated tests (`tests/test_data_quality.py`) verify that both `A3006` and `A3029` remain separate scorecard entities with distinct ticket volumes and CSAT averages.
* **Limitation**: Display tables must include `agent_id` alongside `name` to avoid user confusion in downstream UI dashboards.

---

### Decision 3: CSAT Metric Definition (Exclusion of Blanks)
* **Decision**: CSAT averages and medians must strictly exclude unpopulated (blank/null) survey responses. Blanks must never be imputed or converted to zero.
* **Evidence**: In `tickets.csv`, only 5,196 out of 11,750 tickets have a CSAT score (44.22% response rate, matching Policy §8's benchmark of ~45%). Policy §8 explicitly commands: *"A blank score means no response and must be excluded from averages, not treated as zero."* Imputing blanks as zero artificially collapses companywide CSAT from 3.33 to 1.47.
* **Engineering Implication**: `src/metrics.py` calculates CSAT exclusively on `tickets['csat_score'].dropna()`. Blanks are tracked separately as response rate indicators.
* **Limitation**: Agents with lower response rates may have higher CSAT variance due to smaller sample sizes (`csat_n` is explicitly surfaced on all scorecards).

---

### Decision 4: Legacy Timestamp Reconciliation (`+05:30` IST Offset)
* **Decision**: For tickets originating from `source_system == 'legacy_fd'`, resolution timestamps are adjusted in derived field `resolved_at_reporting` by adding exactly 5 hours and 30 minutes (`+05:30`). Helpdesk rows remain unadjusted.
* **Evidence**: 2,309 tickets in `legacy_fd` had `resolved_at < first_response_at` with an average negative duration of -5.13 hours. Policy §9 explains that helpdesk timestamps were exported in IST, whereas legacy Freshdesk resolution timestamps were reconstructed from event logs storing UTC (UTC + 5:30 = IST). Adding 5.5 hours resolves 100% of negative durations without exception.
* **Engineering Implication**: `src/data_loader.py` derives `resolved_at_reporting` and sets `legacy_timestamp_adjusted = True`. An automated integrity assertion enforces that zero legacy tickets have negative handle time post-adjustment.
* **Limitation**: Any historical micro-delays within the Freshdesk queue cannot be retroactively reconstructed beyond the standard 5.5-hour timezone offset.

---

### Decision 5: Handle Time Scope (Attendance Tickets Only)
* **Decision**: Handle time is calculated strictly as `resolved_at_reporting - first_response_at` in hours. Completed handle-time observations are populated ONLY for tickets in attendance status (`resolved` or `closed`) where both timestamps exist. Tickets in `open` or `pending` status are assigned `NaN`.
* **Evidence**: Policy §10 defines handle time as *"first response to resolution"* and attendance as *"any ticket in status resolved or closed"*. Open and pending tickets have not reached resolution; computing duration against incomplete tickets corrupts duration distributions.
* **Engineering Implication**: `src/data_loader.py` sets `handle_time_hours = np.nan` for open/pending tickets. `src/metrics.py` computes duration statistics exclusively across completed attendance records (11,183 tickets).
* **Limitation**: Does not measure current aging duration for currently open backlogs (which requires real-time snapshot analysis).

---

### Decision 6: Operational Stratification (Separation of Tier 1 and Tier 2)
* **Decision**: No companywide combined "worst employee" ranking is generated. Tier 1 Frontline agents and Tier 2 Escalations & Warranty engineers are evaluated strictly within separate operational benchmark groups.
* **Evidence**: In a naive companywide ranking by CSAT, **all 6 Tier 2 Escalations & Warranty agents occupy positions 1 through 6 at the very bottom**, and **the four Tier 1 hardware triage agents ("Kavya's four") occupy positions 7 through 10**. Tier 2 agents handle physical hardware defects, multi-touch RMA cases, and angry customers by design. Policy §6 explicitly states: *"Tier 2 cases are multi-touch by nature and are measured on resolution in days, not on tickets closed per week. Tier 2 agents are not to be compared with Tier 1 on volume metrics."*
* **Engineering Implication**: `src/agent_analysis.py` assigns `benchmark_group` (e.g. `Tier 1 - Chat Frontline`, `Tier 2 - Escalations & Warranty`) and calculates intra-group ranks (`intra_group_csat_rank_asc`).
* **Limitation**: Requires executive stakeholders to review multiple peer-group tables rather than a simplistic single list.

---

### Decision 7: Omission of Risky Fallback Order Joins
* **Decision**: Core ticket KPIs, agent metrics, and SLA calculations do not join `orders.csv`. Order-level analyses (such as lot code tracking) are restricted strictly to tickets with directly populated `order_id` values. Fallback joining on `(customer_id, product_sku)` is omitted from core reporting.
* **Evidence**: 4,107 tickets lack an `order_id`. In `orders.csv`, exactly 1,388 `(customer_id, sku)` pairs placed multiple orders (up to 4 separate orders for the same SKU). Performing a fallback join generates a Cartesian product, creating duplicate ticket rows that artificially inflate ticket counts, handle times, and costs.
* **Engineering Implication**: `src/data_quality.py` reports the count of multi-order pairs and unlinked tickets. `src/financials.py` joins `orders.csv` only where `ticket.order_id` is populated.
* **Limitation**: Manufacturing lot codes cannot be determined for the 34.95% of tickets where the customer did not quote an order number.

---

### Decision 8: Replacement Costing Standards (Policy §5 vs Finance Estimate)
* **Decision**: Authoritative replacement spend is computed strictly using Policy §5: $\text{Unit Cost} + ₹340 \text{ Logistics}$. Finance's informal ₹2,500 rule-of-thumb is reported solely as a comparative diagnostic.
* **Evidence**: Products range in unit cost from ₹90 (USB cable) to ₹2,650 (Strata 3 headphones). Policy §5 explicitly defines replacement cost as the product's unit cost plus ₹340 for reverse pickup and forward shipping. Finance's flat ₹2,500 figure overstates Vireo's actual replacement spend by ₹13,24,010 (+38.76%).
* **Engineering Implication**: `src/financials.py` joins `products.csv` on `product_sku == sku`, computes exact policy replacement costs, and quantifies the Finance overstatement.
* **Limitation**: Assumes ₹340 logistics cost is constant across pan-India delivery zones as prescribed by policy planning guidelines.

---

### Decision 9: First-Response SLA Evaluation (Missing Responses Tracked Separately)
* **Decision**: Tickets lacking a human response (`first_response_at` is null) are classified as `missing_first_response = True` and are NOT automatically counted as SLA breaches. SLA breaches are evaluated only where human response timestamps exist.
* **Evidence**: An unresponded ticket indicates an abandoned or in-flight interaction. Marking missing timestamps as instantaneous breaches distorts channel breach rate percentages.
* **Engineering Implication**: `src/data_loader.py` computes `sla_breach = True` only when `first_response_minutes > sla_target_minutes`. `src/metrics.py` reports total eligible tickets and missing responses as distinct metrics.
* **Limitation**: Open tickets that are currently older than the SLA threshold must be monitored in real-time queue monitors rather than historical resolution logs.

---

### Decision 10: Non-Punitive Reporting of Dual Refund/Replacement Anomaly
* **Decision**: Instances where both a refund and a replacement were issued for the same order or ticket are classified neutrally as *"policy compliance exceptions requiring review"*, rather than labeled as fraud.
* **Evidence**: Exactly 6 tickets have both a replacement flag and a refund amount on the same ticket, and 131 orders received both across separate tickets. While Policy §5 forbids dual benefits, observational data alone cannot distinguish between customer deceit, agent error, or authorized customer service exceptions.
* **Engineering Implication**: `src/data_quality.py` isolates affected `ticket_id` and `order_id` records into an audit dictionary for operational review.
* **Limitation**: Final financial write-offs require manual investigation by Team Leads and Finance.

---

### Decision 11: Avoidance of Unfounded Causal Claims
* **Decision**: Observational correlations (e.g., replacement surge coinciding with Pulse 2 manufacturing lots `PL2-2510/11/12`) are reported as *"high-replacement lot candidates"* and *"strong statistical associations"*, rather than definitive engineering causes.
* **Evidence**: The correlation between Pulse 2 lots and replacement frequency is overwhelming (32%–45% replacement rate vs 3% baseline), and customer text frequently mentions left earbud charging failures. However, without physical hardware laboratory tear-downs or supplier quality audit reports, software analytics cannot prove metallurgical or electronic causality.
* **Engineering Implication**: Reports and data models maintain neutral, defensible language.
* **Limitation**: Management must conduct physical warehouse batch testing before filing formal commercial warranty recovery claims against contract manufacturers.
