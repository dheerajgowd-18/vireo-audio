# Internship Evaluation Submission Facts & Evidence Reference

**Project**: Vireo Audio Support Intelligence & Performance Evaluation  
**Target Submission**: Technical Internship Evaluation / Client Assessment  
**Author**: Lead Data & AI Engineer  
**Status**: Ready for Final Review  

---

## Question 1: Primary Business Goal Formulation

### Prompt:
*State the primary business goal in the format: "Reduce X from A to B, representing approximately ₹Y per quarter."*

### Official Submission Answer:
> **"Reduce frontline Tier 1 above-median handle time across Chat (from 4.38h to 3.81h) and Email (from 6.70h to 7.07h peer median), eliminating 650.8 excess agent-hours per quarter, representing approximately ₹1,07,379 per quarter in recoverable support capacity (scaling to ₹3,73,266 per quarter when targeting the 25th percentile peer benchmark across all Tier 1 agents)."**

### Underlying Data & Policy Evidence:
- **Audit Scope**: 11,750 tickets, 44 agents over 18 months (6 calendar quarters).
- **Target Population**: 22 Tier 1 Frontline agents (15 Chat, 7 Email).
- **Chat Frontline**: 2,752 tickets, mean handle 4.38h vs team median of means 3.81h. Excess hours = 2,836.0h / 18 mo = 472.7h/quarter $\times$ ₹165/hr (Policy §8) = **₹77,990.25/quarter**.
- **Email Frontline**: 1,327 tickets, mean handle 6.70h vs team median of means 7.07h. Excess hours = 1,068.7h / 18 mo = 178.1h/quarter $\times$ ₹165/hr = **₹29,389.33/quarter**.
- **Combined Immediate Frontline Savings**: $472.7 + 178.1 = \mathbf{650.8 \text{ hours/quarter}} = \mathbf{₹1,07,379.58 \text{ per quarter}}$ (~**₹1.07L/quarter**).
- **Full Tier 1 Upper-Quartile (p25) Stretch Benchmark**: Across all 38 Tier 1 agents, bringing above-p25 agents to the 25th percentile efficiency eliminates 2,262.2 excess hours/quarter $\times$ ₹165/hr = **₹3,73,266 per quarter (~₹3.73L/quarter)**, delivering a **93.3% capital efficiency match** against the ₹4,00,000 Q3 training budget.

---

## Question 2: Training Budget Deployment & Target Selection

### Prompt:
*How should Priya deploy the ₹4,00,000 Q3 training budget, and who should (or should not) be trained?*

### Official Submission Answer:
1. **Do NOT Train the Raw Bottom 10**: The raw bottom 10 agents by CSAT / handle time comprise **6 Tier 2 escalation specialists** and **4 specialized hardware triage agents**. These agents handle complex, multi-day, pre-escalated customer disputes and defective hardware where CSAT is structurally depressed (2.4 – 2.9). Forcing senior specialists into frontline remedial training would waste budget and degrade morale.
2. **Target Population**: Deploy the training budget to the **22 frontline Tier 1 agents in Chat and Email**, stratified against their respective peer medians.
3. **Module Budget Allocation**:
   - **Module 1 (₹1,75,000)**: Diagnostic SOPs & Note Standardization. Currently, 31.4% of tickets (36.1% in Chat) have uninformative notes ("done", "fixed"). Standardizing templates prevents repetitive discovery loops.
   - **Module 2 (₹1,25,000)**: First Contact Resolution (FCR) & Escalation Protocols. Frontline agents learn to resolve tier-appropriate tickets, reducing inter-tier transfers (currently 1,215 transfers costing ₹3,70,575) and repeat contacts (3,277 repeats costing ₹9,03,890).
   - **Module 3 (₹1,00,000)**: Tooling & Navigation Simulator. Standardized macro usage to lower first-response latency and prevent SLA breach credits (currently 1,064 breaches costing ₹3,72,400).

---

## Question 3: Financial Exposure & Accounting Reconciliation

### Prompt:
*What is the true financial exposure of Vireo Audio support operations, and how does it reconcile with Finance's initial estimates?*

### Official Submission Answer:
- **Total Tracked Support Operating Exposure**: **₹1,27,62,896** (~₹1.276 Crore).
- **Direct Operating Expenses**: **₹74,12,025** (~₹74.12 Lakhs):
  - Contact Labor Costs: **₹32,53,060** (Policy §8 hourly labor across 16,707 handle hours).
  - Warranty Replacements: **₹34,15,990** (Policy §4 actual BOM cost + ₹340 logistics).
  - SLA Breach Credits: **₹3,72,400** (Policy §3: 1,064 breaches @ ₹350 store credit).
  - Internal Transfers: **₹3,70,575** (Policy §6: 1,215 transfers @ ₹305 fee).
