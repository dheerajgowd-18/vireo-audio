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
> **"Reduce Tier 1 frontline (Chat and Email) above-median handle time from 6.54h to 4.86h (weighted peer medians: Chat 5.61h -> 3.81h, Email 8.49h -> 7.07h), eliminating 624.9 excess agent-hours per quarter, representing approximately ₹1,03,102 per quarter in recoverable staffing capacity."**

### Underlying Data & Policy Evidence:
- **Audit Scope**: 11,750 tickets, 44 agents over 18 months (6 calendar quarters).
- **Valid Ticket Baseline**: Evaluated strictly on **11,183 valid completed handle-time tickets** (`status in {resolved, closed}`, `handle_time >= 0`).
- **Chat Frontline**: 15 agents; 7 above-median agents handle 1,519 valid tickets with a weighted mean of **5.61h** against the team peer median of **3.81h** (-1.80h/ticket). Excess hours = 2,731.18h / 18 mo = 455.20h/quarter $\times$ ₹165/hr (Policy §4) = **₹75,107.40/quarter**.
- **Email Frontline**: 7 agents; 3 above-median agents handle 718 valid tickets with a weighted mean of **8.49h** against the team peer median of **7.07h** (-1.42h/ticket). Excess hours = 1,017.97h / 18 mo = 169.66h/quarter $\times$ ₹165/hr = **₹27,994.19/quarter**.
- **Combined Frontline Capacity Recovery**:
  - Current weighted handle time: $\frac{8,522.83 + 6,096.88}{2,237} = \mathbf{6.54 \text{ hours}}$.
  - Target weighted handle time: $\frac{5,791.66 + 5,078.91}{2,237} = \mathbf{4.86 \text{ hours}}$.
  - Excess hours eliminated: $455.20 + 169.66 = \mathbf{624.86 \text{ hours/quarter}}$.
  - Quarterly capacity value @ ₹165/hr: **₹1,03,101.59 per quarter** (~**₹1.03L/quarter**).
- **Accounting Interpretation**: Converted via Policy §4 at ₹165 per agent-hour. Represents **recoverable staffing capacity value** (freeing up labor to absorb ticket growth without adding headcount), rather than direct cash payroll cuts.
- **Full Tier 1 Upper-Bound Benchmark**: Across all 38 Tier 1 agents, bringing above-p25 agents to the 25th percentile efficiency eliminates 2,154.4 excess hours/quarter $\times$ ₹165/hr = **₹3,55,481 per quarter (~₹3.55L/quarter)**.

---

## Question 2: Training Budget Deployment & Target Selection

### Prompt:
*How should Priya deploy the ₹4,00,000 Q3 training budget, and who should (or should not) be trained?*

### Official Submission Answer:
1. **Do NOT Train the Raw Bottom 10**: The raw bottom 10 agents by CSAT / handle time comprise **6 Tier 2 escalation specialists** and **4 specialized hardware triage agents**. These agents handle complex, multi-day, pre-escalated customer disputes and defective hardware where CSAT is structurally depressed (2.4 – 2.9). Forcing senior specialists into frontline remedial training would waste budget and degrade morale.
2. **Target Population**: Deploy the training budget to the **22 frontline Tier 1 agents in Chat and Email**, focusing 1-on-1 coaching on the 10 agents currently above their team peer medians.
3. **Curriculum Deployment**:
   - **Module 1 (Diagnostic SOPs & Note Standardization)**: Currently, 908 tickets (7.73%) contain uninformative shorthand notes ("-", "done", "cx ok"). Standardizing templates prevents repetitive discovery loops.
   - **Module 2 (First Contact Resolution & Escalation Protocols)**: Frontline agents learn to resolve tier-appropriate tickets, reducing inter-tier transfers (currently 1,215 transfers costing ₹3,70,575 under Policy §4) and repeat contacts (3,277 repeats costing ₹9,03,890).
   - **Module 3 (Tooling, Macros & Aging Ticket Sweep Routines)**: 93-95% of tickets are resolved in <1 hour; coaching agents on daily sweeps of multi-day pending tickets directly addresses the right-tail skew elevating average handle times.
   - *Budget Governance*: Use the ₹4,00,000 budget for peer-benchmarked Tier 1 workflow/troubleshooting training, with final allocation determined by intervention design and baseline needs.

