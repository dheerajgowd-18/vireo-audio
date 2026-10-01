# Vireo Audio Support Intelligence — Screen Recording Script
## Client Evaluation Video Walkthrough (Strict 3:00 Duration)

**Format:** Live Software Walkthrough & Screen Capture (No slide decks, no static presentations)  
**Total Target Runtime:** Exactly 3 Minutes (180 Seconds)  
**Presenter:** Candidate / Lead Data & AI Engineer  
**Live UI URL:** `http://localhost:8000`  

---

### [0:00 – 0:25] Opening: Problem Context & Primary Business Goal

* **Visual on Screen:**  
  Start on the live dashboard at `http://localhost:8000#overview`. Show the top KPI strip (`11,750 Tickets`, `44 Agents`, `3.33 CSAT`, `9.06% SLA Breaches`, `₹1.28 Cr Financial Exposure`) and the primary business goal card.
* **Spoken Script (Voiceover):**  
  > "Hello Priya and the evaluation committee. Today, I'm presenting the Vireo Audio Support Intelligence Platform.
  > 
  > When leadership asked how to deploy the ₹4,00,000 Q3 support training budget, initial discussions focused on penalizing the raw 'Bottom 10' agents and addressing surging replacement costs. 
  > 
  > Our data audit proved that both instincts were misdiagnosed. 
  > 
  > Instead, our analytical engine establishes our primary business goal:
  > **'Reduce Tier 1 frontline Chat and Email above-median handle time from 6.54 hours to 4.86 hours, eliminating 624.9 excess agent-hours per quarter, representing approximately ₹1.03 lakh per quarter in modeled recoverable staffing capacity.'**
  > 
  > Over four quarters, this unlocks ₹4.12 lakhs in annualized modeled capacity value under Policy Section 4, while monitoring CSAT alongside efficiency gains to avoid deterioration in our 3.33 historical baseline."

---

### [0:25 – 0:55] The "Bottom 10" Fallacy & Peer-Stratified Scorecards

* **Visual on Screen:**  
  Click on **"Requested Bottom 10"** in the sidebar (`#bottom10`). Highlight the warning banner explaining structural tier differences. Hover over `A3041 Jaspreet Desai` (CSAT 2.42) and `A3004 Siddharth Kapoor` (CSAT 2.98). Then click **"Agent Performance"** (`#agents`) and filter by `Tier 1 - Chat Frontline`.
* **Spoken Script (Voiceover):**  
  > "First, let's examine the requested 'Bottom 10' list. 
  > 
  > A naive company-wide sort by CSAT shows agents with scores between 2.4 and 3.0. But look at their roles: six of these ten are Tier 2 Escalation specialists handling multi-day, pre-escalated customer disputes where CSAT is structurally low. The other four are frontline agents assigned to the high-friction hardware RMA triage rota.
  > 
  > Retraining Tier 2 senior specialists on frontline basics would waste budget and degrade morale.
  > 
  > In our Agent Performance view, we benchmark agents strictly within their operational peers. When we filter for Tier 1 Chat, we isolate the real operational opportunity: 7 agents operating above their peer median of 3.81 hours, consuming excess hours due to ticket aging rather than lack of effort."

---

### [0:55 – 1:25] AI Signals: Local NLP, Cross-Validation, & Recovering "Other"

* **Visual on Screen:**  
  Click on **"AI Signals"** (`#ai`). Show the Issue Category breakdown chart, scroll to the **"Recovery of 'Other' Category"** section, and highlight the **Model Evaluation Card** showing 5-fold cross-validation metrics.
* **Spoken Script (Voiceover):**  
  > "Next, let's look at our AI text layer. 
  > 
  > Rather than spending on external cloud APIs across 11,750 tickets, we engineered a local scikit-learn TF-IDF and Logistic Regression pipeline. It ran across the entire dataset in 3.8 seconds at zero paid model cost.
  > 
  > In the intake data, 1,732 tickets—nearly 15%—were dumped into an unhelpful 'Other' category. Our model recovered 87.99% of them into actionable operational categories like delivery, connectivity, and billing.
  > 
  > Crucially, we maintain engineering honesty: while in-sample alignment reached 98%, our held-out 5-fold cross-validation proves a true generalization accuracy of 55.56% and a macro F1 of 0.5388—more than double the majority baseline. Our hardware defect detector operates with 100% precision and zero false positives, ensuring no unauthorized replacements are triggered."

