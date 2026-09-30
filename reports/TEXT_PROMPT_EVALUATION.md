# Text Classifier Prompt & Pipeline Specification Report

**Document Version:** 2.0.0  
**Effective Date:** 2026-09-30  
**Evaluation Scope:** 180 Stratified Support Tickets (`reports/text_eval_sample.csv`)  
**Label Provenance:** Rule-Assisted Deterministic Pseudo-Labels (`reports/text_pseudo_labels.csv`)  
**Execution Context:** Local Simulation & Heuristic Prompt Comparison (Zero External Cloud API Calls, ₹0 Paid Cost)  
**Definitive Quantitative Benchmark:** See `reports/CV_EVALUATION.md` for empirical held-out 5-fold cross-validation.  

---

## 1. Context & Scope

This document details the system prompt engineering designs for Vireo Audio's AI text intelligence pipeline:
* **Version 1 (`prompts/text_classifier_v1.md`):** Baseline prompt template with standard operational definitions.
* **Version 2 (`prompts/text_classifier_v2.md`):** Disambiguated prompt template incorporating negative constraints, disambiguation rules for cancellations vs refunds, conservative hardware failure syntax, and agent note shorthand handling.

### Scientific & Operational Integrity Notice:
In accordance with client budget constraints (prohibiting per-ticket cloud API spending across 11,750 tickets), **zero paid external LLM calls were executed**. The metrics below reflect an offline heuristic prompt-rule simulation contrasting uncalibrated rule matching (v1) with disambiguated rule logic (v2). 

For the **true empirical generalization benchmark of our machine learning code**, consult `reports/CV_EVALUATION.md` which documents held-out 5-fold cross-validation (**55.56% Pure ML Accuracy / 0.5388 Macro F1; 65.56% Hybrid Accuracy / 0.6443 Macro F1**).

---

## 2. Evaluation Sample Design

* **Sample Size:** 180 tickets.
* **Stratification:** Controlled sampling (`random_seed=42`) proportional to intake category, channel mix, CSAT availability, replacement issuance, and product representation (with focused coverage of Pulse 2 and the intake category "Other").
* **Exclusions:** 45 telephony/IVR junk records (such as `[line dropped]`, `[inaudible]`, or length < 15 chars) were excluded from language evaluation and tracked separately.
* **Benchmark Labels:** Generated deterministically via policy metadata and keyword logic, stored in `reports/text_pseudo_labels.csv` with explicit provenance `label_source = "rule_assisted_pseudo_label"`.

---

## 3. Version 1 vs Version 2 Prompt Design Heuristic Comparison

| Dimension | Version 1 (Baseline Prompt Template) | Version 2 (Disambiguated Prompt Template) | Design Impact |
| :--- | :---: | :---: | :--- |
| **Cancellation Handling** | Evaluated after refund logic; misclassified cancellation as refunds | High-priority pre-dispatch intent check | Prevents erroneous refund routing |
| **Hardware Defect Criteria** | Triggered on battery degradation or low volume complaints | Restricted strictly to physical failure vocabulary (dead bud, corroded pin) | Eliminates false RMA authorizations |
| **Agent Shorthand Notes** | Mapped brief notes (*"cx ok"*, *"sorted"*) to resolved status | Explicitly mapped to `unresolved_ambiguous` unless explicit action stated | Prevents artificial resolution rate inflation |
| **Output Schema** | Basic category and outcome | Structured JSON with confidence, rule override flag, and signal source | Enables full auditable trace |

---

## 4. Key Failure Modes Addressed in Version 2

### Weakness 1: Confusion Between Cancellation and Returns/Refunds
* **v1 Mode:** Customer messages like *"cancel order VR896827"* or *"cancle ordr before shipping"* were misclassified as `returns_refunds` because v1 matched on financial refund keywords.
* **v2 Improvement:** Version 2 introduced a high-priority cancellation rule that explicitly checks for pre-dispatch cancellation intents before evaluating refund workflows.
* **Resolution:** Overt cancellation requests are routed to immediate fulfillment stoppage.

### Weakness 2: Hardware Defect Signal Conservative Calibration
* **v1 Mode:** Customers stating *"battery life lasts 4 hours instead of 6"* were tagged with `hardware_defect_signal: true`.
* **v2 Improvement:** Version 2 restricted the hardware defect signal strictly to physical failure vocabulary (e.g. *"left earbud not charging"*, *"dead in the case"*, *"charging pins damaged"*).
* **Resolution:** The hardware detector achieved **100% precision** on the benchmark sample ($TP=8, FP=0, TN=163, FN=9$), eliminating false positive RMA replacements.

### Weakness 3: Handling of Shorthand Agent Notes
* **v1 Mode:** Uninformative agent shorthand such as *"see prev"*, *"cx ok"*, or *"sorted"* was inconsistently assigned to `troubleshooting_resolved`.
* **v2 Improvement:** Version 2 explicitly mandates that shorthand notes without explicit action verbs be categorized as `unresolved_ambiguous`.
* **Resolution:** Prevents false resolution inflation in agent performance reporting.

---

## 5. Transition to Machine Learning & Cross-Validation

While prompt specifications provide clear production templates for future LLM integration, the actual deployed analytics pipeline utilizes local scikit-learn models and regex rules to deliver instant, zero-cost classification. 

For the complete held-out statistical evaluation and baseline comparisons, refer directly to [CV_EVALUATION.md](file:///d:/vireo-audio/reports/CV_EVALUATION.md) and [TEXT_MODEL_CARD.md](file:///d:/vireo-audio/reports/TEXT_MODEL_CARD.md).
