# Final Business Case: Tier 1 Handle Time Optimization

**Target Investment**: ₹4,00,000 Q3 Support Training Budget  
**Evaluation Scope**: 11,750 Support Tickets, 44 Agents, 18 Months (Jan 2024 – Jun 2025)  
**Author**: Lead Data & AI Engineer  
**Status**: Formally Approved & Defended  

---

## 1. Primary Business Goal Statement

The primary business goal for Vireo Audio's Q3 support training initiative is formally defined as:

> ### Primary Operational Goal:
> **"Reduce Tier 1 frontline above-median handle time across Chat (from 4.38h to 3.81h) and Email (from 6.70h to 7.07h peer median), eliminating 650.8 excess agent-hours per quarter, representing approximately ₹1,07,379 per quarter in recoverable support capacity."**

> ### Full Tier 1 Program Goal (Aligning with ₹4.0 Lakh Budget):
> **"Reduce Tier 1 handle time across above-p25 agents toward the 25th percentile peer efficiency benchmark, eliminating 2,262.2 excess agent-hours per quarter, representing approximately ₹3,73,266 per quarter (~₹3.73 Lakhs/quarter) in ongoing operational labor capacity."**

---

## 2. One-Paragraph Executive Briefing for Priya (Customer Support Lead)

> "Priya, our quantitative audit shows that targeting the ₹4,00,000 training budget at the raw 'Bottom 10' list would be fundamentally misguided, as 6 of those 10 are Tier 2 specialists handling complex escalations and 4 are specialized hardware triage agents. Furthermore, the ₹22.39L spent replacing Pulse 2 earbuds is driven by factory charging pin corrosion in lot `PL2-2510-3`—a hardware defect that support training cannot solve. Instead, the highest-return investment of your ₹4.0L budget is peer-benchmarked workflow and troubleshooting coaching for your 22 frontline Chat and Email agents. Currently, above-median agents spend 650.8 excess hours per quarter navigating repetitive tickets. By bringing these agents to their own team medians through standard diagnostic macros and escalation coaching, we recover **₹1,07,379 per quarter** in frontline capacity immediately, scaling to **₹3,73,266 per quarter** as agents reach top-quartile efficiency—fully recouping the ₹4.0L investment within four quarters while maintaining our CSAT floor above 3.33."

---

## 3. Mathematical & Data Derivation

### 3.1 Dataset Parameters
- **Audit Duration**: 18 months / 6 calendar quarters (January 2024 to June 2025).
- **Total Support Tickets**: 11,750 tickets.
- **Support Staff**: 44 agents total (38 Tier 1 agents, 6 Tier 2 agents).
- **Target Frontline Cohort**: 22 Tier 1 Frontline agents (15 Chat agents, 7 Email agents).

### 3.2 Chat Frontline Derivation (15 Agents)
- **Ticket Volume**: 2,752 tickets handled.
- **Logged Handle Time**: 12,060.0 hours.
- **Cohort Mean Handle Time**: 4.38 hours per ticket.
- **Team Median of Agent Means**: 3.81 hours per ticket.
- **Excess Agent-Hours Above Median**: 2,836.0 hours over 18 months.
- **Quarterly Run-Rate**: $2,836.0 \text{ hours} \div 6 \text{ quarters} = \mathbf{472.7 \text{ hours/quarter}}$.
- **Financial Conversion** (Policy §8 Chat rate of ₹165/hour):
  $$\text{Quarterly Savings} = 472.7 \text{ hrs} \times ₹165/\text{hr} = \mathbf{₹77,990.25 \text{ per quarter}}$$

### 3.3 Email Frontline Derivation (7 Agents)
- **Ticket Volume**: 1,327 tickets handled.
- **Logged Handle Time**: 8,885.5 hours.
- **Cohort Mean Handle Time**: 6.70 hours per ticket.
- **Team Median of Agent Means**: 7.07 hours per ticket.
- **Excess Agent-Hours Above Median**: 1,068.7 hours over 18 months.
- **Quarterly Run-Rate**: $1,068.7 \text{ hours} \div 6 \text{ quarters} = \mathbf{178.1 \text{ hours/quarter}}$.
- **Financial Conversion** (Policy §8 baseline rate of ₹165/hour):
  $$\text{Quarterly Savings} = 178.1 \text{ hrs} \times ₹165/\text{hr} = \mathbf{₹29,389.33 \text{ per quarter}}$$
  *(Note: At the channel-specific Email rate of ₹195/hr, recovery increases to ₹34,732.83/quarter).*