---

### [1:25 – 1:55] Replacements & The Pulse 2 Hardware Quality Finding

* **Visual on Screen:**  
  Click on **"Replacements"** (`#replacements`). Point to the Pulse 2 metric card (`1,166 replacements`, `₹21.22L policy spend`, `61.50% share`). Scroll down to the **Manufacturing Lot Code Analysis** table and highlight lot **`PL2-2510-3`** (40.94% replacement rate).
* **Spoken Script (Voiceover):**  
  > "Now turning to warranty replacements. 
  > 
  > Finance estimated replacement costs at a flat ₹2,500 per unit, projecting ₹47.4 lakhs. Under Policy Section 5—actual product BOM plus ₹340 logistics—the real spend was ₹34.16 lakhs, revealing a ₹13.24 lakh finance overstatement.
  > 
  > More importantly, our product breakdown reveals that a single product—the Pulse 2 wireless earbuds—drives 61.5% of all replacements, totaling ₹21.22 lakhs.
  > 
  > When we trace lot codes from orders, production lot candidate `PL2-2510-3` shows an alarming 40.94% replacement rate, with text signatures consistently reporting charging pin contact failure. 
  > 
  > Support training cannot fix physical hardware issues. We formally escalate this operational signal to Hardware Engineering and Supply Chain for investigation."

---

### [1:55 – 2:25] SLA, Financial Ledger, & Note Standardization

* **Visual on Screen:**  
  Click on **"SLA & Cost"** (`#sla`). Point to the channel breach rates (Email at 12.21%, Chat at 7.86%) and the financial exposure ledger. Then click on an agent in the table to open the **Agent Detail Drawer**.
* **Spoken Script (Voiceover):**  
  > "In the SLA & Cost view, we track total operating exposure of ₹1.28 Crore, including ₹3.72 lakhs in SLA breach credits across 1,064 breaches. Email is our most vulnerable channel with a 12.21% breach rate under Policy Section 3.
  > 
  > Opening the agent detail drawer, leadership can inspect an agent's peer standing, contact history, and defect exposure.
  > 
  > Here we also see why handle times inflate: 908 tickets contain uninformative shorthand notes like '-' or 'done'. Standardizing diagnostic notes in our training curriculum directly prevents duplicate discovery cycles when tickets are transferred."

---

### [2:25 – 3:00] Training Recommendations & Closing

* **Visual on Screen:**  
  Click on **"Methodology"** (`#methodology`). Scroll to the **Q3 Training Budget Allocation** section showing the three frontline curricula. Finish on the top header showing full system integrity.
* **Spoken Script (Voiceover):**  
  > "To summarize our recommendations for Priya and leadership:
  > 
  > 1. Use the ₹4.0 lakh training budget for peer-benchmarked Tier 1 workflow and troubleshooting training across our 22 frontline Chat and Email agents: Diagnostic SOPs, First-Contact Resolution protocols, and Queue Management Sweeps.
  > 2. Exempt Tier 2 specialists and hardware triage agents from remedial lists, benchmarking them strictly against peers.
  > 3. Escalate the ₹21.22 lakh Pulse 2 replacement finding and lot `PL2-2510-3` to Hardware Engineering as an operational investigation signal.
  > 
  > This gives Vireo Audio an auditable, peer-stratified, and mathematically defensible roadmap to elevate customer experience while preserving operational capital.
  > 
  > Thank you."

---

### Presenter Checklist Before Recording:
* [ ] Local server running: `python -m http.server 8000 --directory web`
* [ ] Browser window sized to 1920x1080 (100% zoom)
* [ ] Audio microphone checked and clear
* [ ] Stop timer set for 3 minutes (180 seconds)
