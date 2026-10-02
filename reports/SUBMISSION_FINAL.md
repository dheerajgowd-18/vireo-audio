# Vireo Audio Support Intelligence & Performance Evaluation
## Client Final Submission Form & Technical Audit Responses

**Candidate / Engineer:** Lead Data & AI Engineer  
**Evaluation Scope:** 11,750 Tickets, 44 Support Agents, 18 Months (January 2025 – June 2026)  
**Date of Submission:** October 1, 2026  
**Status:** Complete, Audited & Defensible  

---

### What did you build, and what business outcome does it move?

We built a complete, offline-capable Support Intelligence system comprising:
1. **Deterministic Analytics Engine (`src/`)**: Ingests, normalizes, and reconciles 11,750 support tickets, 44 agents, 15,500 orders, and 14 product SKUs strictly under operating policy (`support-policy.pdf` v3.2).
2. **Peer-Stratified Performance Benchmarking**: Resolves display-name collisions (`A3006` vs `A3029` Kavya Pandey), separates Tier 1 frontline queues from Tier 2 escalations and hardware triage, and evaluates handle times against team peer medians.
3. **Local AI Ticket Intelligence**: A local TF-IDF + Logistic Regression NLP classifier running in 3.8 seconds at ₹0 paid API cost that decomposes 87.99% of ambiguous "Other" tickets into operational themes.
4. **Replacement & SLA Ledgers**: Deterministically reconciles warranty replacement spend (unit BOM + ₹340 logistics under Policy §5) and SLA breach exposure.
5. **Interactive Support Intelligence Dashboard (`web/`)**: A fast, offline-first SaaS dashboard built with native HTML5, CSS3, and Vanilla JavaScript with custom SVG charts and zero external dependencies.

**Primary Business Outcome Moved:**
> **"Reduce Tier 1 frontline (Chat and Email) above-median handle time from 6.54h to 4.86h, eliminating approximately 624.9 excess agent-hours per quarter and representing approximately ₹1,03,102 per quarter in modeled recoverable staffing capacity."**

Across four quarters, this unlocks **approximately ₹4.12 lakh annualized modeled capacity value** under Policy §4 (at the fully loaded agent labor rate of ₹165/hour) to absorb volume growth without adding headcount, while monitoring CSAT alongside efficiency gains to avoid deterioration in our historical baseline (3.33 overall mean).

---

### What does one run cost, and what would a month cost at Vireo's volume (roughly 650 tickets a week)?

**One Run Cost:**
* **External API Calls:** 0
* **Actual Paid Model Cost:** **₹0.00**
* Production inference executes 100% locally on standard CPU hardware via scikit-learn in **3.8 seconds** (~3,000 tickets/sec). The web interface has zero external CDN or cloud hosting dependencies.
* *Hypothetical Client Benchmark:* Under the client's hypothetical comparison assumption of ₹5/ticket for external cloud LLM calls, classifying the historical dataset of 11,750 tickets would represent a hypothetical external-call expense of **₹58,750.00** ($11,750 \times ₹5.00$). This is a hypothetical benchmark comparison, not an incurred project expense.

**Monthly Cost at Vireo's Volume:**
* **Weekly Volume:** Roughly 650 tickets/week.
* **Monthly Volume Approximation:** $650 \text{ tickets/week} \times \frac{52 \text{ weeks}}{12 \text{ months}} \approx \mathbf{2,817 \text{ tickets/month}}$.
* **Expected Paid AI Cost:** **₹0.00 per month**.
* The local model runs incrementally in under 1 second of CPU compute per month with zero cloud API billing, fully preserving Vireo's operational budget.

---

### How do you know it works?

We established multi-layered empirical verification across data, machine learning, and frontend layers:
1. **Automated Test Suite (37/37 Tests Passing)**:
   * Data quality & primary/foreign key uniqueness (`tests/test_data_quality.py`).
   * CSAT blank exclusion, attendance-only handle time, and legacy +05:30 offset (`tests/test_metrics.py`).
   * Policy replacement cost arithmetic and fan-out prevention (`tests/test_financials.py`).
   * ML cross-validation fold independence and schema preservation (`tests/test_text_classifier.py`).
   * Business case denominators and capacity formulas (`tests/test_business_reconciliation.py`).
2. **Production Row Count & Data Invariance**:
   * Exactly 11,750 ticket rows ingested and preserved across all transformations; zero dropped records.
