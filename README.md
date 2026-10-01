# Vireo Audio Support Intelligence

An enterprise-grade customer support analytics, financial reconciliation, and ticket text intelligence platform built for **Vireo Audio** leadership.

* **Primary Business Goal**: Reduce Tier 1 frontline (Chat and Email) above-median handle time from 6.54h to 4.86h (weighted peer medians: Chat 5.61h -> 3.81h, Email 8.49h -> 7.07h), eliminating 624.9 excess agent-hours per quarter, representing approximately ₹1,03,102 per quarter in modeled recoverable staffing capacity under Policy §4.
* **Core Deliverables**: Audited Analytical Engine (`src/`), 7-View Offline-First SaaS Dashboard (`web/`), Executive Memorandum (`reports/VIREO_EXECUTIVE_MEMO.md`), and Client Technical Audit Form (`reports/SUBMISSION_FINAL.md`).

### Quick Start
```bash
# 1. Run full analytical pipeline and cross-validation
python run_analysis.py

# 2. Run automated test suite (37/37 tests)
pytest -v

# 3. Compile and verify web dashboard consistency
python scripts/build_web_data.py
python scripts/verify_web_consistency.py

# 4. Launch web dashboard
python -m http.server 8000 --directory web
# Open http://localhost:8000 in your browser
```

---

## What It Does

Vireo Audio processes over 11,000 customer support tickets across chat, voice, email, and social channels. This system provides:
1. **Peer-Stratified Agent Scorecards**: Resolves employee identity collisions (e.g. duplicate display names) and benchmarks agents strictly against operational peers (Tier 1 Frontline vs Tier 2 Escalations vs Logistics).
2. **Deterministic Financial Ledgers**: Reconciles actual replacement inventory spend (unit BOM + ₹340 logistics under Policy §4) against Finance's flat estimates, revealing a ₹13.24L (+38.76%) cost overstatement.
3. **Product & Lot Quality Early Warning**: Identifies that the Pulse 2 wireless earbuds (`VA-EB-PL2`) drive 61.5% of all company replacements, isolating defect concentration in specific 2025 supplier production lots (e.g. `PL2-2510-3`).
4. **Local AI Ticket Intelligence**: Recovers 87.99% of ambiguous tickets originally dumped into the "Other" category, classifying them into 9 operational themes with zero external cloud API spend (₹0 paid cost; ₹58,750 cost avoidance).
5. **Interactive Support Intelligence Dashboard**: A fast, offline-first web dashboard built using native HTML5, CSS3, and Vanilla JavaScript with custom SVG charts and zero external dependencies.

---

## Architecture

```
[Raw CSVs: tickets, agents, orders, products]
                     │
                     ▼
       [Analytical Engine: src/]
       ├── data_loader.py (type coercion, legacy +05:30 offset)
       ├── data_quality.py (PK/FK validation, Cartesian prevention)
       ├── metrics.py (CSAT blanks excluded, attendance handle time)
       ├── financials.py (policy replacement costs, transfer penalties)
       ├── agent_analysis.py (peer stratification, rota tagging)
       ├── text_classifier.py (5-fold CV, TF-IDF + Logistic Regression)
       └── text_analysis.py ('Other' decomposition, defect ledger)
                     │
                     ▼
     [Analytical Outputs & Governance: reports/]
     ├── agent_scorecard.csv, monthly_trends.csv, lot_code_analysis.csv
     ├── text_predictions.csv, cv_predictions.csv, text_pseudo_labels.csv
     ├── DECISION_SPEC.md, CV_EVALUATION.md, TEXT_MODEL_CARD.md
     └── AI_ENGINEERING_DEFENSE.md, WEB_UI_DECISIONS.md
                     │
                     ▼ (python scripts/build_web_data.py)
        [Static Web Data: web/data/]
        ├── overview.json, agents.json, trends.json
        ├── replacements.json, sla.json, ai_signals.json, methodology.json
                     │
                     ▼ (python -m http.server 8000 --directory web)
        [Vanilla Web Frontend: web/]
        ├── index.html (Semantic 7-view structure & drawer)
        ├── styles.css (Minimal SaaS design system)
        └── app.js (Native DOM router, table sorting, SVG charts)
```

---

## Setup

### Prerequisites
* Python 3.10+
* Standard Python packages: `pandas`, `numpy`, `scikit-learn`, `pytest`

```bash
pip install pandas numpy scikit-learn pytest
```

---

## Run Analytics

Execute the complete deterministic analytics engine and machine learning evaluation:

```bash
python run_analysis.py
```

This ingests raw CSVs, performs data quality audits, runs held-out cross-validation, and exports all CSV/Markdown reports to `reports/`.

---

## Build Web Data

Compile the analytical outputs into compact, schema-validated JSON files for the frontend:

```bash
python scripts/build_web_data.py
```

Outputs 7 compact JSON files to `web/data/`.

---

## Run Frontend

Serve the static web dashboard locally using Python's built-in HTTP server:

```bash
python -m http.server 8000 --directory web
```

