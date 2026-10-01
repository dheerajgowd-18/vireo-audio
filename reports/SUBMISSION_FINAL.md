# Vireo Audio Support Intelligence & Performance Evaluation
## Client Final Submission Form & Technical Audit Responses

**Candidate / Engineer:** Lead Data & AI Engineer  
**Evaluation Scope:** 11,750 Tickets, 44 Support Agents, 18 Months (Jan 2024 – Jun 2025)  
**Date of Submission:** October 1, 2026  
**Status:** Complete, Audited & Defensible  

---

### Links & Metadata

* **Screen Recording Video Link:** `[PLACEHOLDER — PUBLIC GOOGLE DRIVE VIDEO LINK]`
* **Public Google Drive Folder Link:** `[PLACEHOLDER — PUBLIC DRIVE FOLDER LINK]`
* **Engineering Hours Spent:** `[TO BE FILLED BY CANDIDATE]`
* **Public GitHub Repository URL:** `https://github.com/dheerajgowd-18/vireo-audio.git`

---

### Question 1: Primary Business Goal Statement

> **"Reduce Tier 1 frontline (Chat and Email) above-median handle time from 6.54h to 4.86h (weighted peer medians: Chat 5.61h -> 3.81h, Email 8.49h -> 7.07h), eliminating 624.9 excess agent-hours per quarter, representing approximately ₹1,03,102 per quarter in recoverable staffing capacity."**

**Mathematical & Accounting Derivation:**
* Evaluated across **11,183 valid attendance tickets** (`status in {resolved, closed}`, duration $\ge 0$). Open and pending tickets (567 tickets) lack resolution timestamps and are excluded from handle-time multipliers.
* **Chat Frontline (15 agents)**: 7 above-median agents handle 1,519 valid tickets at a weighted average of 5.61h vs. the team peer median of 3.81h (-1.80h/ticket). Excess hours = 2,731.18h over 18 months = 455.20h/quarter $\times$ ₹165/hr (Policy §4) = **₹75,107.40/quarter**.
* **Email Frontline (7 agents)**: 3 above-median agents handle 718 valid tickets at a weighted average of 8.49h vs. the team peer median of 7.07h (-1.42h/ticket). Excess hours = 1,017.97h over 18 months = 169.66h/quarter $\times$ ₹165/hr = **₹27,994.19/quarter**.
* **Combined Frontline Impact**: Eliminates $455.20 + 169.66 = \mathbf{624.86 \text{ agent-hours/quarter}}$. At the Policy §4 rate of ₹165/hr, this represents **₹1,03,101.59 per quarter** (~₹1.03L/quarter) in modeled recoverable staffing capacity value (operational bandwidth to absorb ticket growth without adding headcount).
* **Upper-Bound Benchmark Across Tier 1**: Bringing all above-p25 Tier 1 agents to the 25th percentile peer efficiency eliminates 2,154.4 excess hours/quarter, yielding **₹3,55,481 per quarter (~₹3.55L/quarter)**.

---

### Question 2: Why the "Bottom 10" Ranking is the Wrong Problem to Solve

A naive company-wide sort by raw CSAT or handle time misdiagnoses support operations due to structural role conflation:
1. **Tier 2 Structural Penalization**: Six of the bottom ten agents (`A3039` Sameer Ghosh, `A3040` Tarun Fernandes, `A3041` Jaspreet Desai, `A3042` Sneha Sethi, `A3043` Kabir Varghese, `A3044` Pranav Khanna) are Tier 2 Escalation specialists. They handle pre-escalated, highly frustrated customers with complex multi-day warranty and RMA disputes. Under Policy §6, Tier 2 is evaluated on resolution in days, not tickets closed per week. Their lower CSAT (2.42–2.83) reflects ticket complexity, not poor individual performance.
2. **Hardware Triage Rota Penalization**: The remaining four agents (`A3004` Siddharth Kapoor, `A3005` Zaid Khanna, `A3006` Kavya Pandey, `A3007` Siddharth Trivedi) are frontline agents assigned to the high-friction hardware RMA triage rota ("Kavya's four"). Customers reaching this rota already possess physically defective hardware, structurally depressing CSAT to 2.98–3.04.
3. **Operational Consequence**: Forcing senior Tier 2 engineers into frontline remedial training would waste the ₹4.0L budget and severely degrade team morale. Support evaluation must benchmark agents strictly against peers within their operational tier.

---

### Question 3: Recommended Deployment of the ₹4,00,000 Training Budget

