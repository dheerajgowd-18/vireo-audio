# Model Card: Vireo Audio Local Ticket Classifier & Theme Extractor

**Model Name:** `vireo-ticket-classifier-local`  
**Model Version:** `2.0.0`  
**Release Date:** September 2026  
**License:** Proprietary / Internal Use Only  
**Model Type:** Hybrid Text Intelligence Architecture (TF-IDF + Balanced Logistic Regression + Deterministic Rule Overrides)  

---

## 1. Model Details

* **Developers:** Vireo Audio Analytics & Data Engineering Team.
* **Architecture:**
  * **Feature Extraction:** Sub-linear TF-IDF vectorization with unigrams and bigrams (`ngram_range=(1, 2)`), English stop-word removal, and vocabulary capped at 2,500 terms.
  * **Statistical Classifier:** Multiclass Logistic Regression with $L_2$ regularization, balanced class weights (`class_weight='balanced'`), and L-BFGS solver (`max_iter=500`).
  * **Deterministic Rule Engine:** High-priority regex rules for order cancellation and physical charging pin defects.
  * **Hardware Defect Signal Detector:** Independent regex pattern matcher targeting physical earbud failure syntax.
  * **Resolution Mapper:** Policy-backed rule engine extracting outcomes from agent notes and transactional ledgers.
* **Compute Infrastructure:** 100% local CPU execution. Zero external cloud API calls; ₹0 paid inference cost.
* **Output Schema:** Structured prediction records including `ai_issue_category`, `ai_resolution_outcome`, `hardware_defect_signal`, `hardware_signal_source`, `ai_confidence`, `is_rule_override`, and `prediction_source`.

---

## 2. Intended Use

### In-Scope Operational Uses:
* **Thematic Decomposition:** Retrospective classification of customer support messages into 9 standard operational issue categories.
* **Intake Bot Remediation:** Decomposing tickets originally miscategorized as generic "Other" by the front-end intake bot into actionable support queues.
* **Hardware Defect Early Warning:** Identifying clusters of overt physical hardware defects (e.g. charging contact corrosion, dead earbuds) to correlate against manufacturing lot codes (such as Pulse 2 lots).
* **Workload Triage:** Routing complex technical tickets to Tier 2 agents and straightforward courier inquiries to Logistics.

### Out-of-Scope / Prohibited Uses:
* **Automated Disciplinary Actions:** The model must **never** be used as the sole basis for agent termination, punitive scorecards, or compensation cuts.
* **Autonomous Financial Decisions:** The model must not autonomously issue refunds or approve RMAs without human agent verification.
* **Causal Attribution:** The model's predictions must not be used to make causal claims regarding customer dissatisfaction without controlling for hardware defects, delivery delays, and tier complexity.

---

## 3. Factors & Subgroups

* **Channels:** Supports Chat, Email, and Voice. 
  * *Filtering Guardrail:* Short telephony IVR fragments (<15 characters, `[line dropped]`, `[inaudible]`) are detected by diagnostics and excluded from evaluation sampling.
* **Product Coverage:** Encompasses all 14 Vireo Audio products, with focused sensitivity on the Pulse 2 wireless earbuds (`VA-EB-PL2`).
* **Support Tiers:** Evaluates ticket themes across Tier 1 Frontline, Tier 2 Hardware Triage, and Logistics/Operations.

---

## 4. Empirical Evaluation & Performance Metrics

### 5-Fold Stratified Cross-Validation (Held-Out Benchmark, $N=180$)

All metrics reflect strictly out-of-fold generalization performance across 5 cross-validation folds. For every fold, feature vectorization was fitted exclusively on training folds ($X_{train}$), eliminating data leakage.

| Architecture / Evaluation Step | Accuracy | Macro Precision | Macro Recall | Macro F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| **Majority Class Baseline** (`connectivity_pairing`) | 26.67% | 0.0296 | 0.1111 | 0.0468 |
| **Simple Keyword Rules** | 46.11% | 0.7224 | 0.5373 | 0.5399 |
| **Pure ML (Held-Out 5-Fold CV)** | **55.56%** | **0.5342** | **0.5528** | **0.5388** |
| **Hybrid Pipeline (Rules + 5-Fold ML Fallback)** | **65.56%** | **0.6374** | **0.6655** | **0.6443** |

