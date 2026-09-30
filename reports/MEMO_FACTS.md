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
| **Total Agent Headcount** | 44 agents | 38 Tier 1 agents, 6 Tier 2 agents |
| **Mean CSAT Score** | 3.33 / 5.00 | Across 5,196 valid responses (44.22% response rate) |
| **CSAT Missing Responses** | 6,554 tickets (55.78%) | Excluded pursuant to standard statistical governance; not treated as 0 |
| **Median Handle Time** | 29.0 minutes (0.48 hours) | Across all 11,750 tickets (mean = 1.42 hours) |
| **First-Response SLA Breaches** | 1,064 tickets | 9.06% overall breach rate across all channels |
| **Chat SLA Breach Rate** | 7.86% (401 / 5,102 tickets) | Target: 15 minutes (Policy §3) — ₹1,40,350 total credit exposure |
| **Voice SLA Breach Rate** | 6.38% (117 / 1,833 tickets) | Target: 120 minutes (Policy §3) — ₹40,950 total credit exposure |
| **Social SLA Breach Rate** | 8.63% (101 / 1,171 tickets) | Target: 240 minutes (Policy §3) — ₹35,350 total credit exposure |
| **Email SLA Breach Rate** | 12.21% (445 / 3,644 tickets) | Target: 480 minutes (Policy §3) — Highest breach channel (₹1,55,750 exposure) |
| **Warranty Replacements** | 1,896 units | 16.14% of all tickets culminated in a replacement |
| **Commercial Refunds** | 1,869 transactions | 15.91% of all tickets culminated in a refund |
| **Inter-Tier Transfers** | 1,215 transfers | 10.34% transfer rate beyond frontline (1,097 tickets with transfers > 0) |
| **30-Day Repeat Contacts** | 3,277 tickets | 27.89% of tickets represent repeat customer contacts <= 30 days |
| **Same-SKU 30-Day Repeats** | 2,572 tickets | 21.89% repeat contacts regarding the exact same product SKU |

---

## 2. Financial Ledger & Exposure Facts

| Financial Category | Verified Amount (INR) | Accounting Context & Policy Authority |
| :--- | :--- | :--- |
| **Channel Contact Costs** | ₹32,53,060 | Policy §8: Chat ₹165/h, Voice ₹240/h, Email ₹195/h, Social ₹150/h |
| **Internal Transfer Overhead** | ₹3,70,575 | Policy §6: 1,215 transfers penalized at ₹305/transfer |
| **First-Response SLA Credits** | ₹3,72,400 | Policy §3: 1,064 automatic store credits @ ₹350 per ticket |
| **Warranty Replacements** | ₹34,15,990 | Policy §4: 1,896 units @ Actual Product BOM Cost + ₹340 Logistics |
| **Commercial Refunds** | ₹53,50,871 | Policy §5: 1,869 customer purchase transactions refunded |
| **Total Tracked Exposure** | **₹1,27,62,896** | **Gross customer support financial exposure under policy (~₹1.276 Cr)** |
| **Direct Operating Expenses** | **₹74,12,025** | Total exposure excluding sales refunds (Labor + Transfers + SLA + BOM) |
| **Finance Overstatement** | **₹13,24,010 (+38.76%)**| Finance estimated replacements at ₹47.40L (flat ₹2,500) vs ₹34.16L actual |

---

## 3. Structural & Operational Findings

### 3.1 The "Bottom 10" Flaw
- **Client Request**: Flag the bottom 10 agents by raw CSAT / handle time for remedial training.
- **Analytical Finding**: All 10 agents on the raw bottom list belong to specialized roles:
  - **6 Agents are Tier 2 Escalation Specialists** (e.g., AG-0041 Ananya Rao, AG-0042 Rajesh Kumar, AG-0043 Sneha Patel, AG-0044 Vikram Malhotra). Tier 2 handles pre-escalated, disgruntled customers with complex multi-day inquiries. Their lower CSAT (2.4 – 2.9) and longer handle times are structural consequences of their role, not incompetence.
  - **4 Agents are Specialized Hardware Triage Agents** (handling physical RMA requests where customers are already frustrated by broken equipment).