3. **Empirical Held-Out Cross-Validation (5-Fold Stratified CV)**:
   * Evaluated across the 180-ticket benchmark with fold-independent vectorization (zero data leakage):
     * *Pure ML (TF-IDF + Logistic Regression)*: **Accuracy = 55.56%**, **Macro F1 = 0.5388**.
     * *Majority Class Floor (`connectivity_pairing`)*: 26.67% accuracy, 0.0468 Macro F1 (+28.89% absolute ML improvement).
     * *Simple Keyword Rules*: 46.11% accuracy, 0.5399 Macro F1.
     * *Hybrid Pipeline (Rules + CV ML Fallback)*: **65.56% accuracy**, **0.6443 Macro F1**.
4. **Hardware Defect Signal Evaluation**:
   * On the benchmark sample: **Precision = 100.00%**, **Recall = 47.06%**, **F1 = 64.00%** ($TP=8, FP=0, TN=163, FN=9$). The 100% precision represents an internal self-consistency check against deterministic regex pseudo-labels, operating as an intentionally conservative text signal with zero false alarms while capturing ~47% of overt failure phrasing.
5. **Evaluation Honesty & Label Provenance**:
   * *The benchmark labels are rule-assisted pseudo-labels, not independently human-annotated gold labels.* They were programmatically derived via deterministic policy rules and keyword heuristics (`label_source = "rule_assisted_pseudo_label"`).
6. **Web Consistency Verifier**:
   * Automated verification (`scripts/verify_web_consistency.py`) verifies 100% ID matching between `index.html` and `app.js`, zero CDN dependencies, and exact metric parity with analytical outputs.

---

### Did you change, narrow, or push back on the client's ask? What, when, and why?

Yes. We made deliberate, evidence-based scoping adjustments during the implementation audit:
1. **Narrowed the "Bottom 10" Training Ask to Comparable Operational Peers**:
   * *Client Ask:* Flag the bottom 10 agents by raw CSAT / handle time for remedial training.
   * *Adjustment:* We retained the requested raw "Bottom 10" view in the dashboard, but narrowed training interpretation strictly to comparable operational groups. 
   * *Why:* Six of the bottom ten agents are Tier 2 Escalation specialists handling multi-day, pre-escalated disputes, and four are frontline hardware triage agents ("Kavya's four"). Policy §6 explicitly states that Tier 2 cases are multi-touch by nature and must not be compared with Tier 1 on volume metrics. These agents handle structurally different work populations; using raw cross-tier rankings to drive remedial training would misdirect capital.
2. **Replaced Finance's Informal ₹2,500 Replacement Cost with Policy §5 Standards**:
   * *Client Context:* Finance Controller Arjun Mehta estimated replacements at a flat ₹2,500/unit.
   * *Adjustment:* We calculated replacement spend using Policy §5: $\text{Unit BOM Cost} + ₹340 \text{ Logistics}$.
   * *Why:* Product BOM costs range from ₹90 to ₹2,650. Finance's flat assumption overstated replacement liability by ₹13,24,010 (+38.76%). Policy §5 is the binding operational standard.
3. **Avoided Risky Fallback Order Joins**:
   * *Client Context:* 4,107 tickets lacked `order_id`; `README.txt` suggested `(customer_id, product_sku)` as a fallback.
   * *Adjustment:* We restricted order joins strictly to direct `order_id` links.
   * *Why:* 1,388 customer-SKU pairs placed multiple orders. Joining on customer+SKU would have triggered a Cartesian fan-out, duplicating ticket rows and inflating financial calculations.
4. **Avoided Per-Ticket Cloud LLM Calls**:
   * *Client Context:* Email thread discussed ₹5/ticket cloud API costs.
   * *Adjustment:* We engineered a local scikit-learn NLP pipeline.
   * *Why:* Avoided ₹58,750 in cloud compute, eliminated PII transmission risks, and cut runtime from ~98 minutes to 3.8 seconds.

---

### What is wrong with what you are handing us?

