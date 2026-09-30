"""Data quality, referential integrity, and policy compliance anomaly audit."""

from typing import Dict, Any, List
import pandas as pd
import numpy as np


def validate_primary_keys(datasets: Dict[str, pd.DataFrame]) -> Dict[str, Dict[str, Any]]:
    """Validate primary key uniqueness across all five datasets."""
    pk_map = {
        "customers": "customer_id",
        "orders": "order_id",
        "agents": "agent_id",
        "products": "sku",
        "tickets": "ticket_id",
    }
    
    results = {}
    for table_name, pk_col in pk_map.items():
        df = datasets[table_name]
        total_rows = len(df)
        unique_pks = df[pk_col].nunique()
        duplicate_count = total_rows - unique_pks
        is_valid = (duplicate_count == 0)
        
        results[table_name] = {
            "pk_column": pk_col,
            "total_rows": total_rows,
            "unique_pks": unique_pks,
            "duplicate_count": duplicate_count,
            "is_valid": is_valid,
        }
    return results


def validate_foreign_keys(
    tickets: pd.DataFrame,
    agents: pd.DataFrame,
    customers: pd.DataFrame,
    orders: pd.DataFrame,
    products: pd.DataFrame,
) -> Dict[str, Dict[str, Any]]:
    """Check foreign key referential integrity from tickets to parent tables."""
    results = {}
    
    # 1. tickets.agent_id -> agents.agent_id
    agent_ids = set(agents["agent_id"].dropna())
    ticket_agents = set(tickets["agent_id"].dropna())
    unmatched_agents = ticket_agents - agent_ids
    results["agent_fk"] = {
        "source_col": "agent_id",
        "target_table": "agents",
        "total_tickets": len(tickets),
        "unmatched_count": len(unmatched_agents),
        "unmatched_keys": list(unmatched_agents),
        "is_valid": len(unmatched_agents) == 0,
    }
    
    # 2. tickets.customer_id -> customers.customer_id
    customer_ids = set(customers["customer_id"].dropna())
    ticket_customers = set(tickets["customer_id"].dropna())
    unmatched_cust = ticket_customers - customer_ids
    results["customer_fk"] = {
        "source_col": "customer_id",
        "target_table": "customers",
        "total_tickets": len(tickets),
        "unmatched_count": len(unmatched_cust),
        "unmatched_keys": list(unmatched_cust),
        "is_valid": len(unmatched_cust) == 0,
    }
    
    # 3. tickets.product_sku -> products.sku
    product_skus = set(products["sku"].dropna())
    ticket_skus = set(tickets["product_sku"].dropna())
    unmatched_skus = ticket_skus - product_skus
    results["product_fk"] = {
        "source_col": "product_sku",
        "target_table": "products",
        "total_tickets": len(tickets),
        "unmatched_count": len(unmatched_skus),
        "unmatched_keys": list(unmatched_skus),
        "is_valid": len(unmatched_skus) == 0,
    }
    
    # 4. tickets.order_id -> orders.order_id (for non-null order_ids)
    populated_orders = tickets[tickets["order_id"].notnull() & (tickets["order_id"] != "")]
    order_ids = set(orders["order_id"].dropna())
    ticket_order_ids = set(populated_orders["order_id"].dropna())
    unmatched_orders = ticket_order_ids - order_ids
    missing_order_count = tickets["order_id"].isnull().sum() + (tickets["order_id"] == "").sum()
    
    results["order_fk"] = {
        "source_col": "order_id",
        "target_table": "orders",
        "total_tickets": len(tickets),
        "populated_order_tickets": len(populated_orders),
        "missing_order_tickets": int(missing_order_count),
        "unmatched_count": len(unmatched_orders),
        "unmatched_keys": list(unmatched_orders),
        "is_valid": len(unmatched_orders) == 0,
    }
    
    return results


