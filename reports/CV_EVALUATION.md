# Empirical Cross-Validation Evaluation Report: Text Classification Layer

**Document Version:** 2.0.0  
**Effective Date:** 2026-09-30  
**Evaluation Scope:** 180 Stratified Support Tickets (`reports/text_eval_sample.csv`)  
**Label Provenance:** Rule-Assisted Deterministic Pseudo-Labels (`reports/text_pseudo_labels.csv`)  
**Evaluation Engine:** 5-Fold Stratified Cross-Validation (`src/text_classifier.py`)  
**Out-of-Fold Predictions:** `reports/cv_predictions.csv` *(Local-only benchmark artifact; regenerable via `run_analysis.py`)*  

---

## 1. Executive Summary & Evaluation Integrity

In this evaluation, we replace earlier in-sample alignment claims with a mathematically rigorous, held-out **5-fold stratified cross-validation** benchmark. 

Key empirical findings:
1. **True Generalization Performance (Pure ML)**: The held-out TF-IDF + Logistic Regression model achieves **55.56% accuracy** and a **Macro F1-score of 0.5388**. The previously cited 98.89% was an in-sample training metric caused by evaluating the model on its own training data.
2. **Baseline Hierarchy**:
   * *Majority Class Baseline*: 26.67% accuracy (Macro F1: 0.0468).
   * *Simple Keyword Rules*: 46.11% accuracy (Macro F1: 0.5399).
   * *Pure ML (5-Fold CV)*: 55.56% accuracy (Macro F1: 0.5388).
   * *Hybrid Pipeline (Rules + ML Fallback)*: 65.56% accuracy (Macro F1: 0.6443).
3. **Hardware Defect Signal Reality**:
   * Evaluated on the benchmark sample: **Precision = 100.00%**, **Recall = 47.06%**, **F1-Score = 64.00%** ($TP=8, FP=0, TN=163, FN=9$).
   * *Critical Provenance Disclosure*: The benchmark pseudo-label for hardware defect signal (`gt_hardware_defect_signal`) was synthesized using the exact same deterministic regex rules as the detector. Consequently, 100% precision is an internal self-consistency check on the pseudo-label synthesis, NOT an independent gold-standard test on unseen human-labeled text. In production, unmodeled colloquial descriptions will yield lower empirical precision and recall.
4. **Label Provenance & Rare-Class CV Limitations**:
   * All benchmark labels were programmatically derived via deterministic policy rules and keyword heuristics. They are explicitly documented as **rule-assisted pseudo-labels**, not double-blind independent human annotations.
   * *Rare-Class Split Caveat*: With $N=180$ tickets across 9 classes, 5-fold StratifiedKFold cannot guarantee balanced representation for classes where $N < 5$ (`cancellation` $N=3$, `product_enquiry_setup` $N=4$), leading to folds with 0 validation examples for those classes.

---

## 2. Cross-Validation Methodology

To guarantee complete independence between training and validation data:
* **Stratified Folds**: 5 folds partitioned proportionally across the 9 issue categories with a fixed seed (`seed=42`).
* **Zero Feature Leakage**: For each fold, the `TfidfVectorizer` (max features=2,500, n-gram range=(1, 2)) was fitted **strictly on the training fold ($X_{train}$)**. Vocabulary sizes varied across folds (Fold 1: 1,929, Fold 2: 1,876, Fold 3: 1,925, Fold 4: 1,934, Fold 5: 1,917), confirming total vectorizer independence.
* **Out-of-Fold Evaluation**: Predictions were generated strictly on unseen validation folds ($X_{val}$). Every prediction in `reports/cv_predictions.csv` represents an out-of-fold inference (text benchmark artifacts containing customer message text are intentionally kept local and can be regenerated from the supplied evaluation data).

---

## 3. Comparative Baseline Performance Hierarchy

| Architecture / Baseline | Accuracy | Macro Precision | Macro Recall | Macro F1-Score | Architectural Role |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Majority Class Baseline** (`connectivity_pairing`) | 26.67% | 0.0296 | 0.1111 | 0.0468 | Theoretical floor (predicting most frequent class) |
| **Simple Keyword Rules** | 46.11% | 0.7224 | 0.5373 | 0.5399 | Pure regex / keyword matching |
| **Pure ML (5-Fold Stratified CV)** | **55.56%** | **0.5342** | **0.5528** | **0.5388** | Held-out TF-IDF + Balanced Logistic Regression |
| **Hybrid Pipeline** (Rules + CV ML Fallback) | **65.56%** | **0.6374** | **0.6655** | **0.6443** | Deterministic overrides + ML out-of-fold fallback |

### Key Takeaway:
* Pure ML provides a **+28.89% absolute accuracy boost** over the majority class baseline, proving genuine statistical feature extraction.
* Combining deterministic domain rules with machine learning yields the best operational performance (**65.56% accuracy / 0.6443 Macro F1**), demonstrating that domain rules and statistical learning complement each other.

---

## 4. Per-Class Held-Out Performance (Pure ML 5-Fold CV)