### 3.4 Combined Frontline Capacity Recovery
- **Total Excess Hours**: $472.7 + 178.1 = \mathbf{650.8 \text{ agent-hours per quarter}}$.
- **Direct Financial Recovery**: $₹77,990 + ₹29,389 = \mathbf{₹1,07,379.58 \text{ per quarter (~₹1.07L/quarter)}}$.
- **Annualized Value**: **₹4,29,518 per year**, achieving a 107.4% annual ROI on the ₹4.0L budget.

### 3.5 Full Tier 1 Population Benchmarking (38 Agents)
When training is extended across all 38 Tier 1 agents:
- **Median Benchmark**: 5,565.1 excess hours over 18 months = 927.5 hours/quarter $\times$ ₹165/hr = **₹1,53,040 per quarter (~₹1.53L/quarter)**.
- **25th Percentile Benchmark (Upper-Quartile Target)**:
  - 13,573.3 excess hours across Tier 1 over 18 months.
  - Quarterly Run-Rate: $13,573.3 \div 6 = \mathbf{2,262.2 \text{ hours/quarter}}$.
  - Financial Conversion: $2,262.2 \times ₹165/\text{hr} = \mathbf{₹3,73,266 \text{ per quarter (~₹3.73L/quarter)}}$.
  - **Capital Alignment**: Recovers 93.3% of the entire ₹4,00,000 budget in a single quarter, or **₹14,93,064 per year** in ongoing operational productivity.

---

## 4. Operational Implementation of the ₹4,00,000 Training Budget

To achieve these specific efficiencies, the ₹4,00,000 training budget should be allocated across three targeted modules designed to eliminate frontline friction:

```
+-----------------------------------------------------------------------------------+
|               ₹4,00,000 Q3 TRAINING BUDGET ALLOCATION ROADMAP                     |
+-----------------------------------------------------------------------------------+
| Module 1: Diagnostic SOPs & Note Standardization               | ₹1,75,000 (43.75%)|
| Module 2: Escalation Protocol & Transfer Reduction             | ₹1,25,000 (31.25%)|
| Module 3: Knowledge Base Tooling & Macro Navigation            | ₹1,00,000 (25.00%)|
+-----------------------------------------------------------------------------------+
```

### Module 1: Diagnostic SOPs & Note Hygiene (₹1,75,000)
- **Problem**: 31.4% of tickets currently contain uninformative agent notes ("resolved", "customer called", "done"), preventing peer context and extending subsequent handle times.
- **Intervention**: Structured note-taking templates and standardized diagnostic checklists for common Bluetooth pairing and battery complaints.
- **Target Impact**: Eliminate redundant discovery questioning, driving Chat handle time toward 3.81h.

### Module 2: Escalation Protocols & FCR Optimization (₹1,25,000)
- **Problem**: 1,215 tickets were transferred between tiers (incurring ₹305/transfer), while 3,277 tickets represented 30-day repeat contacts (costing ₹9,03,890 in labor).
- **Intervention**: Frontline empowerment to resolve common configuration tickets on the first contact without escalating to Tier 2.
- **Target Impact**: Reduce avoidable transfers by 20%, saving an additional ~₹12,350/quarter, and reduce repeat contacts by 15%, saving ~₹22,600/quarter in labor.

### Module 3: Tooling & Macro Navigation (₹1,00,000)
- **Problem**: Inconsistent adoption of standard response macros across shift rotations and sites.
- **Intervention**: Practical simulator coaching on CRM navigation, macro auto-completes, and quick-tagging.
- **Target Impact**: Compress first-response latency and prevent SLA breach penalties (currently ₹62,067/quarter).

---

## 5. Quality Guardrails & Confounder Governance

To ensure operational efficiency gains are not achieved at the expense of customer satisfaction or policy compliance, two mandatory guardrails are instituted:

1. **CSAT Floor Guardrail**: Mean agent CSAT must remain at or above **3.33 / 5.00**. Any agent whose handle time drops but whose CSAT falls below 3.00 will be flagged for quality remediation.
2. **SLA Breach Ceiling**: First-response SLA breach rate must not exceed **9.06%**. Efficiency must not be achieved by delaying customer ticket pickups.
3. **Hardware Defect Non-Interference**: Agents will be strictly trained to follow Policy §4 warranty guidelines for Pulse 2 charging pin defects, without artificially suppressing replacements or frustrating customers.
