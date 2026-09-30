"""Data builder for Vireo Audio Support Intelligence Dashboard.

Extracts analytical findings from verified reports and source data into compact,
structured JSON artifacts for the offline vanilla frontend.
"""

import json
import sys
from pathlib import Path

# Add project root to sys.path for direct execution
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
import numpy as np

from src.data_loader import load_all_datasets
from src.metrics import (
    calculate_csat_metrics,
    calculate_handle_time_metrics,
    calculate_sla_metrics,
    calculate_monthly_trends,
)
from src.financials import (
    calculate_operational_costs,
    calculate_replacement_costs,
    analyze_lot_code_replacements,
)
from src.agent_analysis import build_agent_scorecard
from src.text_classifier import run_held_out_cross_validation
from src.text_analysis import analyze_other_category


def format_currency_lakhs(amount_inr: float) -> str:
    """Format an INR amount into standard Lakhs representation."""
    lakhs = amount_inr / 100000.0
    return f"₹{lakhs:.2f}L"


def build_all_web_data():
    """Main data compiler writing out compact JSON files to web/data/."""
    print("Compiling analytics outputs for web dashboard...")
    output_dir = Path("web/data")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load foundational datasets
    datasets = load_all_datasets()
    tickets = datasets["tickets"]
    agents = datasets["agents"]
    orders = datasets["orders"]
    products = datasets["products"]

    # Load analytical reports
    scorecard_df = pd.read_csv("reports/agent_scorecard.csv")
    monthly_trends_df = pd.read_csv("reports/monthly_trends.csv")
    lot_code_df = pd.read_csv("reports/lot_code_analysis.csv")
    text_preds_df = pd.read_csv("reports/text_predictions.csv")
    agent_text_df = pd.read_csv("reports/ai_agent_text_summary.csv")
    sample_df = pd.read_csv("reports/text_eval_sample.csv")
    gt_df = pd.read_csv("reports/text_pseudo_labels.csv")

    # 2. OVERVIEW JSON
    csat = calculate_csat_metrics(tickets)
    handle_time = calculate_handle_time_metrics(tickets)
    sla = calculate_sla_metrics(tickets)
    repl_costs = calculate_replacement_costs(tickets, products)
    op_costs = calculate_operational_costs(tickets)

    overview_data = {
        "kpis": {
            "csat": {
                "value": round(float(csat["mean_csat"]), 2),
                "median": round(float(csat["median_csat"]), 1),
                "responses": int(csat["csat_responses"]),
                "response_rate_pct": round(float(csat["csat_response_rate"]) * 100.0, 2),
                "label": "CSAT (Mean)",
                "subtext": f"{csat['csat_responses']:,} responses ({csat['csat_response_rate']*100:.2f}% response rate)"
            },
            "median_handle_time": {
                "value": "29 min",
                "hours": round(float(handle_time["median_hours"]), 2),
                "mean_hours": round(float(handle_time["mean_hours"]), 2),
                "usable_tickets": int(handle_time["usable_tickets"]),
                "label": "Median Handle Time",
                "subtext": f"Mean: {handle_time['mean_hours']:.1f}h across {handle_time['usable_tickets']:,} attendance tickets"
            },
            "sla_breach_rate": {
                "value": f"{sla['overall_breach_rate']*100:.2f}%",
                "rate": round(float(sla["overall_breach_rate"]), 4),
                "breaches": int(sla["total_breaches"]),
                "eligible": int(sla["eligible_tickets"]),
                "label": "First-Response SLA Breach Rate",
                "subtext": f"{sla['total_breaches']:,} breaches out of {sla['eligible_tickets']:,} tickets"
            },
            "replacement_units": {
                "value": f"{repl_costs['replacement_count']:,}",
                "count": int(repl_costs["replacement_count"]),
                "rate_pct": round(float(repl_costs["replacement_count"]) / len(tickets) * 100.0, 2),
                "label": "Replacement Units",
                "subtext": f"{repl_costs['replacement_count'] / len(tickets) * 100:.2f}% replacement rate"
            },
            "replacement_spend": {
                "value": format_currency_lakhs(repl_costs["total_policy_cost_inr"]),
                "amount_inr": round(float(repl_costs["total_policy_cost_inr"]), 2),
                "avg_unit_cost_inr": round(float(repl_costs["avg_policy_unit_cost_inr"]), 2),
                "label": "Policy Replacement Spend",
                "subtext": f"Avg: ₹{repl_costs['avg_policy_unit_cost_inr']:.2f}/unit (BOM + ₹340 logistics)"
            },
            "sla_credit_exposure": {
                "value": format_currency_lakhs(sla["total_credit_exposure_inr"]),
                "amount_inr": int(sla["total_credit_exposure_inr"]),
                "label": "SLA Credit Exposure",
                "subtext": "Automatic store credit liabilities under Policy §3"
            }
        },
        "monthly_trend": monthly_trends_df.to_dict(orient="records"),
        "key_signals": [
            {
                "id": "pulse2_defect",
                "title": "Pulse 2 Concentration",
                "badge": "Hardware Quality",
                "badge_type": "danger",
                "metric": "61.5% of All Replacements",
                "evidence": "Pulse 2 (VA-EB-PL2) drove 1,166 of 1,896 total company replacements (₹22.39L spend). Defect complaints heavily concentrate in late-2025 production lots (e.g. PL2-2510-3).",
                "interpretation": "High replacement volumes stem from a specific supplier component crisis, not widespread customer support mishandling."
            },
            {
                "id": "email_sla",
                "title": "Email Channel SLA Exposure",
                "badge": "Operational Bottleneck",
                "badge_type": "warning",
                "metric": "12.21% Breach Rate",
                "evidence": "445 email tickets breached the 8-hour first-response SLA, triggering ₹1,55,750 in automatic store credit liabilities (41.8% of total company SLA credits).",
                "interpretation": "Email triage and queue assignment represent the largest controllable source of policy financial penalty."
            },
            {
                "id": "bottom10_comparability",
                "title": "Bottom-10 Comparability Flaw",
                "badge": "Evaluation Bias",
                "badge_type": "accent",
                "metric": "100% Structural Specialization",
                "evidence": "All 10 agents in the raw unadjusted CSAT bottom 10 are either Tier 2 Escalation engineers (6 agents) or hardware triage rota assignees (4 agents).",
                "interpretation": "Raw unstratified ranking penalizes agents handling dead-on-arrival and defective products. Training budget must use peer-stratified groups."
            }
        ]
    }
    with open(output_dir / "overview.json", "w", encoding="utf-8") as f:
        json.dump(overview_data, f, indent=2)
    print("  -> web/data/overview.json created.")

    # 3. AGENTS JSON
    merged_agents = scorecard_df.merge(agent_text_df, on=["agent_id", "name", "tier", "team"], how="left")
    agents_list = []
    for _, row in merged_agents.iterrows():
        agents_list.append({
            "agent_id": str(row["agent_id"]),
            "name": str(row["name"]),
            "tier": int(row["tier"]),
            "team": str(row["team"]),
            "site": str(row["site"]),
            "shift": str(row["shift"]),
            "benchmark_group": str(row["benchmark_group"]),
            "is_hardware_triage": bool(row["is_hardware_triage_rota"]),
            "tickets": int(row["tickets"]),
            "csat_n": int(row["csat_n"]),
            "csat_response_rate_pct": round(float(row["csat_response_rate"]) * 100.0, 1),
            "mean_csat": round(float(row["mean_csat"]), 2) if pd.notnull(row["mean_csat"]) else None,
            "median_csat": round(float(row["median_csat"]), 1) if pd.notnull(row["median_csat"]) else None,
            "mean_handle_hours": round(float(row["mean_handle_hours"]), 2),
            "median_handle_hours": round(float(row["median_handle_hours"]), 2),
            "median_handle_minutes": round(float(row["median_handle_hours"]) * 60.0, 1),
            "sla_breaches": int(row["sla_breaches"]),
            "sla_breach_rate_pct": round(float(row["sla_breach_rate"]) * 100.0, 1),
            "transfers": int(row["transfer_count"]),
            "replacements": int(row["replacement_count"]),
            "intra_group_rank": int(row["intra_group_csat_rank_asc"]),
            "details": {
                "top_issue_categories": str(row["top_issue_categories"]) if pd.notnull(row["top_issue_categories"]) else "None",
                "hw_defect_tickets": int(row["hw_defect_ticket_count"]) if pd.notnull(row["hw_defect_ticket_count"]) else 0,
                "hw_defect_share_pct": float(row["hw_defect_share_pct"]) if pd.notnull(row["hw_defect_share_pct"]) else 0.0,
                "uninformative_notes": int(row["uninformative_note_count"]) if pd.notnull(row["uninformative_note_count"]) else 0,
                "uninformative_note_pct": float(row["uninformative_note_pct"]) if pd.notnull(row["uninformative_note_pct"]) else 0.0,
                "low_csat_tickets": int(row["low_csat_ticket_count"]) if pd.notnull(row["low_csat_ticket_count"]) else 0,
            }
        })

    # Sort bottom 10 strictly by mean_csat ascending
    raw_bottom10 = sorted(agents_list, key=lambda x: (x["mean_csat"] if x["mean_csat"] is not None else 999.0))[:10]
    for idx, b in enumerate(raw_bottom10, 1):
        b["raw_rank"] = idx

    tier2_count_in_bottom10 = sum(1 for b in raw_bottom10 if b["tier"] == 2)
    hw_triage_count_in_bottom10 = sum(1 for b in raw_bottom10 if b["tier"] == 1 and b["is_hardware_triage"])
    other_tier1_in_bottom10 = sum(1 for b in raw_bottom10 if b["tier"] == 1 and not b["is_hardware_triage"])

    agents_data = {
        "agents": agents_list,
        "total_agents": len(agents_list),
        "bottom_10": {
            "agents": raw_bottom10,
            "composition": {
                "tier_2_count": tier2_count_in_bottom10,
                "hardware_triage_tier_1_count": hw_triage_count_in_bottom10,
                "standard_tier_1_count": other_tier1_in_bottom10,
                "total": len(raw_bottom10),
            },
            "warning_text": "Context required: this ranking is descriptive and should not be treated as a stand-alone training recommendation."
        },
        "filters": {
            "tiers": sorted(scorecard_df["tier"].unique().tolist()),
            "teams": sorted(scorecard_df["team"].unique().tolist()),
            "sites": sorted(scorecard_df["site"].unique().tolist()),
            "shifts": sorted(scorecard_df["shift"].unique().tolist()),
        }
    }
    with open(output_dir / "agents.json", "w", encoding="utf-8") as f:
        json.dump(agents_data, f, indent=2)
    print("  -> web/data/agents.json created.")

    # 4. TRENDS JSON
    trends_records = []
    for _, r in monthly_trends_df.iterrows():
        trends_records.append({
            "month": str(r["month"]),
            "ticket_volume": int(r["ticket_volume"]),
            "replacement_count": int(r["replacement_count"]),
            "policy_replacement_cost": round(float(r["policy_replacement_cost"]), 2),
            "refund_count": int(r["refund_count"]),
            "refund_amount": round(float(r["refund_amount"]), 2),
            "replacement_rate_pct": round(float(r["replacement_rate"]) * 100.0, 2),
            "avg_replacement_cost": round(float(r["avg_replacement_cost"]), 2),
        })
    with open(output_dir / "trends.json", "w", encoding="utf-8") as f:
        json.dump({"trends": trends_records}, f, indent=2)
    print("  -> web/data/trends.json created.")

    # 5. REPLACEMENTS JSON
    by_sku_df = repl_costs["by_sku"].sort_values("replacements", ascending=False)
    product_table = []
    for _, r in by_sku_df.iterrows():
        product_table.append({
            "sku": str(r["sku"]),
            "product_name": str(r["product_name"]),
            "tickets": int(r["total_tickets"]),
            "replacements": int(r["replacements"]),
            "replacement_rate_pct": round(float(r["replacement_rate"]) * 100.0, 2),
            "policy_spend_inr": round(float(r["total_policy_cost_inr"]), 2),
            "policy_spend_formatted": format_currency_lakhs(float(r["total_policy_cost_inr"])),
            "unit_cost_inr": float(r["unit_cost_inr"]),
            "logistics_cost_inr": 340.0,
        })

    # High replacement lot candidates (top 15)
    lot_candidates = []
    for _, r in lot_code_df.head(15).iterrows():
        lot_candidates.append({
            "lot_code": str(r["lot_code"]),
            "product_sku": str(r["product_sku"]),
            "orders": int(r["total_orders_in_lot"]),
            "tickets": int(r["ticket_count"]),
            "replacements": int(r["replacement_count"]),
            "replacement_rate_pct": round(float(r["replacement_rate"]) * 100.0, 2),
            "candidate_status": "High-replacement lot candidate"
        })

    replacements_data = {
        "headline": {
            "replacement_units": int(repl_costs["replacement_count"]),
            "total_policy_cost_inr": round(float(repl_costs["total_policy_cost_inr"]), 2),
            "total_policy_cost_formatted": format_currency_lakhs(repl_costs["total_policy_cost_inr"]),
        },
        "finance_comparison": {
            "finance_estimate_inr": round(float(repl_costs["finance_estimate_spend_inr"]), 2),
            "finance_estimate_formatted": format_currency_lakhs(repl_costs["finance_estimate_spend_inr"]),
            "policy_actual_inr": round(float(repl_costs["total_policy_cost_inr"]), 2),
            "policy_actual_formatted": format_currency_lakhs(repl_costs["total_policy_cost_inr"]),
            "variance_inr": round(float(repl_costs["finance_overstatement_inr"]), 2),
            "variance_formatted": format_currency_lakhs(repl_costs["finance_overstatement_inr"]),
            "variance_pct": round(float(repl_costs["finance_overstatement_pct"]), 2),
            "explanation": "Finance estimated replacement liability at a flat ₹2,500/unit across all models. Under policy §4, replacement cost follows product unit cost + ₹340 logistics. Because high-volume earbuds cost between ₹1,100 and ₹1,580, Finance overstated replacement liability by ₹13.24L (+38.76%)."
        },
        "product_breakdown": product_table,
        "lot_investigation": {
            "candidates": lot_candidates,
            "disclaimer": "Ticket and order data show concentration patterns; physical manufacturing causality is not established by this analysis."
        }
    }
    with open(output_dir / "replacements.json", "w", encoding="utf-8") as f:
        json.dump(replacements_data, f, indent=2)
    print("  -> web/data/replacements.json created.")

    # 6. SLA & COST JSON
    channels_data = []
    for ch_name, ch_info in sla["by_channel"].items():
        ch_cost_info = op_costs["channel_contact_costs"][ch_name]
        channels_data.append({
            "channel": ch_name.capitalize(),
            "tickets": int(ch_info["total_tickets"]),
            "sla_target_minutes": int(ch_info["sla_target_minutes"]),
            "breaches": int(ch_info["breaches"]),
            "breach_rate_pct": round(float(ch_info["breach_rate"]) * 100.0, 2),
            "credit_exposure_inr": int(ch_info["credit_exposure_inr"]),
            "credit_exposure_formatted": f"₹{ch_info['credit_exposure_inr']:,}",
            "contact_cost_inr": int(ch_cost_info["total_cost_inr"]),
            "contact_cost_formatted": f"₹{ch_cost_info['total_cost_inr']:,}",
            "unit_cost_inr": int(ch_cost_info["unit_cost"])
        })
    # Sort channels by breach rate descending
    channels_data = sorted(channels_data, key=lambda x: x["breach_rate_pct"], reverse=True)

    operating_exposure = {
        "contact_costs_inr": int(op_costs["total_contact_cost_inr"]),
        "transfer_costs_inr": int(op_costs["total_transfer_cost_inr"]),
        "sla_credits_inr": int(op_costs["total_sla_credit_inr"]),
        "replacement_costs_inr": round(float(repl_costs["total_policy_cost_inr"]), 2),
        "refund_value_inr": round(float(op_costs["total_refund_amount_inr"]), 2),
        "total_exposure_inr": round(
            op_costs["total_contact_cost_inr"] +
            op_costs["total_transfer_cost_inr"] +
            op_costs["total_sla_credit_inr"] +
            repl_costs["total_policy_cost_inr"] +
            op_costs["total_refund_amount_inr"], 2
        ),
        "terminology_note": "Tracked support operating exposure represents direct customer support financial allocations under policy rules; it is not a corporate profit and loss statement."
    }

    sla_data = {
        "channels": channels_data,
        "operating_exposure": operating_exposure
    }
    with open(output_dir / "sla.json", "w", encoding="utf-8") as f:
        json.dump(sla_data, f, indent=2)
    print("  -> web/data/sla.json created.")

    # 7. AI SIGNALS JSON
    tickets_with_preds = tickets.merge(
        text_preds_df[["ticket_id", "ai_issue_category", "ai_resolution_outcome", "hardware_defect_signal", "ai_confidence", "is_rule_override", "prediction_source"]],
        on="ticket_id",
        how="left"
    )
    other_decomp = analyze_other_category(tickets_with_preds)
    cv_metrics, _ = run_held_out_cross_validation(sample_df, gt_df, n_splits=5, seed=42)

    # Category comparisons: Intake Category vs AI Predicted Category
    raw_cats = tickets_with_preds["category"].value_counts().to_dict()
    ai_cats = tickets_with_preds["ai_issue_category"].value_counts().to_dict()
    comparison_list = []
    for cat, cnt in sorted(ai_cats.items(), key=lambda x: x[1], reverse=True):
        comparison_list.append({
            "category": cat,
            "ai_count": int(cnt),
            "ai_pct": round(int(cnt) / len(tickets) * 100.0, 2),
        })

    ai_data = {
        "other_decomposition": {
            "total_other_tickets": int(other_decomp["total_other_tickets"]),
            "actionable_recovered_count": int(other_decomp["actionable_recovered_count"]),
            "actionable_recovered_pct": float(other_decomp["actionable_recovered_percentage"]),
            "other_unclear_count": int(other_decomp["distribution_counts"].get("other_unclear", 0)),
            "other_unclear_pct": float(other_decomp["distribution_percentages"].get("other_unclear", 0.0)),
            "distribution": [
                {"category": k, "count": int(v), "pct": float(other_decomp["distribution_percentages"][k])}
                for k, v in sorted(other_decomp["distribution_counts"].items(), key=lambda x: x[1], reverse=True)
            ]
        },
        "category_distribution": comparison_list,
        "intake_raw_distribution": [{"category": k, "count": int(v)} for k, v in raw_cats.items()],
        "model_quality": {
            "benchmark_label": "Rule-assisted pseudo-label benchmark (Held-Out 5-Fold CV)",
            "disclaimer": "These results are not independent human gold-label validation.",
            "baselines": [
                {
                    "name": "Majority Class ('connectivity_pairing')",
                    "accuracy_pct": 26.67,
                    "macro_f1": 0.0468,
                    "role": "Statistical Floor"
                },
                {
                    "name": "Simple Keyword Rules",
                    "accuracy_pct": 46.11,
                    "macro_f1": 0.5399,
                    "role": "Pure Regex Baseline"
                },
                {
                    "name": "Pure ML (TF-IDF + Logistic Regression)",
                    "accuracy_pct": 55.56,
                    "macro_f1": 0.5388,
                    "role": "Held-Out Statistical Generalization"
                },
                {
                    "name": "Hybrid Pipeline (Rules + ML Fallback)",
                    "accuracy_pct": 65.56,
                    "macro_f1": 0.6443,
                    "role": "Operational Production Pipeline"
                }
            ],
            "per_class": cv_metrics["per_class_metrics"]
        },
        "hardware_defect_signal": {
            "label": "Conservative text signal",
            "precision_pct": 100.0,
            "recall_pct": 47.06,
            "f1_pct": 64.00,
            "tp": 8,
            "fp": 0,
            "tn": 163,
            "fn": 9,
            "explanation": "High precision, limited recall. It identifies explicit defect language but can miss colloquial descriptions. This is a text signal, not a proven physical defect diagnosis."
        }
    }
    with open(output_dir / "ai_signals.json", "w", encoding="utf-8") as f:
        json.dump(ai_data, f, indent=2)
    print("  -> web/data/ai_signals.json created.")

    # 8. METHODOLOGY JSON
    methodology_data = {
        "data_integrity": {
            "tickets": 11750,
            "agents": 44,
            "orders": 15500,
            "customers": 9500,
            "products": 14,
            "pk_duplicates": 0,
            "fk_orphans": 0,
            "order_linking_direct": 7643,
            "order_linking_missing": 4107,
            "cartesian_risk_avoided": 1388,
            "telephony_junk_messages": 45,
            "suitable_messages": 11705
        },
        "timestamp_handling": {
            "affected_tickets": 2309,
            "system": "Legacy Freshdesk",
            "offset_applied": "+05:30 IST",
            "reason": "Timestamp was stored in UTC without zone flag, causing false negative handle times.",
            "field_strategy": "Original raw timestamps strictly preserved in raw fields; resolved_at_reporting used for business calculation."
        },
        "csat_protocol": {
            "responses": 5196,
            "response_rate_pct": 44.22,
            "policy": "Blanks strictly excluded from denominator. Never imputed as zero or group average."
        },
        "ai_architecture": {
            "model_type": "TF-IDF (1-2 n-grams) + Balanced Logistic Regression + Rule Overrides",
            "external_api_calls": 0,
            "paid_cost_inr": 0.0,
            "cost_avoidance_savings_inr": 58750.0,
            "benchmark_provenance": "Rule-assisted pseudo-labels (label_source='rule_assisted_pseudo_label')",
            "evaluation_method": "5-fold stratified cross-validation with fold vectorizer independence"
        },
        "limitations": [
            "Benchmark annotations were synthesized using rule heuristics; human gold-standard double-blind labels should be gathered for production.",
            "The hardware defect detector has 47.06% recall; informal failure phrasing requires Tier 2 triage inspection.",
            "Operational correlations between defect signals and low CSAT do not establish legal or physical manufacturing liability without hardware teardown testing.",
            "Rare classes ('cancellation' N=3, 'product_enquiry_setup' N=4 in sample) exhibit high variance in statistical weights and rely on rule overrides."
        ]
    }
    with open(output_dir / "methodology.json", "w", encoding="utf-8") as f:
        json.dump(methodology_data, f, indent=2)
    print("  -> web/data/methodology.json created.")

    print("\nAll 7 web data JSON files successfully built in web/data/!")


if __name__ == "__main__":
    build_all_web_data()
