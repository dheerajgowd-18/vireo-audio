# Final Business Case: Tier 1 Frontline Handle Time Optimization

**Target Investment**: ₹4,00,000 Q3 Support Training Budget  
**Evaluation Scope**: 11,750 Support Tickets, 44 Agents, 18 Months (Jan 2025 – Jun 2026)  
**Author**: Lead Data & AI Engineer  
**Status**: Formally Reconciled & Audited  

---

## 1. Primary Business Goal Statement

The primary business goal for Vireo Audio's Q3 support training initiative is formally defined as:

> ### Primary Operational Goal:
> **"Reduce Tier 1 frontline (Chat and Email) above-median handle time from 6.54h to 4.86h (weighted peer medians: Chat 5.61h -> 3.81h, Email 8.49h -> 7.07h), eliminating 624.9 excess agent-hours per quarter, representing approximately ₹1,03,102 per quarter in recoverable staffing capacity."**

> ### Full Tier 1 Program Benchmark (Upper-Bound Potential Across Tier 1):
> **"Reduce Tier 1 handle time across above-p25 agents toward the 25th percentile peer efficiency benchmark, eliminating 2,154.4 excess agent-hours per quarter, representing approximately ₹3,55,481 per quarter (~₹3.55 Lakhs/quarter) in ongoing operational labor capacity."**

---

## 2. One-Paragraph Executive Briefing for Priya (Customer Experience Lead)

> "Priya, our quantitative audit shows that targeting the ₹4,00,000 training budget strictly at the raw 'Bottom 10' list does not account for operational queue differences, as 6 of those 10 are Tier 2 specialists handling complex escalations and 4 are specialized hardware triage agents. These agents handle structurally different work populations; their raw scores therefore should not be interpreted without operational context. Policy §6 explicitly distinguishes Tier 2 work from Tier 1 on workload and measurement characteristics. Furthermore, the ₹21.22L spent replacing Pulse 2 earbuds is heavily concentrated in high-replacement lot candidate `PL2-2510-3` (70 replacements; 40.94% replacement rate with observed charging-contact failure text patterns)—an operational hardware signal that support training cannot solve. Instead, the highest-return investment of your ₹4.0L budget is peer-benchmarked workflow and troubleshooting coaching for your 22 frontline Chat and Email agents. Currently, the 10 above-median agents in these channels average 6.54 hours per ticket across 2,237 valid completed tickets, consuming 624.9 excess hours per quarter above their team peer medians. By coaching these agents to their respective team medians (Chat 5.61h to 3.81h; Email 8.49h to 7.07h), we reduce their average handle time to 4.86 hours, releasing **₹1,03,102 per quarter in modeled recoverable staffing capacity** (~₹4.12 Lakhs annualized modeled capacity value under Policy §4 at ₹165/hour), while monitoring CSAT alongside efficiency gains to avoid deterioration in our historical baseline (3.33 overall mean)."

---

## 3. Mathematical & Data Derivation

### 3.1 Benchmark Definition & Methodology
- **Valid Ticket Population**: Handle-time calculations are evaluated strictly on **11,183 valid attendance tickets** (`status in {resolved, closed}`, `first_response_dt` present, `resolved_at_reporting` present, and `handle_time_hours >= 0`). Open and pending tickets (567 tickets) lack resolution timestamps and are strictly excluded from handle-time multipliers.
- **Benchmark Definition (Interpretation A)**: For each team, the benchmark is the median of agent-level mean handle times. An agent is defined as "above-median" if their individual mean handle time on valid tickets exceeds this team median.
- **Nature of Financial Conversion**: Policy §4 defines fully loaded agent labor for staffing decisions at **₹165 per agent-hour**. The resulting ₹1,03,102 per quarter represents **recoverable staffing capacity value** (operational capacity to absorb growing ticket volume without adding headcount), rather than direct cash payroll cuts.

### 3.2 Chat Frontline Derivation (15 Agents, Tier 1)
- **Cohort Ticket Volume**: 3,474 total tickets; **3,314 valid completed tickets**.
- **Cohort Mean Handle Time**: 4.38 hours (mean of agent means).
- **Team Benchmark (Median of Agent Means)**: **3.8128 hours (~3.81h)**.
- **Above-Median Cohort**: 7 agents (A3003, A3006, A3007, A3011, A3012, A3014, A3015) handling **1,519 valid completed tickets**.
- **Current Weighted Mean of Above-Median Agents**: **5.6108 hours (~5.61h)** (unweighted agent mean = 5.79h).
- **Proposed Target**: Team median of **3.8128 hours** (-1.798 hours per ticket).
- **Excess Agent-Hours Over 18 Months**:
  $$\text{Current Hours} (8,522.83\text{h}) - \text{Target Hours} (1,519 \times 3.8128 = 5,791.66\text{h}) = \mathbf{2,731.18 \text{ hours}}$$