To maintain absolute technical and operational honesty:
1. **Handle Time Reflects Operational Aging and Queue Dynamics**: Mean handle time is heavily skewed by a long right tail of multi-day pending tickets awaiting customer or courier replies. It cannot be treated as pure active keyboard/talk time.
2. **AI Layer is Assistive, Not Autonomous**: The classifier provides retrospective intelligence and triage signals; it is not an autonomous action agent and does not auto-resolve tickets.
3. **Benchmark Evaluated on Rule-Assisted Pseudo-Labels**: Ground-truth labels in the 180-ticket sample were derived using deterministic heuristics rather than double-blind human annotations with inter-rater reliability scores.
4. **Low Validation Support on Rare Classes**: Categories such as `cancellation` ($N=3$) and `product_enquiry_setup` ($N=4$) have limited representation in the sample, requiring rule overrides in production.
5. **No Physical Manufacturing Root-Cause Proof**: While lot `PL2-2510-3` correlates strongly with replacements (40.94% rate) and charging contact failure phrases, observational text cannot prove physical metallurgy or factory root causes without destructive physical lab teardowns.
6. **Batch Export, Not Real-Time Streaming**: Ingestion operates as a batch analytics pipeline; real-time Kafka/webhook streaming was not implemented within scope.
7. **No External LLM Runtime Configured**: System prompt templates (`prompts/text_classifier_v1.md`, `v2.md`) are engineered for future cloud migration, but no live external API integration is active.

---

### What did you deliberately leave out, and why that rather than something else?

We deliberately excluded several potential components to maximize reliability, budget efficiency, and interpretability under the 5-hour engineering constraint:
1. **Per-Ticket Cloud LLM Inference**: Calling commercial APIs across 11,750 tickets would have cost ₹58,750 (14.7% of the entire Q3 training budget) and introduced external network failure modes.
2. **Complex Multi-Agent Frameworks**: Auto-GPT/CrewAI architectures add non-deterministic latency, debugging opacity, and high token overhead without improving deterministic SQL/pandas accuracy.
3. **Predictive Time-Series Forecasting**: Forecasting future ticket volume or stockouts requires external seasonal demand and marketing campaign data not present in the historical CSVs.
4. **Risky Customer+SKU Fallback Joins**: Omitted to prevent Cartesian row duplication across 1,388 multi-order customer-SKU pairs.
5. **Automated Employee Scoring & Disciplinary Decisioning**: We intentionally avoided single-score punitive rankings, providing peer-stratified context to support human supervisory discretion.
6. **Definitive Causal Attribution Models**: Omitted causal inference econometric modeling because observational support logs lack instrumental variables or randomized A/B holdouts.

---

### Anything you built or found that nobody asked for?

Yes. Our forensic audit uncovered several critical operational insights beyond the original prompt:
1. **Pulse 2 Replacement Concentration & High-Replacement Lot Candidate**:
   * Pulse 2 earbuds drive **61.50% of all company replacements (1,166 units; ₹21,22,120)**.
   * Specific manufacturing production lot candidate **`PL2-2510-3`** exhibits an abnormal **40.94% replacement rate** (70 replacements across 171 tickets on direct `order_id` join) with text signatures consistently describing charging cradle pin contact failure.
2. **Finance Replacement Cost Overstatement (₹13.24L / +38.76%)**:
   * Reconciled actual Policy §5 replacement spend (₹34.16L) against Finance's flat ₹2,500 estimate (₹47.40L), identifying a ₹13.24L overstatement.
3. **Decomposition & Recovery of the "Other" Category**:
   * Recovered **1,524 actionable tickets (87.99%)** from the 1,732 tickets dumped into "Other" by the intake bot, mapping them to concrete operational drivers like delivery (21.8%) and connectivity (19.5%).
4. **Policy Compliance Exceptions (Dual Refund & Replacement)**:
   * Identified 6 tickets and 131 orders where both a refund and a replacement were recorded, isolating them for operational review under Policy §5.
5. **Agent Display Name Collision Safeguard**:
   * Identified and protected two distinct agents named "Kavya Pandey" (`A3006` in Chat vs `A3029` in Logistics), enforcing strict foreign key joins on `agent_id`.
6. **Telephony IVR Transcription Corruption**:
   * Isolated ~40 tickets where IVR navigation transcripts were corrupted during telephony gateway export, exonerating agents from responsibility.

---

### What did you use AI for?

We used AI across two distinct dimensions: embedded statistical NLP within the product, and AI coding assistants during engineering development.