Deploy the ₹4,00,000 budget to upskill the **22 frontline Tier 1 agents across Chat (15) and Email (7)**, with dedicated 1-on-1 coaching for the 10 agents operating above their peer medians:
* **Module 1: Diagnostic SOPs & Note Standardization (₹1,75,000)**: Standardizes diagnostic intake checklists and eliminates shorthand notes. In our audit, 908 tickets (7.73%) contained uninformative shorthand notes (`words <= 2 OR characters <= 9`, e.g., `"-"`, `"done"`), forcing downstream agents into redundant discovery cycles.
* **Module 2: FCR Protocols & Escalation Boundary Management (₹1,25,000)**: Trains agents on resolving tier-appropriate issues to avoid unnecessary transfers. Historically, 1,215 inter-tier transfers generated ₹3,70,575 in transfer overhead (Policy §4: ₹305/transfer) and drove 3,277 30-day repeat contacts.
* **Module 3: Queue Sweeps & Aging Ticket Management (₹1,00,000)**: In frontline channels, 93–95% of tickets resolve in under an hour; average handle time is inflated by a 5–7% right-tail of multi-day lingering tickets. Coaching agents on systematic daily sweeps directly compresses this long-tail delay.

---

### Question 4: True Financial Exposure vs. Finance Estimates

* **Total Tracked Support Financial Exposure**: **₹1,27,62,896** (~₹1.276 Crore).
* **Direct Operating Expenses**: **₹74,12,025** (~₹74.12 Lakhs):
  * Channel Contact Labor: **₹32,53,060** (Policy §4 labor across 16,707 handle hours).
  * Warranty Replacements: **₹34,15,990** (Policy §5 actual BOM + ₹340 logistics).
  * First-Response SLA Credits: **₹3,72,400** (Policy §3: 1,064 breaches @ ₹350 store credit).
  * Internal Transfer Overhead: **₹3,70,575** (Policy §4: 1,215 transfers @ ₹305 fee).
* **Customer Commercial Refunds (Sales Reversals)**: **₹53,50,871** (1,869 transactions refunded under Policy §5).
* **Finance Overstatement Reconciliation**: Finance Controller Arjun Mehta estimated replacement liability at a flat ₹2,500/unit across 1,896 replacements, projecting ₹47,40,000. Under Policy §5 (actual product BOM cost + ₹340 logistics), actual replacement spend was ₹34,15,990. Finance **overstated replacement liability by ₹13,24,010 (+38.76%)**.

---

### Question 5: Product Defect & Operational Root-Cause Findings

* **Product Concentration**: The **Pulse 2** wireless earbud model (`VA-EB-PL2`) drives **61.50% of all company replacements (1,166 out of 1,896 units)**, incurring **₹21,22,120.00** in policy replacement spend (1,166 units $\times$ [₹1,480 BOM + ₹340 logistics = ₹1,820]).
* **Manufacturing Lot Concentration**: Production lot **`PL2-2510-3`** generated **70 replacements** across 171 tickets on direct `order_id` join—a severe **40.94% replacement rate** (₹1,27,400 spend).
* **Observed Text Signature**: Customer messages and agent notes consistently describe physical charging pin contact failure and charging cradle detachment.
* **Engineering Caveat**: Physical metallurgy and factory solder joints have not been independently laboratory-tested. Lot `PL2-2510-3` is classified as a **"high-replacement lot candidate."**
* **Strategic Escalation**: Frontline support training cannot fix defective manufacturing hardware. Recommending agent coaching to reduce replacements would violate Policy §5 warranty obligations. This finding is formally escalated to Hardware Engineering and Supply Chain for supplier warranty recovery.

---

### Question 6: Critical Data Traps & Hygiene Discoveries

1. **Display Name Collision**: Two distinct agents share the exact display name **"Kavya Pandey"**:
   * `A3006`: Tier 1 Chat Frontline agent based in Indore (Morning shift).
   * `A3029`: Tier 1 Logistics agent based in Bengaluru (Morning shift).  
   *Resolution*: All joins and metric calculations key strictly on `agent_id`; display names are never used as keys.