- **Quarterly Run-Rate**: $2,731.18 \text{ hours} \div 6 \text{ quarters} = \mathbf{455.20 \text{ hours/quarter}}$.
- **Quarterly Capacity Value (@ ₹165/hr)**:
  $$455.20 \text{ hrs} \times ₹165/\text{hr} = \mathbf{₹75,107.40 \text{ per quarter}}$$

### 3.3 Email Frontline Derivation (7 Agents, Tier 1)
- **Cohort Ticket Volume**: 1,670 total tickets; **1,592 valid completed tickets**.
- **Cohort Mean Handle Time**: 6.70 hours (mean of agent means). Note that two fast agents (3.02h, 4.26h) pull the cohort mean below the median.
- **Team Benchmark (Median of Agent Means)**: **7.0737 hours (~7.07h)**.
- **Above-Median Cohort**: 3 agents (A3018, A3020, A3021) handling **718 valid completed tickets**.
- **Current Weighted Mean of Above-Median Agents**: **8.4915 hours (~8.49h)** (unweighted agent mean = 8.48h).
- **Proposed Target**: Team median of **7.0737 hours** (-1.418 hours per ticket).
- **Excess Agent-Hours Over 18 Months**:
  $$\text{Current Hours} (6,096.88\text{h}) - \text{Target Hours} (718 \times 7.0737 = 5,078.91\text{h}) = \mathbf{1,017.97 \text{ hours}}$$
- **Quarterly Run-Rate**: $1,017.97 \text{ hours} \div 6 \text{ quarters} = \mathbf{169.66 \text{ hours/quarter}}$.
- **Quarterly Capacity Value (@ ₹165/hr)**:
  $$169.66 \text{ hrs} \times ₹165/\text{hr} = \mathbf{₹27,994.19 \text{ per quarter}}$$

### 3.4 Combined Frontline Capacity Recovery
- **Total Participating Above-Median Cohort**: 10 agents handling 2,237 valid completed tickets.
- **Current Combined Weighted Handle Time**:
  $$\frac{8,522.83 + 6,096.88}{2,237} = \frac{14,619.72}{2,237} = \mathbf{6.5354 \text{ hours (~6.54h)}}$$
- **Target Combined Weighted Handle Time**:
  $$\frac{5,791.66 + 5,078.91}{2,237} = \frac{10,870.57}{2,237} = \mathbf{4.8594 \text{ hours (~4.86h)}}$$
- **Handle Time Reduction**: **6.54h $\rightarrow$ 4.86h** (-1.68 hours per ticket).
- **Total Excess Hours (18 Months)**: $2,731.18 + 1,017.97 = \mathbf{3,749.15 \text{ hours}}$.
- **Quarterly Hours Saved**: $3,749.15 \div 6 = \mathbf{624.86 \text{ hours/quarter}}$.
- **Direct Capacity Value (@ ₹165/hr)**:
  $$624.8581 \text{ hrs} \times ₹165/\text{hr} = \mathbf{₹1,03,101.59 \text{ per quarter (~₹1.03L/quarter)}}$$
- **Annualized Capacity Value**: **₹4,12,406 per year** in recoverable operational support capacity.

---

## 4. All Tier 1 Teams Benchmark Audit Table

Evaluation of all Tier 1 teams (using valid handle-time tickets only):

| Team Name | Tier | Total Agents | Valid Tickets | Team Median AHT | Above-Median Agents | Valid Tickets in Cohort | 18-Mo Excess Hours | Quarterly Excess Hours | Quarterly Value @ ₹165/hr |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Chat Frontline** | 1 | 15 | 3,314 | 3.81h | 7 | 1,519 | 2,731.18h | 455.20h | **₹75,107.40** |
| **Email Frontline** | 1 | 7 | 1,592 | 7.07h | 3 | 718 | 1,017.97h | 169.66h | **₹27,994.19** |
| **Billing** | 1 | 4 | 1,407 | 4.25h | 2 | 726 | 502.01h | 83.67h | ₹13,805.14 |
| **Logistics** | 1 | 5 | 1,803 | 41.08h | 2 | 740 | 512.96h | 85.49h | ₹14,106.35 |
| **Returns Desk** | 1 | 3 | 1,055 | 35.63h | 1 | 542 | 483.79h | 80.63h | ₹13,304.25 |
| **Voice Frontline** | 1 | 4 | 764 | 3.63h | 2 | 575 | 77.33h | 12.89h | ₹2,126.69 |
| **Total Tier 1 (Median)** | **1** | **38** | **9,935** | — | **17** | **4,820** | **5,325.24h** | **887.54h** | **₹1,46,444.10** |
| **Total Tier 1 (p25 Stretch)** | **1** | **38** | **9,935** | — | **28** | **7,087** | **12,926.57h** | **2,154.43h** | **₹3,55,480.68** |

