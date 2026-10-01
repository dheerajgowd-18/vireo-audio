# Executive Memo Facts & Source-of-Truth Reference

**Audit Period**: January 1, 2024 – June 30, 2025 (18 Months / 6 Quarters)  
**Dataset Scale**: 11,750 Tickets, 44 Support Agents, 15,500 Orders, 9,500 Customers, 14 Product SKUs  
**Author**: Lead Data & AI Engineer  
**Purpose**: Verified factual foundation for executive communication and board briefing  

---

## 1. Core Operating & Support Performance Facts

| Metric / Dimension | Verified Value | Evidence / Context |
| :--- | :--- | :--- |
| **Total Ticket Volume** | 11,750 tickets | Complete census across 18 operating months |
| **Valid Handle-Time Tickets** | 11,183 tickets | Attendance tickets (resolved/closed) with handle_time >= 0 |
| **Total Agent Headcount** | 44 agents | 38 Tier 1 agents, 6 Tier 2 agents |
| **Mean CSAT Score** | 3.33 / 5.00 | Across 5,196 valid responses (44.22% response rate) under Policy §8 |
| **CSAT Missing Responses** | 6,554 tickets (55.78%) | Excluded pursuant to Policy §8; not treated as 0 |
| **Median Handle Time** | 29.0 minutes (0.48 hours) | Across all 11,750 tickets (mean = 1.42 hours) |
| **First-Response SLA Breaches** | 1,064 tickets | 9.06% overall breach rate across all channels under Policy §3 |
| **Chat SLA Breach Rate** | 7.86% (401 / 5,102 tickets) | Target: 15 minutes (Policy §3) — ₹1,40,350 total credit exposure |
| **Voice SLA Breach Rate** | 6.38% (117 / 1,833 tickets) | Target: 120 minutes (Policy §3) — ₹40,950 total credit exposure |
| **Social SLA Breach Rate** | 8.63% (101 / 1,171 tickets) | Target: 240 minutes (Policy §3) — ₹35,350 total credit exposure |
| **Email SLA Breach Rate** | 12.21% (445 / 3,644 tickets) | Target: 480 minutes (Policy §3) — Highest breach channel (₹1,55,750 exposure) |
| **Warranty Replacements** | 1,896 units | 16.14% of all tickets culminated in a replacement under Policy §5 |
| **Commercial Refunds** | 1,869 transactions | 15.91% of all tickets culminated in a refund under Policy §5 |
| **Inter-Tier Transfers** | 1,215 transfers | 10.34% transfer rate beyond frontline (1,097 tickets with transfers > 0) |
| **30-Day Repeat Contacts** | 3,277 tickets | 27.89% of tickets represent repeat customer contacts <= 30 days under Policy §10 |
| **Same-SKU 30-Day Repeats** | 2,572 tickets | 21.89% repeat contacts regarding the exact same product SKU |

---

## 2. Financial Ledger & Exposure Facts

| Financial Category | Verified Amount (INR) | Accounting Context & Policy Authority |
| :--- | :--- | :--- |
| **Channel Contact Costs** | ₹32,53,060 | Policy §4: Chat ₹210, Voice ₹520, Email ₹260, Social ₹240 / contact (or labor) |
| **Internal Transfer Overhead** | ₹3,70,575 | Policy §4: 1,215 transfers penalized at ₹305/transfer |
| **First-Response SLA Credits** | ₹3,72,400 | Policy §3: 1,064 automatic store credits @ ₹350 per ticket |
| **Warranty Replacements** | ₹34,15,990 | Policy §5: 1,896 units @ Actual Product BOM Cost + ₹340 Logistics |
| **Customer Refunds** | ₹53,50,871 | Policy §5: 1,869 customer purchase transactions refunded |
| **Total Tracked Exposure** | **₹1,27,62,896** | **Gross customer support financial exposure under policy (~₹1.276 Cr)** |
| **Direct Operating Expenses** | **₹74,12,025** | Total exposure excluding sales refunds (Labor + Transfers + SLA + BOM) |
| **Finance Overstatement** | **₹13,24,010 (+38.76%)**| Finance estimated replacements at ₹47.40L (flat ₹2,500) vs ₹34.16L actual |