2. **CSAT Missing Data Governance**: 6,554 tickets (55.78%) lack CSAT survey ratings. Under Policy §8, blank surveys must be excluded from averages. Mean CSAT is **3.33 / 5.00** across 5,196 valid responses. Imputing blanks as 0 would have falsely collapsed CSAT to 1.47.
3. **Legacy Freshdesk Timestamps**: 2,309 tickets from `source_system == 'legacy_fd'` had `resolved_at < first_response_at` due to UTC event log reconstruction. Applying a +05:30 IST offset resolved 100% of negative durations.
4. **Risky Fallback Order Joins Avoided**: 4,107 tickets lack `order_id`. Joining on `(customer_id, product_sku)` would have created 1,388 duplicate ticket collisions (Cartesian join). Analysis is restricted to direct `order_id` links.
5. **Telephony IVR Ingestion Glitch**: Approximately 40 tickets contain corrupt phone system navigation text (`"Press 1 for support..."`). This is an automated IVR ingestion defect, not an agent performance flaw.

---

### Question 7: AI/Text Evaluation Methodology & Honest Cross-Validation Performance

* **Cross-Validation Performance**: Evaluated via held-out **5-fold stratified cross-validation** using TF-IDF + Logistic Regression across the 180-ticket benchmark:
  * **Accuracy:** **55.56%** (100 / 180 out-of-fold correct predictions)
  * **Macro Precision:** **0.5342**
  * **Macro Recall:** **0.5528**
  * **Macro F1-Score:** **0.5388**
* **The 98.89% In-Sample Clarification**: The previously cited 98.89% was an in-sample training metric caused by evaluating a model on its own training data. True generalization accuracy is 55.56%.
* **Baseline Hierarchy**:
  1. *Majority Class Baseline (`connectivity_pairing`)*: 26.67% accuracy (Macro F1: 0.0468) — statistical floor.
  2. *Simple Keyword Rules*: 46.11% accuracy (Macro F1: 0.5399).
  3. *Pure ML (5-Fold CV)*: 55.56% accuracy (Macro F1: 0.5388) — +28.89% gain over majority floor.
  4. *Hybrid Pipeline (Rules + CV ML Fallback)*: 65.56% accuracy (Macro F1: 0.6443) — operational peak.
* **Hardware Defect Detector Performance**: On the benchmark sample, the regex detector achieves:
  * **Precision: 100.00%** ($TP=8, FP=0$)
  * **Recall: 47.06%** ($TP=8, FN=9$)
  * **F1-Score: 64.00%**  
  The previously cited 94.87% was negative-class precision ($163 / 172$). The detector operates as a zero-false-positive conservative filter.
* **Prompt Comparison Status**: Prompt v1 vs. v2 comparisons (82.22% vs. 92.78%) were simulated offline heuristics. Zero cloud LLM API calls were executed; cross-validation is our sole quantitative benchmark.
* **Label Provenance**: All benchmark labels are explicitly documented as **rule-assisted pseudo-labels**, not double-blind human annotations.

---

### Question 8: Recovery of the "Other" Ticket Category

In the intake dataset, 1,732 tickets (14.74% of all tickets) were classified as "Other." Our hybrid classifier recovered **1,524 actionable tickets (87.99%)** into operational categories:
* `delivery_shipping`: 378 tickets (21.82%)
* `connectivity_pairing`: 338 tickets (19.52%)
* `returns_refunds`: 229 tickets (13.22%)
* `cancellation`: 202 tickets (11.66%)
* `charging_battery`: 159 tickets (9.18%)
* `billing_payment`: 91 tickets (5.25%)
* `hardware_audio_defect`: 74 tickets (4.27%)
* `product_enquiry_setup`: 53 tickets (3.06%)
* `other_unclear`: 208 tickets (12.01%) — preserved as genuinely ambiguous.

---

### Question 9: Software & Analytical Architecture Overview

The system is structured as an auditable pipeline with strict separation between business logic, analytical outputs, and UI:
```
[Raw CSVs: tickets, agents, orders, products]
                   │
                   ▼
      [Analytical Engine: src/]
      ├── data_loader.py (type coercion, legacy +05:30 offset)
      ├── data_quality.py (PK/FK validation, Cartesian prevention)
      ├── metrics.py (CSAT blanks excluded, attendance handle time)
      ├── financials.py (policy replacement costs, transfer penalties)
      ├── agent_analysis.py (peer stratification, rota tagging)
      ├── text_classifier.py (5-fold CV, TF-IDF + Logistic Regression)
      └── text_analysis.py ('Other' decomposition, defect ledger)
                   │
                   ▼
   [Analytical Outputs & Governance: reports/]
   ├── agent_scorecard.csv, monthly_trends.csv, lot_code_analysis.csv
   ├── text_predictions.csv, cv_predictions.csv, text_pseudo_labels.csv
   ├── DECISION_SPEC.md, CV_EVALUATION.md, TEXT_MODEL_CARD.md
   └── AI_ENGINEERING_DEFENSE.md, WEB_UI_DECISIONS.md
                   │
                   ▼ (python scripts/build_web_data.py)
      [Static Web Data: web/data/]
      ├── overview.json, agents.json, trends.json
      ├── replacements.json, sla.json, ai_signals.json, methodology.json
                   │
                   ▼ (python -m http.server 8000 --directory web)
      [Vanilla Web Frontend: web/]
      ├── index.html (Semantic 7-view structure & drawer)
      ├── styles.css (Minimal SaaS design system)
      └── app.js (Native DOM router, table sorting, SVG charts)
```