1. **Embedded Product NLP (100% Local Scikit-Learn)**:
   * **Feature Extraction & Modeling**: Sublinear TF-IDF vectorization (unigrams + bigrams, 2,500 features) paired with a balanced multiclass Logistic Regression model to classify unstructured customer messages into 9 operational issue themes.
   * **Deterministic Signal Rules**: High-precision regular expression pattern matching targeting overt hardware failure terminology (charging pins, dead case contacts).
   * **Theme Recovery**: Decomposed 87.99% of ambiguous intake "Other" tickets into actionable routing themes at ₹0 paid API cost.

2. **AI Development Tools (Agentic Coding & LLM Assistance)**:
   * **Where AI Helped Most**:
     - *Rapid Boilerplate & Test Generation*: Generating parameter-rich pytest test fixtures for timestamp edge cases (+05:30 IST offset) and primary/foreign key integrity checks.
     - *CSS Design System Architecture*: Scaffolding a clean, accessible, Linear/Stripe-inspired monochrome design system with native CSS variables and SVG line-chart mathematics without third-party chart libraries.
     - *Cross-Validation Pipeline*: Structuring strict fold-independent feature vectorization in `src/text_classifier.py` to prevent data leakage.
   * **Where AI Wasted Time & Generated Unreliable Output**:
     - *Hallucinated In-Sample Metrics*: Early AI scaffolding evaluated models on their own training folds, mistakenly declaring "98.89% accuracy" which collapsed to 55.56% under rigorous held-out cross-validation.
     - *Circular Ground Truth Validation*: AI scripts generated pseudo-labels using deterministic regex rules and then evaluated those same regex rules against them, claiming "100% precision / 47% recall" as an independent benchmark rather than recognizing it as an internal self-consistency check.
     - *Denominator Inconsistencies*: AI drafts computed handle time across attendance-only tickets but initially multiplied excess hours across all tickets including uncompleted tickets, requiring manual mathematical audit and correction.
   * **Discarded Prompt & Model Experiments**:
     - *Heuristic Prompt Comparison Claims*: Authored structured prompt specifications (`prompts/text_classifier_v1.md`, `v2.md`), but discarded early 82.22% vs 92.78% comparative claims because zero external LLM API calls were executed.
     - *Per-Ticket Cloud LLM Architecture*: Discarded external cloud LLM inference entirely to honor the ₹0 API spend constraint, eliminate PII privacy risks, and reduce processing time from ~98 minutes (hypothetical sequential API latency) to 3.8 seconds locally.

---

### Link your three-minute screen recording here.

`[PUBLIC GOOGLE DRIVE VIDEO LINK]`

---

### Public Google Drive Link

`[PUBLIC DRIVE FOLDER LINK]`

---

### Someone picks this up on Monday and you are unreachable. The three things they need to know.

1. **How to Run the Entire System in Under 60 Seconds**:
   * Analytical pipeline & CV: `python run_analysis.py`
   * Automated test suite (37 tests): `python -m pytest tests/ -v`
   * Web data compilation & consistency check: `python scripts/build_web_data.py && python scripts/verify_web_consistency.py`
   * Launch frontend: `python -m http.server 8000 --directory web` (Open `http://localhost:8000`).
2. **Source of Truth for Data & Business Goals**:
   * Analytical outputs live in `reports/` (`agent_scorecard.csv`, `monthly_trends.csv`, `lot_code_analysis.csv`, `cv_predictions.csv`).
   * Primary Business Goal: *"Reduce Tier 1 frontline (Chat and Email) above-median handle time from 6.54h to 4.86h, eliminating approximately 624.9 excess agent-hours per quarter and representing approximately ₹1,03,102 per quarter in modeled recoverable staffing capacity under Policy §4."*
3. **Critical Operational & Analytical Caveats**:
   * **Do Not Join on Agent Name**: Always join on `agent_id` (`A3006` and `A3029` share the name Kavya Pandey).
   * **Do Not Train Tier 2 or Hardware Triage Based on Raw CSAT**: Tier 2 cases are multi-touch investigations under Policy §6; hardware triage intentionally handles damaged goods. Compare agents only within their peer benchmark group.
   * **Pulse 2 is an Operational Hardware Signal**: The ₹21.22L Pulse 2 replacement spend and lot `PL2-2510-3` concentration require hardware/supply-chain investigation; support training cannot fix physical hardware issues.

---

### Honest hours spent.

`[HONEST HOURS SPENT]`

---

### Github Repo Link

https://github.com/dheerajgowd-18/vireo-audio
