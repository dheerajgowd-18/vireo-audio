"""Automated tests for data loading, quality, referential integrity, and anomaly detection."""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.data_quality import (
    validate_primary_keys,
    validate_foreign_keys,
    detect_policy_anomalies,
    analyze_order_fallback_risks,
)
from src.agent_analysis import build_agent_scorecard
from src.financials import calculate_replacement_costs


def test_primary_key_uniqueness():
    """Verify primary key uniqueness detection on controlled datasets."""
    datasets = {
        "customers": pd.DataFrame({"customer_id": ["C1", "C2", "C3"]}),
        "orders": pd.DataFrame({"order_id": ["O1", "O2", "O3"]}),
        "agents": pd.DataFrame({"agent_id": ["A1", "A2", "A3"]}),
        "products": pd.DataFrame({"sku": ["SKU1", "SKU2"]}),
        "tickets": pd.DataFrame({"ticket_id": ["T1", "T2", "T3"]}),
    }
    results = validate_primary_keys(datasets)
    for table, res in results.items():
        assert res["is_valid"] is True
        assert res["duplicate_count"] == 0


def test_duplicate_display_names_remain_distinct():
    """Verify two agents with the exact same display name are not merged."""
    agents = pd.DataFrame([
        {"agent_id": "A3006", "name": "Kavya Pandey", "site": "Indore", "team": "Chat Frontline", "shift": "Morning", "tier": 1},
        {"agent_id": "A3029", "name": "Kavya Pandey", "site": "Bengaluru", "team": "Logistics", "shift": "Morning", "tier": 1},
    ])
    tickets = pd.DataFrame([
        {"ticket_id": "T1", "agent_id": "A3006", "csat_score": 4.0, "handle_time_hours": 2.0, "status": "resolved", "transfers": 0, "sla_breach": False, "replacement_issued": "N"},
        {"ticket_id": "T2", "agent_id": "A3006", "csat_score": 5.0, "handle_time_hours": 3.0, "status": "resolved", "transfers": 0, "sla_breach": False, "replacement_issued": "N"},
        {"ticket_id": "T3", "agent_id": "A3029", "csat_score": 2.0, "handle_time_hours": 10.0, "status": "resolved", "transfers": 1, "sla_breach": True, "replacement_issued": "Y"},
    ])
    
    scorecard = build_agent_scorecard(tickets, agents)
    
    # Assert two separate rows are preserved
    assert len(scorecard) == 2
    row_3006 = scorecard[scorecard["agent_id"] == "A3006"].iloc[0]
    row_3029 = scorecard[scorecard["agent_id"] == "A3029"].iloc[0]
    
    assert row_3006["tickets"] == 2
    assert row_3006["mean_csat"] == (4.0 + 5.0) / 2.0
    assert row_3029["tickets"] == 1
    assert row_3029["mean_csat"] == 2.0
    assert row_3006["name"] == row_3029["name"] == "Kavya Pandey"


def test_foreign_key_validation():
    """Verify detection of orphaned foreign keys."""
    agents = pd.DataFrame({"agent_id": ["A1", "A2"]})
    customers = pd.DataFrame({"customer_id": ["C1", "C2"]})
    products = pd.DataFrame({"sku": ["SKU1"]})
    orders = pd.DataFrame({"order_id": ["O1", "O2"]})
    
    # Ticket T2 has an invalid agent_id "A999"
    tickets = pd.DataFrame([
        {"ticket_id": "T1", "agent_id": "A1", "customer_id": "C1", "product_sku": "SKU1", "order_id": "O1"},
        {"ticket_id": "T2", "agent_id": "A999", "customer_id": "C2", "product_sku": "SKU1", "order_id": "O2"},
    ])
    
    results = validate_foreign_keys(tickets, agents, customers, orders, products)
    assert results["agent_fk"]["is_valid"] is False
    assert results["agent_fk"]["unmatched_count"] == 1
    assert "A999" in results["agent_fk"]["unmatched_keys"]
    assert results["customer_fk"]["is_valid"] is True
    assert results["product_fk"]["is_valid"] is True
    assert results["order_fk"]["is_valid"] is True


def test_detect_policy_anomalies_same_ticket_and_order():
    """Verify detection of dual refund and replacement policy compliance exceptions."""
    tickets = pd.DataFrame([
        # Clean replacement
        {"ticket_id": "T1", "order_id": "O1", "replacement_issued": "Y", "refund_amount_inr": np.nan},
        # Clean refund
        {"ticket_id": "T2", "order_id": "O2", "replacement_issued": "N", "refund_amount_inr": 1500.0},
        # Same ticket exception
        {"ticket_id": "T3", "order_id": "O3", "replacement_issued": "Y", "refund_amount_inr": 2000.0},
        # Same order across tickets exception (order O4 has both T4 and T5)
        {"ticket_id": "T4", "order_id": "O4", "replacement_issued": "Y", "refund_amount_inr": np.nan},
        {"ticket_id": "T5", "order_id": "O4", "replacement_issued": "N", "refund_amount_inr": 1200.0},
    ])
    
    anomalies = detect_policy_anomalies(tickets)
    assert anomalies["same_ticket_count"] == 1
    assert anomalies["same_ticket_ids"] == ["T3"]
    assert anomalies["same_order_count"] == 2  # O3 (from T3) and O4 (from T4+T5)
    assert set(anomalies["same_order_ids"]) == {"O3", "O4"}


def test_order_join_fanout_risk_detection():
    """Verify that multiple orders for the same (customer, sku) are detected to prevent fan-out."""
    orders = pd.DataFrame([
        {"order_id": "O1", "customer_id": "C1", "sku": "SKU1"},
        {"order_id": "O2", "customer_id": "C1", "sku": "SKU1"},  # Repeat purchase
        {"order_id": "O3", "customer_id": "C2", "sku": "SKU2"},
    ])
    tickets = pd.DataFrame([
        {"ticket_id": "T1", "order_id": None, "customer_id": "C1", "product_sku": "SKU1"},
    ])
    
    risk_report = analyze_order_fallback_risks(orders, tickets)
    assert risk_report["multi_order_pairs_count"] == 1
    assert risk_report["max_orders_for_single_pair"] == 2
    assert risk_report["tickets_missing_order_id"] == 1


def test_ticket_row_count_invariance_on_product_join():
    """Verify that joining products to tickets preserves the exact ticket row count."""
    products = pd.DataFrame([
        {"sku": "SKU1", "product_name": "P1", "family": "earbuds", "unit_cost_inr": 1000},
        {"sku": "SKU2", "product_name": "P2", "family": "speaker", "unit_cost_inr": 2000},
    ])
    tickets = pd.DataFrame([
        {"ticket_id": "T1", "product_sku": "SKU1", "replacement_issued": "Y"},
        {"ticket_id": "T2", "product_sku": "SKU2", "replacement_issued": "N"},
        {"ticket_id": "T3", "product_sku": "SKU1", "replacement_issued": "Y"},
    ])
    
    res = calculate_replacement_costs(tickets, products)
    assert res["replacement_count"] == 2
    # Product cost: (1000 + 340) * 2 = 2680
    assert res["total_policy_cost_inr"] == (1000 + 340) * 2