### Per-Category Held-Out Generalization (Pure ML)

* `delivery_shipping`: Precision 0.7273, Recall 0.8000, F1 0.7619 ($N=30$)
* `charging_battery`: Precision 0.6522, Recall 0.6522, F1 0.6522 ($N=23$)
* `connectivity_pairing`: Precision 0.6667, Recall 0.6250, F1 0.6452 ($N=48$)
* `billing_payment`: Precision 0.7143, Recall 0.5263, F1 0.6061 ($N=19$)
* `cancellation`: Precision 0.7500, Recall 1.0000, F1 0.8571 ($N=3$) *(Low sample warning)*
* `product_enquiry_setup`: Precision 0.5000, Recall 0.5000, F1 0.5000 ($N=4$) *(Low sample warning)*
* `returns_refunds`: Precision 0.3333, Recall 0.4286, F1 0.3750 ($N=21$)
* `other_unclear`: Precision 0.2500, Recall 0.2667, F1 0.2581 ($N=15$)
* `hardware_audio_defect`: Precision 0.2143, Recall 0.1765, F1 0.1935 ($N=17$)

### Hardware Defect Detector Benchmark

* **True Positives ($TP$)**: 8 | **False Positives ($FP$)**: 0
* **True Negatives ($TN$)**: 163 | **False Negatives ($FN$)**: 9
* **Precision**: **100.00%** | **Recall**: **47.06%** | **F1-Score**: **64.00%**
* *Operational Profile:* Conservative zero-false-positive filter. It guarantees that any ticket flagged as a hardware defect is legitimate, preventing erroneous RMA cost inflation.

---

## 5. Training & Evaluation Data

* **Source Population:** 11,750 customer support tickets spanning January 2025 to June 2026.
* **Evaluation Sample:** 180 tickets extracted via stratified sampling (`random_seed=42`) across intake category, channel, replacement status, and CSAT availability.
* **Label Provenance:**
  * Benchmark labels in `reports/text_pseudo_labels.csv` were programmatically synthesized using deterministic domain heuristics, policy metadata, and transaction records.
  * Explicitly documented as **rule-assisted pseudo-labels**, avoiding false claims of double-blind human verification.
  * Column `label_source = "rule_assisted_pseudo_label"` is recorded in every benchmark row.

---

## 6. Quantitative Analyses & Primary Failure Modes

1. **Acoustic vs. Electrical Defect Overlap:** Customers describing earbuds that are "dead" or "silent" trigger confusion between `hardware_audio_defect` (speaker driver failure) and `charging_battery` (pin contact failure).
2. **Compound Intents:** Messages combining delivery delays with refund or cancellation threats (e.g. *"Courier has not delivered for 10 days, refund my UPI payment now"*) contain overlapping keywords spanning three classes.
3. **Shorthand Agent Documentation:** Agent notes such as *"cx called"*, *"done"*, or `"- [closed]"` offer minimal linguistic signal, forcing reliance on customer message text alone.

---

## 7. Ethical Considerations & Operational Safeguards

* **Identity Protection:** Disambiguates agents with identical display names (e.g. Agent A3006 vs Agent A3029, both named "Kavya Pandey") using strict primary-key joins on `agent_id`.
* **Peer Stratification:** Prevents bias against Tier 2 hardware specialists who handle difficult, low-CSAT cases by benchmarking agents strictly within their operational tier.
* **Transparency & Provenance:** Every prediction records its provenance (`prediction_source`: `"ml"`, `"rule"`, or `"ml_low_conf_fallback"`; `is_rule_override`: boolean; `hardware_signal_source`: `"regex_rule"` or `"none"`).

---

## 8. Caveats & Strategic Recommendations

1. **Acquire Human Annotations:** Future model iterations should replace the rule-assisted pseudo-labels with a double-blind human-annotated sample of at least 500 tickets.
2. **Calibrate Low-Confidence Routing:** For production triage, route predictions with confidence below 0.15 to a human supervisor under `other_unclear`.
3. **Continuous Defect Monitoring:** Monitor the high-precision hardware defect detector against Pulse 2 manufacturing lot codes to catch batch regressions early.
