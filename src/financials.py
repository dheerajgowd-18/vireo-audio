"""Financial cost accounting: policy replacement costs, transfers, contact costs, and lot analysis."""

from typing import Dict, Any
import pandas as pd
import numpy as np

from .config import (
    CONTACT_COSTS_INR,
    TRANSFER_COST_INR,
    REPLACEMENT_LOGISTICS_INR,
    SLA_BREACH_CREDIT_INR,
)


def calculate_operational_costs(tickets: pd.DataFrame) -> Dict[str, Any]:
    """Calculate operational costs across contacts, transfers, and SLA breach credits."""
    # Contact costs by channel
    channel_counts = tickets["channel"].value_counts().to_dict()
    channel_costs = {}
    total_contact_cost = 0
    
    for ch, count in channel_counts.items():
        unit_cost = CONTACT_COSTS_INR.get(ch, 290)
        spend = count * unit_cost
        channel_costs[ch] = {"volume": int(count), "unit_cost": unit_cost, "total_cost_inr": spend}
        total_contact_cost += spend
        
    # Transfer costs: transfers * 305
    total_transfers = int(tickets["transfers"].sum())
    tickets_with_transfers = int((tickets["transfers"] > 0).sum())
    total_transfer_cost = total_transfers * TRANSFER_COST_INR
    
    # SLA Breach Credits: breaches * 350
    breaches = int(tickets["sla_breach"].sum())
    total_sla_credit = breaches * SLA_BREACH_CREDIT_INR
    
    # Refunds
    total_refund_spend = float(tickets["refund_amount_inr"].fillna(0.0).sum())
    refund_count = int(tickets["refund_amount_inr"].notnull().sum())
    
    return {
        "channel_contact_costs": channel_costs,
        "total_contact_cost_inr": total_contact_cost,
        "total_transfers": total_transfers,
        "tickets_with_transfers": tickets_with_transfers,
        "total_transfer_cost_inr": total_transfer_cost,
        "total_sla_breaches": breaches,
        "total_sla_credit_inr": total_sla_credit,
        "refund_ticket_count": refund_count,
        "total_refund_amount_inr": total_refund_spend,
    }


def calculate_replacement_costs(
    tickets: pd.DataFrame, products: pd.DataFrame
) -> Dict[str, Any]:
    """Calculate policy replacement spend vs Finance rule-of-thumb estimate."""
    initial_ticket_count = len(tickets)
    
    # Direct join to products table
    merged = tickets.merge(
        products[["sku", "product_name", "family", "unit_cost_inr"]],
        left_on="product_sku",
        right_on="sku",
        how="left",
    )
    
    # Validate ticket row count invariance
    if len(merged) != initial_ticket_count:
        raise ValueError(
            f"Row count mismatch in tickets-product join: original {initial_ticket_count}, "
            f"merged {len(merged)}"
        )
        
    replacements = merged[merged["replacement_issued"] == "Y"].copy()
    replacements["policy_unit_cost"] = replacements["unit_cost_inr"] + REPLACEMENT_LOGISTICS_INR
    
    total_replacement_count = len(replacements)
    total_policy_spend = float(replacements["policy_unit_cost"].sum())
    avg_replacement_cost = (
        total_policy_spend / total_replacement_count if total_replacement_count > 0 else 0.0
    )
    
    # Finance rule-of-thumb comparison (@ ₹2,500)
    finance_estimate_spend = total_replacement_count * 2500
    finance_overestimate_inr = finance_estimate_spend - total_policy_spend
    finance_overestimate_pct = (
        (finance_overestimate_inr / total_policy_spend * 100.0) if total_policy_spend > 0 else 0.0
    )
    
    # By SKU breakdown
    sku_summary = (
        replacements.groupby(["sku", "product_name", "family"])
        .agg(
            replacements=("ticket_id", "count"),
            unit_cost_inr=("unit_cost_inr", "first"),
            total_policy_cost_inr=("policy_unit_cost", "sum"),
        )
        .reset_index()
    )
    # Calculate SKU replacement rate against total tickets for that SKU
    sku_total_tickets = merged.groupby("sku").size().to_dict()
    sku_summary["total_tickets"] = sku_summary["sku"].map(sku_total_tickets)
    sku_summary["replacement_rate"] = sku_summary["replacements"] / sku_summary["total_tickets"]
    sku_summary = sku_summary.sort_values("replacements", ascending=False)
    
    return {
        "replacement_count": total_replacement_count,
        "total_policy_cost_inr": total_policy_spend,
        "avg_policy_unit_cost_inr": float(avg_replacement_cost),
        "finance_estimate_spend_inr": finance_estimate_spend,
        "finance_overstatement_inr": float(finance_overestimate_inr),
        "finance_overstatement_pct": float(finance_overestimate_pct),
        "by_sku": sku_summary,
    }


def analyze_lot_code_replacements(
    tickets: pd.DataFrame, orders: pd.DataFrame
) -> pd.DataFrame:
    """Analyze replacement frequency across manufacturing lot codes using direct order_id matches.
    
    Constraint: Evaluated ONLY where ticket.order_id is populated to prevent Cartesian duplication.
    """
    valid_order_tickets = tickets[tickets["order_id"].notnull() & (tickets["order_id"] != "")].copy()
    
    # 1:1 merge on order_id
    merged = valid_order_tickets.merge(
        orders[["order_id", "lot_code", "order_date"]],
        on="order_id",
        how="inner",
    )
    
    lot_summary = (
        merged.groupby(["lot_code", "product_sku"])
        .agg(
            ticket_count=("ticket_id", "count"),
            replacement_count=("replacement_issued", lambda s: (s == "Y").sum()),
        )
        .reset_index()
    )
    lot_summary["replacement_rate"] = lot_summary["replacement_count"] / lot_summary["ticket_count"]
    
    # Total orders per lot for context
    lot_order_counts = orders.groupby(["lot_code", "sku"]).size().to_dict()
    lot_summary["total_orders_in_lot"] = lot_summary.apply(
        lambda r: lot_order_counts.get((r["lot_code"], r["product_sku"]), np.nan), axis=1
    )
    
    lot_summary["candidate_status"] = np.where(
        lot_summary["replacement_rate"] >= 0.25,
        "high-replacement lot candidate",
        "standard lot",
    )
    return lot_summary.sort_values("replacement_count", ascending=False)
