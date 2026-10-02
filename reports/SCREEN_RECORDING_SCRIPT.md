# Vireo Audio Support Intelligence — Screen Recording Script
## Client Evaluation Video Walkthrough (Strict 3:00 Duration · ≤ 420 Words Spoken)

**Format:** Live Software Walkthrough & Screen Capture (No slides, live UI at `http://localhost:8000`)  
**Total Target Runtime:** Exactly 3 Minutes (180 Seconds)  
**Presenter:** Candidate / Lead Data & AI Engineer  
**Pacing:** ~135–140 words per minute (comfortably relaxed, professional delivery)  

---

### [0:00 – 0:35] Part 1: Bottom 10 Context & Primary Business Goal

* **Visual on Screen:**  
  Start on the live dashboard at `http://localhost:8000#overview`. Show the headline KPI strip (`11,750 Tickets`, `44 Agents`, `3.33 CSAT`, `₹1.28 Cr Financial Exposure`) and the primary business goal card.
* **Spoken Script (Voiceover):**  
  > "Hello Priya and committee. In reviewing Vireo's 18-month support data across 11,750 tickets, initial instincts suggested penalizing the raw 'Bottom 10' agents. Our audit proved this misdiagnoses operational reality: six are Tier 2 Escalation specialists handling multi-day disputes, and four are frontline hardware triage agents. Their raw CSAT reflects structurally complex queue assignments, not individual capability. Instead, our primary business goal focuses strictly on frontline capability: Reduce Tier 1 frontline Chat and Email above-median handle time from 6.54 to 4.86 hours, eliminating 624.9 excess agent-hours per quarter and recovering approximately ₹1.03 lakh per quarter in modeled staffing capacity under Policy Section 4."

---

### [0:35 – 1:15] Part 2: Agent Performance & Peer Benchmarks

* **Visual on Screen:**  
  Click **"Agent Performance"** (`#agents`). Filter by `Tier 1 - Chat Frontline`. Hover over median handle time vs mean handle time, then click an agent to open the **Agent Detail Drawer**.
* **Spoken Script (Voiceover):**  
  > "Under Agent Performance, we benchmark agents strictly within their operational peers, reporting medians alongside means because handle time contains a long right tail of aging tickets. Filtering for Tier 1 Chat isolates the real coaching opportunity: 7 agents operating above their peer median of 3.81 hours. Opening an agent drawer shows why: 908 tickets contain uninformative shorthand notes like 'done' or hyphens, forcing duplicate discovery cycles upon transfer. Standardizing diagnostic notes directly eliminates redundant handling hours."

---

### [1:15 – 1:55] Part 3: Warranty Replacements & Lot Quality Signal

* **Visual on Screen:**  
  Click **"Replacements"** (`#replacements`). Point to Pulse 2 metric card (`1,166 replacements`, `₹21.22L policy spend`, `61.5% share`). Scroll to the **Manufacturing Lot Code Analysis** table and highlight lot **`PL2-2510-3`** (40.94% replacement rate).
* **Spoken Script (Voiceover):**  
  > "Turning to replacements: under Policy Section 5, actual replacement spend was ₹34.16 lakhs across 1,896 units, proving Finance's flat assumption overstated liability by ₹13.24 lakhs. Crucially, Pulse 2 earbuds account for 61.5% of all replacements, totaling ₹21.22 lakhs. Production lot candidate PL2-2510-3 shows an abnormal 40.94% replacement rate with recurring charging-pin contact complaints. Support coaching cannot fix hardware defects, so we formally escalate this lot signal to Hardware Engineering."

---

### [1:55 – 2:35] Part 4: Local AI Intelligence & Recovering "Other"

* **Visual on Screen:**  
  Click **"AI Signals"** (`#ai`). Highlight the 87.99% Theme Recovery card, the horizontal theme distribution bars, and the Model Quality baseline hierarchy card.
* **Spoken Script (Voiceover):**  
  > "For ticket intelligence, we avoided external cloud APIs, deploying a local scikit-learn pipeline that classified all tickets in 3.8 seconds at zero paid model cost. Our model decomposed 87.99% of ambiguous intake 'Other' tickets into actionable operational themes like delivery and connectivity. We maintain engineering transparency: held-out 5-fold cross-validation achieves 55.56% generalization accuracy—more than double the majority baseline—against benchmark pseudo-labels, while our hardware detector provides a conservative zero-false-alarm text signal."

---

### [2:35 – 3:00] Part 5: Methodology Caveat & Q3 Recommendation

* **Visual on Screen:**  
  Click **"Methodology"** (`#methodology`). Show the data integrity checks, then finish on the **Q3 Training Deployment** recommendation table.
* **Spoken Script (Voiceover):**  
  > "To conclude: our ₹1.03 lakh quarterly figure represents modeled recoverable staffing capacity to absorb volume growth without hiring, not immediate payroll cash cuts. We recommend deploying the ₹4 lakh training budget into diagnostic SOPs, escalation control, and queue sweeps across our 22 frontline agents, while exempting Tier 2 and hardware triage from remedial lists. Thank you."

---

### Presenter Checklist Before Recording:
* [ ] Local server running: `python -m http.server 8000 --directory web`
* [ ] Browser window sized to 1920x1080 (100% zoom)
* [ ] Audio microphone checked and clear
* [ ] Stop timer set for 3 minutes (180 seconds)