---

## Question 3: Financial Exposure & Accounting Reconciliation

### Prompt:
*What is the true financial exposure of Vireo Audio support operations, and how does it reconcile with Finance's initial estimates?*

### Official Submission Answer:
- **Total Tracked Support Operating Exposure**: **₹1,27,62,896** (~₹1.276 Crore).
- **Direct Operating Expenses**: **₹74,12,025** (~₹74.12 Lakhs):
  - Contact Labor Costs: **₹32,53,060** (Policy §4 hourly labor across 16,707 handle hours).
  - Warranty Replacements: **₹34,15,990** (Policy §5 actual BOM cost + ₹340 logistics).
  - SLA Breach Credits: **₹3,72,400** (Policy §3: 1,064 breaches @ ₹350 store credit).
  - Internal Transfers: **₹3,70,575** (Policy §4: 1,215 transfers @ ₹305 fee).
- **Sales Revenue Reversals (Refunds)**: **₹53,50,871** (1,869 order transactions refunded under Policy §5).
- **Finance Estimation Audit**: Finance Controller Arjun Mehta estimated replacements at a flat ₹2,500/unit, projecting ₹47,40,000. True policy replacement cost is ₹34,15,990. Finance **overstated replacement liability by ₹13,24,010 (+38.76%)**.
- **Accounting Distinction**: Operating exposure reflects direct customer support allocations under policy rules; it is not a corporate P&L statement.

---

## Question 4: Product Defect & Operational Root-Cause Findings

### Prompt:
*What explains the 100% surge in replacement spend, and how should Vireo address it?*

### Official Submission Answer:
- **Product Concentration**: Wireless earbud model **Pulse 2** accounts for **1,166 out of 1,896 total replacements (61.50%)** and **₹21,22,120.00** of policy replacement spend (1,166 units $\times$ [₹1,480 BOM + ₹340 logistics = ₹1,820/unit] under Policy §5).
- **Batch Concentration**: Manufacturing lot **`PL2-2510-3`** generated **70 replacements** across 171 tickets on direct `order_id` join (40.94% replacement rate, ₹1,27,400 spend).
- **Physical Root Cause (Qualitative Evidence)**: Analysis of customer messages and agent notes identifies physical charging pin contact failure and charging cradle detachment.
- **Unverified Status**: Physical metallurgy or component failure mechanisms have not been independently laboratory-tested. Lot `PL2-2510-3` is classified as a **"high-replacement lot candidate."**
- **Strategic Action**: Support training cannot fix defective manufacturing hardware. Recommending support training to reduce replacements would violate Policy §5 warranty obligations. This finding is formally escalated to **Hardware Engineering & Supply Chain** as an operational signal requiring hardware and supplier investigation.

---

## Question 5: Data Integrity & Critical Engineering Caveats

### Prompt:
*What critical data traps and data hygiene issues were uncovered during the technical audit?*

### Official Submission Answer:
1. **Display Name Collision**: Two distinct agents share the exact name **"Kavya Pandey"**:
   - `A3006`: Tier 1 Chat Frontline agent (Indore).
   - `A3029`: Tier 1 Logistics agent (Bengaluru).
   - *Fix*: Strict foreign key joining on `agent_id`; zero joins on display name.
2. **CSAT Missing Data Governance**: 6,554 tickets (55.78%) lack CSAT survey responses. The mean CSAT of 3.33 is computed strictly over the 5,196 valid responses under Policy §8. Treating missing surveys as 0 would artificially distort CSAT to 1.47, destroying metric validity.
3. **Telephony IVR Glitch**: Approximately 40 tickets contain corrupt phone system IVR navigation transcripts in the customer message field. This is an automated telephony ingestion bug, not an agent performance issue.
4. **Legacy Freshdesk Timestamps**: 2,347 tickets migrated from Freshdesk (`source_system = legacy_fd`) contained UTC timestamps requiring a +05:30 offset to align with helpdesk IST business hours.
