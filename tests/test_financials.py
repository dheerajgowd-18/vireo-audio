"""Automated tests for financial cost calculations, transfers, and replacement ledgers."""

import pytest
import pandas as pd
import numpy as np

from src.financials import (
    calculate_operational_costs,
    calculate_replacement_costs,
    analyze_lot_code_replacements,
)
from src.config import (
    TRANSFER_COST_INR,
    REPLACEMENT_LOGISTICS_INR,
    CONTACT_COSTS_INR,
    SLA_BREACH_CREDIT_INR,
)


def test_transfer_and_operational_costs():
    """Verify transfer costs (₹305/transfer) and channel contact costs."""
    tickets = pd.DataFrame([
        {"ticket_id": "T1", "channel": "chat", "transfers": 1, "sla_breach": False, "refund_amount_inr": np.nan},
        {"ticket_id": "T2", "channel": "chat", "transfers": 2, "sla_breach": True, "refund_amount_inr": np.nan},
        {"ticket_id": "T3", "channel": "email", "transfers": 0, "sla_breach": True, "refund_amount_inr": 1000.0},
        {"ticket_id": "T4", "channel": "voice", "transfers": 0, "sla_breach": False, "refund_amount_inr": np.nan},
    ])
    
    costs = calculate_operational_costs(tickets)
    
    # 3 total transfers (1 + 2 + 0 + 0) @ ₹305 = ₹915
    assert costs["total_transfers"] == 3
    assert costs["total_transfer_cost_inr"] == 3 * TRANSFER_COST_INR
    assert costs["tickets_with_transfers"] == 2
    
    # Contact costs: 2 chats (2 * 210) + 1 email (260) + 1 voice (520) = 420 + 260 + 520 = 1200
    expected_contact_cost = (2 * CONTACT_COSTS_INR["chat"]) + CONTACT_COSTS_INR["email"] + CONTACT_COSTS_INR["voice"]
    assert costs["total_contact_cost_inr"] == expected_contact_cost
    
    # SLA Breaches: 2 @ ₹350 = ₹700
    assert costs["total_sla_breaches"] == 2
    assert costs["total_sla_credit_inr"] == 2 * SLA_BREACH_CREDIT_INR
    
    # Refund total: 1000.0
    assert costs["refund_ticket_count"] == 1
    assert costs["total_refund_amount_inr"] == 1000.0


def test_replacement_policy_cost_arithmetic():
    """Verify replacement policy cost = unit_cost + ₹340 logistics (not ₹2,500)."""
    products = pd.DataFrame([
        {"sku": "SKU-A", "product_name": "Earbuds A", "family": "earbuds", "unit_cost_inr": 1500},
        {"sku": "SKU-B", "product_name": "Speaker B", "family": "speaker", "unit_cost_inr": 2000},
    ])
    tickets = pd.DataFrame([
        {"ticket_id": "T1", "product_sku": "SKU-A", "replacement_issued": "Y"},
        {"ticket_id": "T2", "product_sku": "SKU-A", "replacement_issued": "Y"},
        {"ticket_id": "T3", "product_sku": "SKU-B", "replacement_issued": "Y"},
        {"ticket_id": "T4", "product_sku": "SKU-B", "replacement_issued": "N"},  # No replacement
    ])
    
    res = calculate_replacement_costs(tickets, products)
    
    assert res["replacement_count"] == 3
    # 2 SKU-A: 2 * (1500 + 340) = 2 * 1840 = 3680
    # 1 SKU-B: 1 * (2000 + 340) = 1 * 2340 = 2340
    # Total Policy Cost = 3680 + 2340 = 6020
    assert res["total_policy_cost_inr"] == 6020.0
    assert pytest.approx(res["avg_policy_unit_cost_inr"], 0.01) == 6020.0 / 3
    
    # Finance estimate: 3 * 2500 = 7500
    assert res["finance_estimate_spend_inr"] == 7500
    assert res["finance_overstatement_inr"] == 7500 - 6020.0


def test_lot_code_analysis_without_fanout():
    """Verify lot code aggregation works cleanly on tickets with direct order_id."""
    orders = pd.DataFrame([
        {"order_id": "O101", "sku": "SKU-A", "lot_code": "LOT-01", "order_date": "2025-10-01"},
        {"order_id": "O102", "sku": "SKU-A", "lot_code": "LOT-01", "order_date": "2025-10-02"},
        {"order_id": "O103", "sku": "SKU-B", "lot_code": "LOT-02", "order_date": "2025-10-03"},
    ])
    tickets = pd.DataFrame([
        {"ticket_id": "T1", "order_id": "O101", "product_sku": "SKU-A", "replacement_issued": "Y"},
        {"ticket_id": "T2", "order_id": "O102", "product_sku": "SKU-A", "replacement_issued": "N"},
        {"ticket_id": "T3", "order_id": None, "product_sku": "SKU-B", "replacement_issued": "Y"},  # Omitted from lot analysis
    ])
    
    lot_df = analyze_lot_code_replacements(tickets, orders)
    
    # Only LOT-01 should be present because T3 had null order_id
    assert len(lot_df) == 1
    row = lot_df.iloc[0]
    assert row["lot_code"] == "LOT-01"
    assert row["ticket_count"] == 2
    assert row["replacement_count"] == 1
    assert row["replacement_rate"] == 0.5
    assert row["candidate_status"] == "high-replacement lot candidate"