| Issue Category | Precision | Recall | F1-Score | Support ($N$) | Operational Assessment |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `billing_payment` | 0.7143 | 0.5263 | 0.6061 | 19 | Strong precision; struggles on brief UPI/invoice notes |
| `cancellation` | 0.7500 | 1.0000 | 0.8571 | 3 | **Warning: Low Sample Size ($N=3$)** |
| `charging_battery` | 0.6522 | 0.6522 | 0.6522 | 23 | Balanced performance across battery/case complaints |
| `connectivity_pairing` | 0.6667 | 0.6250 | 0.6452 | 48 | Most common class; stable feature weights |
| `delivery_shipping` | 0.7273 | 0.8000 | 0.7619 | 30 | High recall on courier, tracking, and transit terms |
| `hardware_audio_defect` | 0.2143 | 0.1765 | 0.1935 | 17 | Confused with charging issues (e.g. dead bud vs dead pin) |
| `other_unclear` | 0.2500 | 0.2667 | 0.2581 | 15 | Inherently noisy; captures residual ambiguity |
| `product_enquiry_setup` | 0.5000 | 0.5000 | 0.5000 | 4 | **Warning: Low Sample Size ($N=4$)** |
| `returns_refunds` | 0.3333 | 0.4286 | 0.3750 | 21 | Often confused with delivery tracking and cancellations |
| **Macro Average** | **0.5342** | **0.5528** | **0.5388** | **180** | **Balanced evaluation across all 9 classes** |

---

## 5. Rare Class Sample Size Warnings

> [!WARNING] Statistical Reliability Notice for Low-Support Classes
> * **`cancellation` ($N=3$)**: Representing only 1.67% of the evaluation sample. In a 5-fold cross-validation split, 2 of the 5 validation folds contained 0 cancellation examples. While metrics appear high (Precision: 0.7500, Recall: 1.0000), this is an artifact of tiny sample support.
> * **`product_enquiry_setup` ($N=4$)**: Support is only 4 examples (2.22% of sample). One fold contained 0 validation examples.
> * **Recommendation**: Triage these two classes with high-priority deterministic keyword rules rather than relying solely on statistical weights until a minimum of 50 human-annotated examples per class are acquired.

---

## 6. Confusion Matrix & Primary Error Modes

```
True \ Pred       bill   canc   chg   conn  deliv  hw_aud  oth   prod   ret   [Total]
billing_payment    10      0      1      2      2       0     2     0     2    [ 19 ]
cancellation        0      3      0      0      0       0     0     0     0    [  3 ]
charging_battery    0      0     15      3      1       3     0     0     1    [ 23 ]
connectivity_pair   2      0      1     30      3       5     3     1     3    [ 48 ]
delivery_shipping   0      1      0      0     24       0     2     0     3    [ 30 ]
hardware_audio      0      0      3      6      0       3     2     1     2    [ 17 ]
other_unclear       1      0      0      2      2       3     4     1     2    [ 15 ]
product_enquiry     0      0      0      1      0       0     1     2     0    [  4 ]
returns_refunds     1      0      3      1      1       0     4     1     9    [ 21 ]

Total Evaluated: 180 | Correct: 100 (55.56%) | Classification Errors: 80 (44.44%)
```

### Primary Diagnostic Error Modes:
1. **Acoustic vs Electrical Hardware Confusion**: Tickets complaining of *"no sound from left bud"* or *"dead in the case"* cross-correlate between `hardware_audio_defect` and `charging_battery`. The vocabulary overlap between "earbud dead" (battery failure) and "earbud dead" (audio driver failure) creates semantic ambiguity.
2. **Returns vs Delivery vs Cancellation**: Customers demanding a refund for an order that has not yet arrived span three workflow buckets simultaneously (`returns_refunds`, `delivery_shipping`, `cancellation`). 
3. **Telephony Shorthand in Agent Notes**: Brief agent notes (e.g., *"cx called"*, *"done"*, *"as discussed"*) provide negligible n-gram signal, forcing the classifier to rely entirely on the customer message.

---

## 7. Hardware Defect Detector Benchmark

The standalone regex-based hardware defect detector was evaluated against the benchmark ground truth:

```
Confusion Matrix (Hardware Defect Signal):
                   Predicted Negative (False)   Predicted Positive (True)
Actual Negative:              163                           0
Actual Positive:                9                           8
```

* **True Positives ($TP$)**: 8
* **False Positives ($FP$)**: 0
* **True Negatives ($TN$)**: 163
* **False Negatives ($FN$)**: 9
* **Precision**: **100.00%** ($8 / 8$)
* **Recall**: **47.06%** ($8 / 17$)
* **F1-Score**: **64.00%**

### Engineering Defense & Critical Caveat:
The hardware defect detector was intentionally designed with a **conservative regex pattern**. In customer support operations, misflagging a routine connection reset as a physical hardware defect risks unnecessary ₹1,800+ replacement authorizations. 

However, **this benchmark metric must be interpreted with technical honesty**: because `gt_hardware_defect_signal` in `reports/text_pseudo_labels.csv` was generated using the same heuristic regex logic (`detect_hardware_defect_signal`), the 100% precision score is an **internal self-consistency check** of deterministic rule execution, rather than an independent gold-standard validation against human medical/audio annotations. While capturing ~47% of overt hardware failures with zero heuristic false positives, the remaining 53% of colloquial complaints are safely routed to Tier 2 technical triage. True real-world precision and recall must be validated against human-annotated transcripts before deploying autonomous actions.