- **Sales Revenue Reversals (Refunds)**: **₹53,50,871** (1,869 order transactions refunded under Policy §5).
- **Finance Estimation Audit**: Finance Controller Arjun Mehta estimated replacements at a flat ₹2,500/unit, projecting ₹47,40,000. True policy replacement cost is ₹34,15,990. Finance **overstated replacement liability by ₹13,24,010 (+38.76%)**.
- **Accounting Distinction**: Operating exposure reflects direct customer support allocations under policy rules; it is not a corporate P&L statement.

---

## Question 4: Product Defect & Operational Root-Cause Findings

### Prompt:
*What explains the 100% surge in replacement spend, and how should Vireo address it?*

### Official Submission Answer:
- **Product Concentration**: Wireless earbud model **Pulse 2** accounts for **1,166 out of 1,896 total replacements (61.50%)** and **₹22,38,720** of policy replacement spend.
- **Batch Concentration**: Manufacturing lot **`PL2-2510-3`** alone generated **730 replacements** (62.6% of Pulse 2 replacements, 38.5% of company-wide replacements).
- **Physical Root Cause**: Qualitative analysis of customer messages and agent notes identifies physical charging pin corrosion and case connector detachment.
- **Strategic Action**: Support training cannot fix defective manufacturing hardware. Recommending support training to reduce replacements would violate Policy §4 warranty obligations. This finding is formally escalated to **Hardware Engineering & Vendor Quality** for component redesign and supplier warranty clawback.

---

## Question 5: Data Integrity & Critical Engineering Caveats

### Prompt:
*What critical data traps and data hygiene issues were uncovered during the technical audit?*

### Official Submission Answer:
1. **Display Name Collision**: Two distinct agents share the exact name **"Ananya Rao"**:
   - `AG-0004`: Tier 1 Voice frontline agent (Bangalore).
   - `AG-0041`: Tier 2 Escalation specialist (Mumbai).
   - *Fix*: Strict foreign key joining on `agent_id`; zero joins on display name.
2. **CSAT Missing Data Governance**: 6,554 tickets (55.78%) lack CSAT survey responses. The mean CSAT of 3.33 is computed strictly over the 5,196 valid responses. Treating missing surveys as 0 would artificially distort CSAT to 1.47, destroying metric validity.
3. **Telephony IVR Glitch**: Approximately 40 tickets contain corrupt phone system IVR navigation transcripts in the customer message field. This is an automated telephony ingestion bug, not an agent performance issue.
4. **Legacy Freshdesk Timestamps**: 2,347 tickets migrated from Freshdesk (`source_system = legacy_fd`) contained UTC timestamps requiring a +05:30 offset to align with helpdesk IST business hours.

---

## Question 6: AI / ML Text Classification Architecture & Generalization Defense

### Prompt:
*How was the AI/text classification layer designed, evaluated, and defended against technical scrutiny?*

### Official Submission Answer:
- **Zero Cloud Inference API Dependency**: Runs 100% locally with zero per-ticket API costs, completely honoring Finance Controller Arjun Mehta's budget constraint ($11,750 \times ₹5 = ₹58,750$ saved).
- **'Other' Category Theme Decomposition**: Recovered **1,524 out of 1,732 (87.99%)** uninformative `'Other'` tickets into actionable operational themes (Bluetooth Pairing, Shipping Delay, Battery Failure), leaving only 208 (12.01%) genuinely unclear.
- **5-Fold Held-Out Cross-Validation on Stratified Benchmark**:
  - Majority Class Baseline: 26.67% accuracy, 0.0700 Macro F1.
  - Keyword Rule Baseline: 46.11% accuracy, 0.4468 Macro F1.
  - Pure ML (TF-IDF + Logistic Regression): 55.56% accuracy, 0.5388 Macro F1.
  - Production Hybrid Pipeline (Rules + ML Fallback): **65.56% accuracy, 0.6443 Macro F1**.
  - *Engineering Honesty*: We rejected in-sample memorization claims (98.89%) in favor of true held-out generalization metrics.
- **Hardware Defect Text Signal**: Precision = **100.00%** (8 TP, 0 FP), Recall = **47.06%**, F1 = **64.00%**. Intentionally conservative to prevent false engineering alarms.

---

## Question 7: Frontend Dashboard Architecture

### Prompt:
*What architectural choices were made for the user interface, and why?*

### Official Submission Answer:
- **Pure Vanilla Stack**: Built with semantic **HTML5, modern CSS3, and native Vanilla JavaScript (ES6+)**. Zero external frameworks (no React, Next.js, Streamlit, Tailwind, or Bootstrap) and zero CDN dependencies.
- **Inline SVG Data Visualizations**: Rendered dynamically with sub-millisecond execution times and zero bundle bloat.
- **Pre-Aggregated Static JSON Data**: Fast offline execution with zero client-side CSV parsing. Fully operational on `python -m http.server 8000 --directory web`.
- **Restrained SaaS Design System**: Inspired by Linear, Vercel, and Stripe with monochrome neutrals, crisp borders, peer-stratified scorecards, detail flyout drawers, and transparent data methodology modals.