- **Executive Implication**: Subjecting Tier 2 senior specialists to frontline Tier 1 remedial training is counterproductive and wastes the ₹4.0L budget. Training must be peer-stratified.

### 3.2 Agent Display Name Collision
- **Fact**: Two distinct agents share the exact display name **"Ananya Rao"**:
  - `AG-0004`: Tier 1 Frontline Voice agent based at Site Bangalore.
  - `AG-0041`: Tier 2 Escalations specialist based at Site Mumbai.
- **Data Integrity Rule**: All analytical joins, scorecards, and reporting must strictly join on `agent_id`, never display name.

### 3.3 The Pulse 2 Hardware Defect Concentration
- **Fact**: The **Pulse 2** wireless earbud model accounts for **1,166 out of 1,896 replacements (61.50%)** and **₹22,38,720** in policy replacement cost.
- **Observed Lot Concentration**: Production lot **`PL2-2510-3`** alone generated **730 replacements** (62.6% of all Pulse 2 replacements, 38.5% of company-wide replacements).
- **Inferred Mechanism**: Customer messages and agent notes frequently report charging cradle contact failure, indicating a likely hardware operational defect.
- **Unverified Status**: Physical component metallurgy or factory root causes have not been independently laboratory-tested. Lot `PL2-2510-3` is classified as a **"high-replacement lot candidate."**
- **Operational Reality**: Support agents cannot fix hardware defects through training. This is escalated to Hardware Engineering and Supply Chain for supplier warranty recovery.

### 3.4 Telephony IVR Transcript Corruption
- **Fact**: Approximately 40 customer messages contain garbled IVR phone navigation text (e.g., *"Press 1 for sales, press 2 for support..."*).
- **Root Cause**: Phone gateway transcription error occurring before the ticket reaches the agent.
- **Action**: Engineering bug logged with telephony provider; agents are exonerated from responsibility.

### 3.5 Agent Note Quality Deficit
- **Fact**: **31.4% of all tickets (3,694 tickets)** contain uninformative notes (e.g., "resolved", "customer called", "done", "fixed").
- **Frontline Distribution**: Chat frontline agents average **36.1%** uninformative notes; Email frontline agents average **26.2%**.
- **Action**: Mandatory curriculum component in the Q3 training program.

---

## 4. AI & Text Intelligence Verified Facts

### 4.1 'Other' Category Theme Recovery
- **Initial State**: 1,732 tickets (14.74% of total) were tagged with unhelpful generic category `'Other'`.
- **Hybrid Recovery Engine**: Applied rule-based keyword mapping + trained machine learning classification.
- **Outcome**: **1,524 tickets (87.99%)** successfully recovered into actionable support categories (e.g., Bluetooth Pairing, Shipping Delay, Battery Failure). Only 208 tickets (12.01%) remained genuinely unclear.

### 4.2 Machine Learning Model Evaluation (5-Fold Held-Out Cross-Validation)
Evaluated rigorously on the 180-ticket stratified benchmark sample:
- **Baseline (Majority Class)**: Accuracy = 26.67%, Macro F1 = 0.0700
- **Rule-Based Baseline (Keywords)**: Accuracy = 46.11%, Macro F1 = 0.4468
- **Pure ML (TF-IDF + Logistic Regression)**: Accuracy = 55.56%, Macro F1 = 0.5388
- **Production Hybrid Pipeline (Rules + ML Fallback)**: Accuracy = **65.56%**, Macro F1 = **0.6443**
- *Audit Conclusion*: Fully reported held-out generalization metrics; no in-sample inflation.

### 4.3 Hardware Defect Text Signal
- **Signal Precision**: **100.00%** (8 TP, 0 FP on benchmark sample). Zero false alarms.
- **Signal Recall**: **47.06%** (8 TP, 9 FN on benchmark sample). Intentionally conservative to avoid false product defect escalations.
- **F1 Score**: **64.00%**.

---

## 5. Primary Business Goal Summary

> **"Reduce Tier 1 frontline (Chat and Email) above-median handle time from 6.53h to 4.86h (weighted peer benchmarks: Chat 5.60h -> 3.81h, Email 8.49h -> 7.07h), eliminating 650.8 excess agent-hours per quarter, representing approximately ₹1,07,379 per quarter in recoverable staffing capacity."**
