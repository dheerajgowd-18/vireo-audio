"""Core metrics engine: CSAT, Handle Time, SLA Breaches, and Monthly Trends."""

from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

from .config import SLA_BREACH_CREDIT_INR, ATTENDANCE_STATUSES


def calculate_csat_metrics(tickets: pd.DataFrame) -> Dict[str, Any]:
    """Calculate CSAT metrics strictly adhering to Policy §8.
    
    Rule: Blank scores MUST be excluded from averages, not treated as zero.
    """
    total_tickets = len(tickets)
    valid_csat = tickets["csat_score"].dropna()
    csat_count = len(valid_csat)
    response_rate = csat_count / total_tickets if total_tickets > 0 else 0.0
    
    # Attendance tickets (resolved + closed)
    attendance_tickets = tickets[tickets["status"].isin(ATTENDANCE_STATUSES)]
    att_csat = attendance_tickets["csat_score"].dropna()
    att_response_rate = len(att_csat) / len(attendance_tickets) if len(attendance_tickets) > 0 else 0.0
    
    score_dist = {}
    for score in [1.0, 2.0, 3.0, 4.0, 5.0]:
        count = int((valid_csat == score).sum())
        pct = (count / csat_count * 100.0) if csat_count > 0 else 0.0
        score_dist[int(score)] = {"count": count, "percentage": round(pct, 2)}
    
    return {
        "total_tickets": total_tickets,
        "csat_responses": csat_count,
        "csat_response_rate": float(response_rate),
        "attendance_tickets": len(attendance_tickets),
        "attendance_csat_response_rate": float(att_response_rate),
        "mean_csat": float(valid_csat.mean()) if csat_count > 0 else np.nan,
        "median_csat": float(valid_csat.median()) if csat_count > 0 else np.nan,
        "std_csat": float(valid_csat.std()) if csat_count > 1 else np.nan,
        "score_distribution": score_dist,
    }


def calculate_handle_time_metrics(tickets: pd.DataFrame) -> Dict[str, Any]:
    """Calculate handle time metrics from first response to reporting resolution."""
    valid_ht = tickets["handle_time_hours"].dropna()
    usable_count = len(valid_ht)
    
    if usable_count == 0:
        return {
            "usable_tickets": 0,
            "mean_hours": np.nan,
            "median_hours": np.nan,
            "p25_hours": np.nan,
            "p75_hours": np.nan,
            "std_hours": np.nan,
            "min_hours": np.nan,
            "max_hours": np.nan,
        }
    
    return {
        "usable_tickets": usable_count,
        "mean_hours": float(valid_ht.mean()),
        "median_hours": float(valid_ht.median()),
        "p25_hours": float(valid_ht.quantile(0.25)),
        "p75_hours": float(valid_ht.quantile(0.75)),
        "std_hours": float(valid_ht.std()),
        "min_hours": float(valid_ht.min()),
        "max_hours": float(valid_ht.max()),
    }


def calculate_sla_metrics(tickets: pd.DataFrame) -> Dict[str, Any]:
    """Calculate channel-specific first response SLA breaches and credit exposure."""
    total_tickets = len(tickets)
    missing_resp_count = int(tickets["missing_first_response"].sum())
    
    eligible_tickets = tickets[~tickets["missing_first_response"]]
    breaches_count = int(eligible_tickets["sla_breach"].sum())
    overall_breach_rate = breaches_count / len(eligible_tickets) if len(eligible_tickets) > 0 else 0.0
    total_credit_exposure_inr = breaches_count * SLA_BREACH_CREDIT_INR
    
    channel_summary = {}
    for ch, grp in tickets.groupby("channel"):
        ch_eligible = grp[~grp["missing_first_response"]]
        ch_breaches = int(ch_eligible["sla_breach"].sum())
        ch_rate = ch_breaches / len(ch_eligible) if len(ch_eligible) > 0 else 0.0
        ch_target = grp["sla_target_minutes"].iloc[0] if len(grp) > 0 else np.nan
        
        channel_summary[str(ch)] = {
            "total_tickets": len(grp),
            "eligible_tickets": len(ch_eligible),
            "breaches": ch_breaches,
            "breach_rate": float(ch_rate),
            "sla_target_minutes": int(ch_target) if pd.notnull(ch_target) else None,
            "credit_exposure_inr": ch_breaches * SLA_BREACH_CREDIT_INR,
        }
        
    return {
        "total_tickets": total_tickets,
        "missing_first_response_count": missing_resp_count,
        "eligible_tickets": len(eligible_tickets),
        "total_breaches": breaches_count,
        "overall_breach_rate": float(overall_breach_rate),
        "total_credit_exposure_inr": total_credit_exposure_inr,
        "by_channel": channel_summary,
    }


def calculate_monthly_trends(tickets: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    """Generate monthly metrics from Jan 2025 through Jun 2026."""
    # Join with products to calculate policy replacement cost
    tp = tickets.merge(
        products[["sku", "unit_cost_inr"]],
        left_on="product_sku",
        right_on="sku",
        how="left",
    )
    
    tp["month"] = tp["created_dt"].dt.to_period("M").astype(str)
    tp["is_replacement"] = (tp["replacement_issued"] == "Y")
    tp["policy_replacement_cost"] = np.where(
        tp["is_replacement"], tp["unit_cost_inr"] + 340, 0.0
    )
    tp["has_refund"] = tp["refund_amount_inr"].notnull()
    tp["refund_val"] = tp["refund_amount_inr"].fillna(0.0)
    
    monthly = tp.groupby("month").agg(
        ticket_volume=("ticket_id", "count"),
        replacement_count=("is_replacement", "sum"),
        policy_replacement_cost=("policy_replacement_cost", "sum"),
        refund_count=("has_refund", "sum"),
        refund_amount=("refund_val", "sum"),
    ).reset_index()
    
    monthly["replacement_rate"] = monthly["replacement_count"] / monthly["ticket_volume"]
    monthly["avg_replacement_cost"] = np.where(
        monthly["replacement_count"] > 0,
        monthly["policy_replacement_cost"] / monthly["replacement_count"],
        0.0
    )
    return monthly