---

### Question 10: Frontend Design Principles & UI Architecture

The frontend is built with **zero external dependencies** using native **HTML5, CSS3, and Vanilla JavaScript**:
1. **Design System & Aesthetics**: Minimalist SaaS aesthetic inspired by Linear and Stripe (restrained monochrome palette, neutral borders, single accent color `#0284c7`, monospace tabular figures).
2. **Seven Dedicated Views**:
   * `Overview`: Executive KPI cards, monthly ticket volumes, channel distribution.
   * `Agent Performance`: Full 44-agent scorecard with peer-group filtering, search, and sorting.
   * `Requested Bottom 10`: The client's requested view with immediate contextual callouts explaining Tier 2 and hardware triage roles.
   * `AI Signals`: Issue category distributions, "Other" decomposition breakdown, model card, and confusion matrix.
   * `Replacements`: Product replacement rates, Pulse 2 cost breakdown (₹21.22L), and manufacturing lot analysis.
   * `SLA & Cost`: Channel SLA breach rates and financial exposure ledger.
   * `Methodology`: Complete mathematical definitions, policy citations, and data lineage documentation.
3. **Agent Drawer**: Slide-out detail drawer displaying an individual agent's metrics, peer benchmark comparison, shift, site, and hardware defect exposure.
4. **Performance & Reliability**: Zero external CDN calls or heavy JS frameworks. Loads in <50ms with 100% offline operational reliability.

---

### Question 11: Systems Engineering Trade-offs & Budget Optimization

1. **Local NLP vs. Cloud LLM Inference**:
   * *Decision*: Deployed local scikit-learn TF-IDF + Logistic Regression instead of calling external LLMs 11,750 times.
   * *Financial Impact*: Zero paid cost (₹0.00) vs. ₹58,750 estimated cloud API cost (100% cost avoidance). Preserved the client's ₹4.0L budget entirely for human coaching.
   * *Latency*: Full dataset classified in **3.8 seconds** (~3,000 tickets/sec) vs. ~98 minutes over HTTPS.
   * *Privacy & Governance*: Zero customer PII transmitted across external networks.
2. **Deterministic Rules vs. Statistical Models**: High-confidence regex rules handle explicit domain boundaries (e.g., cancellations and defect keywords), while statistical ML classifies ambiguous text.
3. **Vanilla Web Stack vs. Modern JS Frameworks**: Avoided React/Next.js/Tailwind build pipelines. The zero-dependency vanilla stack runs natively on any modern browser via a lightweight local server.

---

### Question 12: Data Modeling Safeguards & Defensibility

1. **Cartesian Join Prevention**: Prohibited fallback joins on `(customer_id, product_sku)` for unlinked tickets, preventing 1,388 duplicate ticket collisions.
2. **Defect Exposure Transparency**: Surfaced `hw_defect_share_pct` on individual agent scorecards, protecting agents assigned to defective Pulse 2 batches from unfair evaluation.
3. **Non-Punitive Anomaly Classification**: Instances where both a refund and a replacement occurred (6 tickets, 131 orders) are neutrally categorized as "policy compliance exceptions requiring review" rather than fraud.

---

### Question 13: Summary Recommendations for Priya & Executive Leadership

1. **Authorize Training Reallocation**: Formally allocate the ₹4,00,000 budget across the three frontline Tier 1 modules (Diagnostic SOPs ₹1.75L, FCR Protocols ₹1.25L, Queue Sweeps ₹1.00L).
2. **Exempt Specialists from Remedial Action**: Remove Tier 2 specialists and hardware triage agents from the "Bottom 10" remediation list. Benchmark agents strictly within their operational peers.
3. **Escalate Pulse 2 Lot Quality**: Deliver the lot `PL2-2510-3` analysis to Hardware Engineering and Supply Chain to initiate vendor warranty clawbacks on the ₹21.22L replacement exposure.
4. **Deploy Ticket Note Standards**: Mandate diagnostic intake templates and deprecate uninformative shorthand notes across the helpdesk platform.
