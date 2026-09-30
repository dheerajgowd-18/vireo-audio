# Business KPI Evaluation: Strategic Candidate Analysis

**Document Scope**: Evaluation of 7 Candidate Support Operations KPIs for Vireo Audio  
**Target Investment**: ₹4,00,000 Q3 Training Budget  
**Evaluation Author**: Lead Data & AI Engineer  
**Status**: Completed & Defended  

---

## 1. Executive Summary & Evaluation Framework

Vireo Audio's executive leadership requested the identification of a single primary business goal to govern the deployment of the ₹4,00,000 Q3 training budget. To ensure the final selection is mathematically rigorous, operationally realistic, and technically defensible in an executive or board interview, seven candidate KPIs were evaluated against five strict criteria:

1. **Measurability & Data Grounding**: Can the metric be calculated deterministically from existing support datasets without unverified assumptions?
2. **Addressability via Frontline Training**: Can the metric be realistically improved through support coaching and workflow training, rather than external hardware/logistics fixes?
3. **Policy-Governed Rupee Conversion**: Does the Vireo Support Policy (Rev 2026.1) provide an explicit, auditable financial conversion formula?
4. **Economic Scale vs. ₹4.0 Lakh Budget**: Does the quarterly addressable financial exposure justify a ₹4,00,000 investment?
5. **Interview Defensibility**: Is the metric free from cross-tier structural bias, false causality, and uncalibrated claims?

---

## 2. Evaluation Matrix of 7 Candidate KPIs

| Candidate KPI | Primary Dimension | Measurability | Training Addressability | Explicit Rupee Conversion | Quarterly Economic Scale | Interview Defensibility | Overall Recommendation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. CSAT Score Improvement** | Customer Satisfaction | High (5,196 ratings) | Moderate | **None** (Policy lacks CSAT-to-INR formula) | High (Indirect / Churn) | Low (Lacks policy cash conversion) | **Secondary Metric** |
| **2. Tier 1 Handle Time Optimization** | Operational Efficiency | **High** (Deterministic) | **High** (Workflow coaching) | **High** (Policy §8 hourly labor rates) | **₹1.07L – ₹3.73L / qtr** | **High** (Peer-stratified benchmarking) | **SELECTED PRIMARY GOAL** |
| **3. SLA Breach Reduction** | Service Level Adherence | High (1,064 breaches) | Moderate | High (Policy §3: ₹350 credit) | Low (Max ₹62,067 / qtr) | Moderate (Scale too small for ₹4L) | Rejected as Primary |
| **4. Inter-Tier Transfer Reduction** | Workflow Routing | High (1,215 transfers) | Moderate (Frontline FCR) | High (Policy §6: ₹305 fee) | Low (Max ₹61,763 / qtr) | Moderate (Scale too small for ₹4L) | Rejected as Primary |
| **5. Repeat Contact / FCR Avoidance** | Resolution Quality | High (3,277 repeats) | High (Diagnostic depth) | High (Channel contact labor rates) | Moderate (₹1.18L – ₹1.51L / qtr) | High (Root-cause resolution) | **Strong Complementary Goal** |
| **6. Warranty Replacements (Pulse 2)** | Inventory Risk | High (1,896 units) | **Zero** (Hardware batch defect) | High (BOM + ₹340 logistics) | Very High (₹3.73L / qtr for Pulse 2) | **Unacceptable** (False causal leap) | **REJECTED (Engineering Issue)** |
| **7. Note Quality / IVR Cleanup** | Data Hygiene | High (Regex/Heuristic) | High (Template training) | Low (Indirect labor efficiency) | Negligible | Low (Process hygiene, not business KPI) | Process Enabler Only |

---

## 3. In-Depth Analysis of Individual Candidates

### Candidate 1: CSAT Score Improvement (e.g., Raise CSAT from 3.33 to 3.80)
- **Strengths**: High executive visibility; measured across 5,196 customer responses (44.22% response rate).
- **Critical Flaw**: **Zero Policy Rupee Conversion Rate**. The Vireo Support Policy defines no financial formula converting CSAT points to cash savings. Converting CSAT to revenue requires fabricating unverified customer lifetime value (LTV) or churn elasticity assumptions, violating the mandate against unsubstantiated claims.
- **Verdict**: Tracked as a key secondary quality guardrail, but rejected as the primary financial goal.

---

### Candidate 2: Tier 1 Handle Time Optimization (SELECTED PRIMARY GOAL)
- **Strengths**: 
  - **Deterministic Tracking**: Derived directly from ticket timestamps and agent assignments.
  - **Direct Policy Cash Link**: Policy §8 explicitly establishes channel labor costs (Chat: ₹165/hr, Email: ₹195/hr, Voice: ₹240/hr, Social: ₹150/hr). Every hour of agent handle time has an exact, audited rupee cost.
  - **Directly Trainable**: Frontline handle time disparities stem from navigation friction, template under-utilization, and troubleshooting hesitations—classic competencies directly remediated by standard operating procedure (SOP) training.
  - **Peer-Stratified Benchmarking**: Prevents the unfairness of comparing Tier 1 frontline agents to Tier 2 escalation specialists.