---

## 3. Structural & Operational Findings

### 3.1 The "Bottom 10" Flaw
- **Client Request**: Flag the bottom 10 agents by raw CSAT / handle time for remedial training.
- **Analytical Finding**: All 10 agents on the raw bottom list belong to specialized roles:
  - **6 Agents are Tier 2 Escalation Specialists** (A3041 Jaspreet Desai, A3042 Sneha Sethi, A3040 Tarun Fernandes, A3044 Pranav Khanna, A3043 Kabir Varghese, A3039 Sameer Ghosh). Tier 2 handles pre-escalated, disgruntled customers with complex multi-day inquiries. Their lower CSAT (2.42 – 2.83) and longer handle times are structural consequences of their role, not incompetence.
  - **4 Agents are Specialized Hardware Triage Agents** (A3004 Siddharth Kapoor, A3006 Kavya Pandey, A3007 Siddharth Trivedi, A3005 Zaid Khanna — "Kavya's four" rota handling physical RMA requests where customers are already frustrated by broken equipment).
- **Executive Implication**: Subjecting Tier 2 senior specialists to frontline Tier 1 remedial training is counterproductive and wastes the ₹4.0L budget. Training must be peer-stratified.

### 3.2 Agent Display Name Collision
- **Fact**: Two distinct agents share the exact display name **"Kavya Pandey"**:
  - `A3006`: Tier 1 Chat Frontline agent based at Site Indore.
  - `A3029`: Tier 1 Logistics agent based at Site Bengaluru.
- **Data Integrity Rule**: All analytical joins, scorecards, and reporting must strictly join on `agent_id`, never display name.

### 3.3 The Pulse 2 Hardware Replacement Concentration
- **Fact**: The **Pulse 2** wireless earbud model accounts for **1,166 out of 1,896 replacements (61.50%)** and **₹21,22,120.00** in policy replacement spend (1,166 $\times$ [₹1,480 + ₹340 = ₹1,820]).
- **Observed Lot Concentration**: Production lot **`PL2-2510-3`** generated **70 replacements** across 171 tickets on direct `order_id` join (40.94% replacement rate, ₹1,27,400 spend).
- **Inferred Mechanism**: Customer messages and agent notes frequently report charging cradle contact failure, indicating a likely hardware operational defect.
- **Unverified Status**: Physical component metallurgy or factory root causes have not been independently laboratory-tested. Lot `PL2-2510-3` is classified as a **"high-replacement lot candidate."**
- **Operational Reality**: Support agents cannot fix hardware defects through training. This is escalated to Hardware Engineering and Supply Chain for vendor warranty recovery.

### 3.4 Telephony IVR Transcript Corruption
- **Fact**: Approximately 40 customer messages contain garbled IVR phone navigation text (e.g., *"Press 1 for sales, press 2 for support..."*).
- **Root Cause**: Phone gateway transcription error occurring before the ticket reaches the agent.
- **Action**: Engineering bug logged with telephony provider; agents are exonerated from responsibility.

### 3.5 Agent Note Quality Deficit
- **Fact**: **908 tickets (7.73% of 11,750)** contain uninformative shorthand notes (`words <= 2 OR characters <= 9`, e.g., `-`, `done`, `cx ok`, `sorted`, `see prev`). Appending `[closed]` or initials expands this to 1,064 tickets (9.06%).
- **Correction Note**: Prior unverified claims citing 31.4% / 3,694 tickets lacked reproducible code and are formally retired.
- **Action**: Mandatory curriculum component in the Q3 training program.

---

## 4. Primary Business Goal Summary

> **"Reduce Tier 1 frontline (Chat and Email) above-median handle time from 6.54h to 4.86h (weighted peer medians: Chat 5.61h -> 3.81h, Email 8.49h -> 7.07h), eliminating 624.9 excess agent-hours per quarter, representing approximately ₹1,03,102 per quarter in recoverable staffing capacity."**