def detect_policy_anomalies(tickets: pd.DataFrame) -> Dict[str, Any]:
    """Detect refund/replacement policy compliance exceptions (Policy §5).
    
    Policy §5: 'In no case is a customer to receive both a refund and a replacement
    for the same order; where this happens in error it must be escalated to the
    Team Lead and Finance the same day.'
    """
    # A. Same ticket has both replacement and refund
    same_ticket_mask = (tickets["replacement_issued"] == "Y") & tickets["refund_amount_inr"].notnull()
    same_ticket_anomalies = tickets[same_ticket_mask]
    
    # B. Same order across multiple tickets has both replacement and refund
    valid_order_tickets = tickets[tickets["order_id"].notnull() & (tickets["order_id"] != "")]
    order_summary = valid_order_tickets.groupby("order_id").agg(
        has_replacement=("replacement_issued", lambda s: (s == "Y").any()),
        has_refund=("refund_amount_inr", lambda s: s.notnull().any()),
        ticket_count=("ticket_id", "count"),
    )
    same_order_anomalies = order_summary[order_summary["has_replacement"] & order_summary["has_refund"]]
    
    return {
        "same_ticket_count": int(len(same_ticket_anomalies)),
        "same_ticket_ids": same_ticket_anomalies["ticket_id"].tolist(),
        "same_order_count": int(len(same_order_anomalies)),
        "same_order_ids": same_order_anomalies.index.tolist(),
        "description": "Policy compliance exceptions requiring review (not fraud accusations)",
    }


def analyze_order_fallback_risks(orders: pd.DataFrame, tickets: pd.DataFrame) -> Dict[str, Any]:
    """Analyze Cartesian fan-out risk if fallback join (customer_id + sku) is used."""
    cust_sku_orders = orders.groupby(["customer_id", "sku"]).size()
    multi_order_pairs = cust_sku_orders[cust_sku_orders > 1]
    
    missing_order_tickets = tickets[tickets["order_id"].isnull() | (tickets["order_id"] == "")]
    
    return {
        "total_orders": len(orders),
        "unique_customer_sku_pairs": len(cust_sku_orders),
        "multi_order_pairs_count": len(multi_order_pairs),
        "max_orders_for_single_pair": int(cust_sku_orders.max()) if len(cust_sku_orders) > 0 else 0,
        "tickets_missing_order_id": len(missing_order_tickets),
        "risk_explanation": (
            f"There are {len(multi_order_pairs)} (customer_id, sku) pairs with multiple orders in orders.csv "
            f"(up to {cust_sku_orders.max()}). A naive fallback join would cause duplicate ticket rows."
        ),
    }


def audit_text_diagnostics(tickets: pd.DataFrame) -> Dict[str, Any]:
    """Deterministic diagnostics of customer_message and agent_notes."""
    cust_len_chars = tickets["customer_message"].str.len().fillna(0)
    cust_len_words = tickets["customer_message"].apply(lambda s: len(str(s).split()))
    
    agent_len_chars = tickets["agent_notes"].str.len().fillna(0)
    agent_len_words = tickets["agent_notes"].apply(lambda s: len(str(s).split()))
    
    # Telephony and placeholder markers
    ivr_bracket_mask = tickets["customer_message"].str.contains(
        r"\[line dropped\]|\[inaudible\]|\[crosstalk\]|hello hello can you hear",
        regex=True,
        case=False,
        na=False,
    )
    short_placeholder_mask = (cust_len_chars < 15) | (cust_len_words <= 2)
    unsuitable_cust_msgs = tickets[ivr_bracket_mask | short_placeholder_mask]
    
    uninformative_notes_mask = (
        (agent_len_chars < 10) |
        tickets["agent_notes"].isin(["-", "sorted", "done", "closed", "see prev", "as discussed", "cx ok"])
    )
    
    return {
        "customer_message_stats": {
            "mean_chars": float(cust_len_chars.mean()),
            "median_chars": float(cust_len_chars.median()),
            "mean_words": float(cust_len_words.mean()),
            "median_words": float(cust_len_words.median()),
            "empty_or_null_count": int((cust_len_chars == 0).sum()),
        },
        "agent_notes_stats": {
            "mean_chars": float(agent_len_chars.mean()),
            "median_chars": float(agent_len_chars.median()),
            "mean_words": float(agent_len_words.mean()),
            "median_words": float(agent_len_words.median()),
            "empty_or_null_count": int((agent_len_chars == 0).sum()),
            "uninformative_shorthand_count": int(uninformative_notes_mask.sum()),
        },
        "telephony_ivr_junk_count": int(ivr_bracket_mask.sum()),
        "total_unsuitable_customer_messages": int(len(unsuitable_cust_msgs)),
        "suitable_customer_messages": int(len(tickets) - len(unsuitable_cust_msgs)),
    }
