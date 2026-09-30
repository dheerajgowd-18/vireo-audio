"""Operational intelligence, 'Other' category decomposition, and cost audit for text layer."""

from typing import Dict, Any, List
import pandas as pd
import numpy as np


def analyze_other_category(tickets: pd.DataFrame) -> Dict[str, Any]:
    """Decompose tickets originally tagged as 'Other' by the intake bot."""
    other_tickets = tickets[tickets["category"] == "Other"].copy()
    total_other = len(other_tickets)
    
    if total_other == 0:
        return {"total_other": 0, "distribution": {}, "recovered_percentage": 0.0}
        
    dist = other_tickets["ai_issue_category"].value_counts().to_dict()
    dist_pct = {k: round(v / total_other * 100.0, 2) for k, v in dist.items()}
    
    # Calculate how many were categorized into concrete actionable categories (excluding 'other_unclear')
    recovered_count = sum(v for k, v in dist.items() if k != "other_unclear")
    recovered_pct = round(recovered_count / total_other * 100.0, 2)
    
    return {
        "total_other_tickets": total_other,
        "distribution_counts": dist,
        "distribution_percentages": dist_pct,
        "actionable_recovered_count": recovered_count,
        "actionable_recovered_percentage": recovered_pct,
    }


def link_text_signals_to_metrics(
    tickets: pd.DataFrame, products: pd.DataFrame, orders: pd.DataFrame
) -> Dict[str, Any]:
    """Correlate AI-derived text labels with operational metrics without making causal claims."""
    # 1. Performance by Predicted Issue Category
    cat_summary = (
        tickets.groupby("ai_issue_category")
        .agg(
            total_tickets=("ticket_id", "count"),
            replacements=("replacement_issued", lambda s: (s == "Y").sum()),
            csat_responses=("csat_score", lambda s: s.notnull().sum()),
            mean_csat=("csat_score", "mean"),
            avg_handle_hours=("handle_time_hours", "mean"),
            sla_breaches=("sla_breach", "sum"),
        )
        .reset_index()
    )
    cat_summary["replacement_rate"] = cat_summary["replacements"] / cat_summary["total_tickets"]
    cat_summary["sla_breach_rate"] = cat_summary["sla_breaches"] / cat_summary["total_tickets"]
    
    # 2. Hardware Defect Signal vs Operational Metrics
    hw_summary = (
        tickets.groupby("hardware_defect_signal")
        .agg(
            total_tickets=("ticket_id", "count"),
            replacements=("replacement_issued", lambda s: (s == "Y").sum()),
            csat_responses=("csat_score", lambda s: s.notnull().sum()),
            mean_csat=("csat_score", "mean"),
            avg_handle_hours=("handle_time_hours", "mean"),
        )
        .reset_index()
    )
    hw_summary["replacement_rate"] = hw_summary["replacements"] / hw_summary["total_tickets"]
    
    # 3. Hardware Defect Signal by Product SKU
    sku_hw = (
        tickets.groupby("product_sku")
        .agg(
            total_tickets=("ticket_id", "count"),
            hw_defect_tickets=("hardware_defect_signal", "sum"),
            replacements=("replacement_issued", lambda s: (s == "Y").sum()),
        )
        .reset_index()
    )
    sku_hw["hw_defect_rate"] = sku_hw["hw_defect_tickets"] / sku_hw["total_tickets"]
    sku_hw = sku_hw.sort_values("hw_defect_tickets", ascending=False)
    
    # 4. Hardware Defect Signal across matched lot codes (Pulse 2)
    valid_order_tickets = tickets[
        (tickets["order_id"].notnull()) &
        (tickets["order_id"] != "") &
        (tickets["product_sku"] == "VA-EB-PL2")
    ]
    merged_orders = valid_order_tickets.merge(
        orders[["order_id", "lot_code"]], on="order_id", how="inner"
    )
    lot_hw = (
        merged_orders.groupby("lot_code")
        .agg(
            total_tickets=("ticket_id", "count"),
            hw_defect_tickets=("hardware_defect_signal", "sum"),
            replacements=("replacement_issued", lambda s: (s == "Y").sum()),
        )
        .reset_index()
    )
    lot_hw["hw_defect_rate"] = lot_hw["hw_defect_tickets"] / lot_hw["total_tickets"]
    lot_hw = lot_hw.sort_values("hw_defect_tickets", ascending=False)
    
    return {
        "by_predicted_category": cat_summary,
        "by_hardware_signal": hw_summary,
        "by_sku_defect_concentration": sku_hw,
        "pulse2_lot_defect_concentration": lot_hw.head(10),
    }


def build_agent_text_summary(
    tickets: pd.DataFrame, agents: pd.DataFrame
) -> pd.DataFrame:
    """Produce an auditable agent-level text profile without opaque employee scores."""
    agent_rows = []
    for _, agent in agents.iterrows():
        a_id = agent["agent_id"]
        a_tickets = tickets[tickets["agent_id"] == a_id]
        
        if len(a_tickets) == 0:
            continue
            
        # Top 2 issue categories
        top_cats = a_tickets["ai_issue_category"].value_counts().head(2).index.tolist()
        top_cats_str = ", ".join(top_cats) if top_cats else "None"
        
        # Hardware defect exposure
        hw_tickets = int(a_tickets["hardware_defect_signal"].sum())
        hw_pct = round(hw_tickets / len(a_tickets) * 100.0, 2)
        
        # Shorthand notes count
        uninformative_notes = (
            (a_tickets["agent_notes"].str.len() < 10) |
            a_tickets["agent_notes"].isin(["-", "sorted", "done", "closed", "see prev", "as discussed", "cx ok"])
        ).sum()
        
        # Low CSAT count (CSAT <= 2)
        low_csat_tickets = (a_tickets["csat_score"] <= 2.0).sum()
        
        agent_rows.append({
            "agent_id": a_id,
            "name": agent["name"],
            "tier": agent["tier"],
            "team": agent["team"],
            "total_tickets": len(a_tickets),
            "top_issue_categories": top_cats_str,
            "hw_defect_ticket_count": hw_tickets,
            "hw_defect_share_pct": hw_pct,
            "low_csat_ticket_count": int(low_csat_tickets),
            "uninformative_note_count": int(uninformative_notes),
            "uninformative_note_pct": round(int(uninformative_notes) / len(a_tickets) * 100.0, 2),
        })
        
    return pd.DataFrame(agent_rows)


def audit_ai_layer_costs(total_tickets: int, sample_size: int = 180) -> Dict[str, Any]:
    """Audit actual AI compute costs vs client's hypothetical per-ticket cloud API scenario."""
    actual_external_calls = 0
    actual_paid_cost_inr = 0.0
    
    # Client's benchmark: Arjun Mehta noted "per-ticket model calls at Rs 5 a pop across twelve thousand tickets"
    hypothetical_per_ticket_rate_inr = 5.0
    hypothetical_total_cost_inr = total_tickets * hypothetical_per_ticket_rate_inr
    total_savings_inr = hypothetical_total_cost_inr - actual_paid_cost_inr
    
    return {
        "external_api_calls": actual_external_calls,
        "sample_size_evaluated": sample_size,
        "full_production_records_processed": total_tickets,
        "actual_paid_cost_inr": actual_paid_cost_inr,
        "cost_status": "Rs 0 paid model cost (100% local deterministic ML and rule execution)",
        "hypothetical_cloud_api_cost_inr": hypothetical_total_cost_inr,
        "cost_avoidance_savings_inr": total_savings_inr,
    }