Then open your browser to:
[http://localhost:8000](http://localhost:8000)

* Fully functional offline with zero internet access, zero CDNs, and zero third-party UI libraries.

---

## Tests

Execute the automated test suite covering data quality, financial arithmetic, metric calculations, and cross-validation integrity:

```bash
python -m pytest tests/ -v
```

All 29 unit tests pass in under 2 seconds.

---

## Cost

* **Actual External Cloud API Calls**: 0
* **Actual Model Cost**: ₹0.00 (100% local CPU execution)
* **Hypothetical Cloud LLM Cost (@ ₹5/ticket)**: ₹58,750.00
* **Cost Avoidance Savings**: **₹58,750.00 (100% cost avoidance)**
* Preserves the client's entire ₹4,00,000 Q3 training budget for human agent development.

---

## AI Method

* **Feature Extraction**: Sub-linear TF-IDF vectorizer (unigrams + bigrams, 2,500 max features, English stop words).
* **Classifier**: Balanced multiclass Logistic Regression with $L_2$ regularization and deterministic rule overrides for high-risk actions (e.g. order cancellations).
* **Hardware Defect Signal**: High-precision regex pattern matcher targeting physical earbud failures (pins damaged, dead in case, not charging).
* **Empirical Validation**: Evaluated via strictly held-out **5-fold stratified cross-validation** with fold vectorizer independence (zero data leakage).
  * Majority Baseline: 26.67%
  * Keyword Rules: 46.11%
  * Pure ML (5-Fold CV): 55.56% (Macro F1: 0.5388)
  * Hybrid Pipeline: 65.56% (Macro F1: 0.6443)
  * Hardware Defect Signal: Precision = 100.0%, Recall = 47.06%, F1 = 64.00% (conservative text signal)
* **Benchmark Provenance**: Explicitly documented as rule-assisted pseudo-labels (`label_source = "rule_assisted_pseudo_label"`).

---

## Validation

Verify data integrity, schema consistency, and offline compliance across the web application:

```bash
python scripts/verify_web_consistency.py
```

Validates:
* All element IDs in `app.js` match `index.html`.
* Zero external CDN or network URLs in HTML, CSS, or JS.
* Overview KPIs match canonical analytical outputs.
* Exactly 44 agents and exactly 10 bottom agents (6 Tier 2, 4 Hardware Triage).
* 87.99% actionable 'Other' category decomposition.
* Product replacement counts and Pulse 2 concentration.

---

## Known Limitations

1. **Rule-Assisted Pseudo-Labels**: Benchmark annotations were derived via deterministic heuristics; double-blind human labels should be gathered for production retraining.
2. **Conservative Defect Detector**: The hardware defect signal achieves 100% precision but 47.06% recall; informal customer complaints require human technical triage.
3. **Observational Correlation**: Concentration of defect signals in specific lots indicates quality anomalies but does not replace physical hardware teardowns.
4. **Rare Classes**: Classes with low support (`cancellation` $N=3$, `product_enquiry_setup` $N=4$ in sample) rely on rule overrides to ensure stable inference.

---

## Project Structure

```
vireo-audio/
├── src/
│   ├── config.py                 # File paths, SLA thresholds, financial rates
│   ├── data_loader.py            # CSV loaders & timestamp normalization
│   ├── data_quality.py           # PK/FK validation & Cartesian join defense
│   ├── metrics.py                # CSAT, handle time, SLA calculation
│   ├── financials.py             # Replacement costing, transfers, lot analysis
│   ├── agent_analysis.py         # Peer stratification & scorecard assembly
│   ├── text_classifier.py        # 5-fold cross-validation, ML & regex classifier
│   └── text_analysis.py          # Theme decomposition & AI cost audit
├── scripts/
│   ├── build_web_data.py         # Compiles analytical outputs into web JSON
│   └── verify_web_consistency.py # Verifies data integrity & offline compliance
├── web/
│   ├── index.html                # Semantic HTML5 shell for 7 views & drawer
│   ├── styles.css                # Minimalist CSS design system with variables
│   ├── app.js                    # Native router, SVG charts, table sorting
│   └── data/                     # Compact analytical JSON files
├── reports/
│   ├── DECISION_SPEC.md          # Technical decisions specification
│   ├── CV_EVALUATION.md          # 5-fold held-out CV report & baselines
│   ├── TEXT_MODEL_CARD.md        # Industry-standard model card
│   ├── AI_ENGINEERING_DEFENSE.md # Technical interview defense (12 questions)
│   ├── TEXT_PROMPT_EVALUATION.md # Prompt templates specification
│   ├── TEXT_TAXONOMY.md          # 9-category issue & outcome taxonomy
│   └── WEB_UI_DECISIONS.md       # Frontend architectural & UI decisions
├── tests/
│   ├── test_data_quality.py      # Tests PK/FK integrity & Cartesian defense
│   ├── test_metrics.py           # Tests blank CSAT, handle time, SLAs
│   ├── test_financials.py        # Tests replacement arithmetic & lot analysis
│   └── test_text_classifier.py   # Tests CV independence, schema, metadata
├── run_analysis.py               # End-to-end analytics execution script
└── README.md                     # Comprehensive project documentation
```