### Why Focus on Chat + Email Frontline as the Primary Case:
1. **Direct Digital Controllability**: Chat and Email handle times reflect direct digital agent activities (typing, CRM navigation, macro lookup, diagnostic questioning). In contrast, Logistics (median 41.08h) and Returns Desk (median 35.63h) are structurally dominated by multi-day courier transit and warehouse inspection, which agents cannot influence via training.
2. **Volume & Excess Concentration**: Chat and Email account for **3,749.15 out of 5,325.24 excess hours (70.4%)** across all Tier 1 teams.

---

## 5. Three Key Secondary Operational Findings

### Finding 1: High-Replacement Lot Candidate `PL2-2510-3` (Pulse 2 Concentration)
- **Product Reconciliation**: Pulse 2 wireless earbuds account for **1,166 of 1,896 replacements (61.50%)** and **₹21,22,120.00** in policy replacement spend (1,166 units $\times$ [₹1,480 BOM + ₹340 logistics = ₹1,820/unit] under Policy §5).
- **Candidate Lot Concentration**: Production lot **`PL2-2510-3`** generated **70 replacements** across 171 tickets on direct `order_id` join (40.94% replacement rate, ₹1,27,400 spend).
- **Defensibility Note**: Customer and agent notes describe charging pin contact failure. This is an operational hardware issue, not a support agent training deficiency. It is escalated to Hardware Engineering and Supply Chain as an operational investigation signal.

### Finding 2: Email First-Response SLA Exposure (12.21% Breach Rate)
- **Audited Evidence**: Email exhibits the highest first-response breach rate of any channel at **12.21%** (445 breaches out of 3,644 eligible tickets), generating **₹1,55,750** in store credit penalties (₹25,958/quarter under Policy §3).
- **Operational Action**: Frontline email queue triage and automated SLA alert triggers should be integrated into Module 3 of the training program.

### Finding 3: Note Quality Hygiene (908 Shorthand Notes)
- **Audited Evidence**: **908 tickets (7.73% of 11,750)** contain uninformative shorthand notes (`words <= 2 OR characters <= 9`, e.g., `-`, `done`, `cx ok`, `sorted`, `see prev`). Appending `[closed]` or agent initials expands shorthand to 1,064 tickets (9.06%).
- **Historical Note**: Prior unverified claims citing 31.4% / 3,694 tickets lacked reproducible code and are formally retired.
- **Operational Action**: Note hygiene standardization is established as the core curriculum of Module 1.

---

## 6. Training Budget Allocation & Program Governance

Use the ₹4,00,000 budget for peer-benchmarked Tier 1 workflow and troubleshooting training, with final allocation determined by the intervention design and baseline needs across three core operational curricula:

1. **Module 1: Diagnostic SOPs & Note Standardization**  
   Target: All 22 frontline Tier 1 agents. Standardize diagnostic intake procedures and eliminate uninformative shorthand notes (currently 908 tickets / 7.73% of volume).
2. **Module 2: Escalation Protocols & FCR Optimization**  
   Target: All 22 frontline Tier 1 agents. Teach clear scope boundaries to resolve tier-appropriate tickets on first contact and curb unnecessary inter-tier transfers.
3. **Module 3: Tooling, Macros & Queue Management Routines**  
   Target: Focused 1-on-1 coaching for the 10 above-median agents. Implement daily sweeps of multi-day pending tickets to directly address the right-tail skew elevating average handle times.

### Targeted Population:
- **Target Cohort**: The **22 Tier 1 Frontline agents** in Chat (15) and Email (7), with individualized coaching focused on the 10 agents currently above their team peer medians.
- **Excluded Cohort**: Senior Tier 2 escalation specialists and hardware triage agents from the raw bottom 10 are **excluded from frontline remedial training**, preserving departmental morale and capital efficiency.

### Quality Guardrail:
- **CSAT Monitoring**: Individual agent performance reviews will verify that efficiency gains do not cause customer satisfaction to deteriorate, monitoring performance alongside the historical team baseline (**3.33 / 5.00**).