- **Quantitative Opportunity**:
  - **Frontline Team Median Benchmark**: Bringing above-median Chat (15 agents) and Email (7 agents) frontline agents to their peer median saves **650.8 agent-hours per quarter**, representing **₹1,07,379 per quarter (~₹1.07 Lakhs/quarter)**.
  - **Tier 1 Upper-Quartile (25th Percentile) Benchmark**: Across all 38 Tier 1 agents, closing the gap to the 25th percentile peer efficiency recovers **2,262.2 agent-hours per quarter**, representing **₹3,73,266 per quarter (~₹3.73 Lakhs/quarter)**. This matches the client's ₹4,00,000 Q3 training budget within 93.3% capital efficiency.
- **Verdict**: **Selected as the Primary Business Goal**.

---

### Candidate 3: First-Response SLA Breach Reduction
- **Strengths**: Direct policy cost: ₹350 store credit per breach under Policy §3.
- **Critical Flaw**: **Insufficient Economic Scale**. Across 18 months, only 1,064 SLA breaches occurred across all channels combined, generating ₹3,72,400 in total credits. This represents an average quarterly exposure of only **₹62,067 per quarter**.
- **Economic Defensibility**: Even if training miraculously eliminated 100% of all SLA breaches across the company, the quarterly savings of ₹62K would take nearly 7 quarters just to break even on a ₹4,00,000 training program.
- **Verdict**: Rejected as primary goal due to inadequate financial scale.

---

### Candidate 4: Inter-Tier Transfer Reduction
- **Strengths**: Direct policy fee: ₹305 per transfer under Policy §6.
- **Critical Flaw**: **Insufficient Economic Scale**. Across 18 months, 1,215 tickets were transferred between tiers, totaling ₹3,70,575 (~**₹61,763 per quarter**).
- **Economic Defensibility**: A realistic 25% reduction in avoidable transfers yields only ~₹15,440 per quarter in savings.
- **Verdict**: Rejected as primary goal; retained as a secondary training curriculum topic.

---

### Candidate 5: Repeat Contact Avoidance / First Contact Resolution (FCR)
- **Strengths**:
  - Under Policy §10, 3,277 tickets represent repeat contacts within 30 days by the same customer, totaling **₹9,03,890** in channel labor handling costs (₹1,50,648 per quarter).
  - 2,572 tickets represent repeat contacts by the same customer regarding the *exact same product SKU*, consuming **₹7,10,140** in labor costs (₹1,18,357 per quarter).
- **Economic Defensibility**: Highly trainable and directly converts to labor capacity savings at policy rates.
- **Verdict**: Selected as the **Primary Complementary / Supporting Goal**.

---

### Candidate 6: Warranty Replacements / RMA Rate (Pulse 2)
- **Strengths**: Huge financial volume: 1,896 replacements totaling ₹34,15,990 (Pulse 2 alone accounts for 1,166 replacements and ₹22.39 Lakhs).
- **CRITICAL FLAWS (WHY THIS MUST BE REJECTED FOR SUPPORT TRAINING)**:
  1. **Root Cause is a Factory Defect**: Lot analysis proves that batch `PL2-2510-3` accounts for 730 out of 1,166 Pulse 2 replacements (62.6%). Customer messages and agent notes confirm physical charging pin corrosion and socket failure. Support agents do not manufacture earbuds; training support agents cannot fix defective hardware.
  2. **Violates Support Policy & Customer Trust**: Support agents are strictly mandated under Policy §4 to authorize replacements for legitimate hardware defects within the 1-year warranty. Claiming that support training will reduce replacements implies training agents to reject valid warranty claims, directly violating policy and destroying customer goodwill.
  3. **Technical Interview Failure**: Defending replacement reduction as a support training achievement would immediately disqualify an engineer in a technical interview due to false causal attribution.
- **Verdict**: **Strictly Rejected as a Support Training Goal**. Must be escalated as a Priority 1 Vendor/Operations Defect.

---

### Candidate 7: Agent Note Quality & IVR Cleanup
- **Strengths**: 31.4% of tickets contain uninformative agent notes; 40 tickets contain corrupt phone system IVR transcripts.
- **Critical Flaw**: IVR corruption is a telephony gateway bug, not an agent training issue. Note quality is a process hygiene metric with no direct policy rupee conversion.
- **Verdict**: Retained as a curriculum requirement in the training modules, but rejected as the business KPI.

---

## 4. Final Strategic Recommendation

The data and policy structure lead to a clear, unambiguous conclusion:
- **Primary Business Goal**: **Tier 1 Handle Time Optimization** toward peer-group benchmarks, saving **₹1,07,379/quarter** (team median benchmark) to **₹3,73,266/quarter** (25th percentile benchmark) in recoverable frontline support capacity.
- **Operational Alignment**: Directly justifies the ₹4,00,000 Q3 training budget by recovering up to ₹3.73L/quarter in ongoing operational labor capacity.
- **Secondary Quality Guardrails**: CSAT floor (>3.33) and SLA breach cap (<9.06%) to ensure efficiency gains do not compromise service quality.
- **Cross-Functional Escalation**: Formal referral of Pulse 2 batch `PL2-2510-3` to Hardware Engineering and Supply Chain to address the ₹22.39L warranty drain at the true root cause.
