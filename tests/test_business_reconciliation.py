"""Regression tests for business case numerical reconciliation."""

import json
from pathlib import Path
import pandas as pd
import pytest

from src.data_loader import load_tickets, load_agents, load_products, load_orders


@pytest.fixture(scope="module")
def data():
    tickets = load_tickets()
    agents = load_agents()
    products = load_products()
    orders = load_orders()
    scorecard = pd.read_csv("reports/agent_scorecard.csv")
    return {
        "tickets": tickets,
        "agents": agents,
        "products": products,
        "orders": orders,
        "scorecard": scorecard,
    }


def test_valid_handle_time_tickets_only(data):
    """Ensure handle time calculations strictly use valid attendance tickets with non-negative handle times."""
    tickets = data["tickets"]
    valid_mask = (
        tickets["status"].isin(["resolved", "closed"]) &
        tickets["first_response_dt"].notnull() &
        tickets["resolved_at_reporting"].notnull() &
        (tickets["handle_time_hours"] >= 0)
    )
    valid_tickets = tickets[valid_mask]
    assert len(valid_tickets) == 11183
    assert (valid_tickets["handle_time_hours"] >= 0).all()


def test_open_pending_tickets_excluded_from_handle_time(data):
    """Ensure open and pending tickets cannot contribute to handle hours."""
    tickets = data["tickets"]
    non_attendance = tickets[~tickets["status"].isin(["resolved", "closed"])]
    assert len(non_attendance) == 567
    assert non_attendance["handle_time_hours"].isna().all()


def test_team_median_benchmark_calculated_from_agent_means(data):
    """Ensure team benchmarks are computed from agent mean handle times within valid tickets."""
    tickets = data["tickets"]
    scorecard = data["scorecard"]
    
    ticket_agent = tickets.merge(
        scorecard[["agent_id", "team"]], 
        on="agent_id", 
        how="left"
    )
    valid = ticket_agent[
        tickets["status"].isin(["resolved", "closed"]) &
        tickets["first_response_dt"].notnull() &
        tickets["resolved_at_reporting"].notnull() &
        (tickets["handle_time_hours"] >= 0)
    ]
    
    # Chat Frontline
    chat_valid = valid[valid["team"] == "Chat Frontline"]
    chat_agent_means = chat_valid.groupby("agent_id")["handle_time_hours"].mean()
    assert len(chat_agent_means) == 15
    assert round(chat_agent_means.median(), 4) == 3.8128
    
    # Email Frontline
    email_valid = valid[valid["team"] == "Email Frontline"]
    email_agent_means = email_valid.groupby("agent_id")["handle_time_hours"].mean()
    assert len(email_agent_means) == 7
    assert round(email_agent_means.median(), 4) == 7.0737


def test_capacity_value_calculation(data):
    """Ensure quarterly capacity value = quarterly excess hours * 165 INR."""
    tickets = data["tickets"]
    scorecard = data["scorecard"]
    
    ticket_agent = tickets.merge(
        scorecard[["agent_id", "team"]], 
        on="agent_id", 
        how="left"
    )
    valid = ticket_agent[
        tickets["status"].isin(["resolved", "closed"]) &
        tickets["first_response_dt"].notnull() &
        tickets["resolved_at_reporting"].notnull() &
        (tickets["handle_time_hours"] >= 0)
    ]
    
    # Chat
    chat = valid[valid["team"] == "Chat Frontline"]
    chat_means = chat.groupby("agent_id")["handle_time_hours"].mean()
    med_chat = chat_means.median()
    above_chat_ids = chat_means[chat_means > med_chat].index
    chat_above = chat[chat["agent_id"].isin(above_chat_ids)]
    excess_chat = chat_above["handle_time_hours"].sum() - (len(chat_above) * med_chat)
    
    # Email
    email = valid[valid["team"] == "Email Frontline"]
    email_means = email.groupby("agent_id")["handle_time_hours"].mean()
    med_email = email_means.median()
    above_email_ids = email_means[email_means > med_email].index
    email_above = email[email["agent_id"].isin(above_email_ids)]
    excess_email = email_above["handle_time_hours"].sum() - (len(email_above) * med_email)
    
    total_excess = excess_chat + excess_email
    qtr_excess = total_excess / 6.0
    qtr_capacity_value = qtr_excess * 165.0
    
    assert round(qtr_excess, 2) == 624.86
    assert round(qtr_capacity_value, 2) == 103101.59


def test_pulse2_replacement_cost_arithmetic(data):
    """Ensure Pulse 2 replacement unit cost = 1480 + 340 = 1820 INR, total = 21,22,120 INR."""
    products = data["products"]
    tickets = data["tickets"]
    
    pl2 = products[products["sku"] == "VA-EB-PL2"].iloc[0]
    unit_cost = pl2["unit_cost_inr"]
    policy_cost_per_unit = unit_cost + 340
    
    assert unit_cost == 1480
    assert policy_cost_per_unit == 1820
    
    pl2_replacements = tickets[
        (tickets["product_sku"] == "VA-EB-PL2") &
        (tickets["replacement_issued"] == "Y")
    ]
    assert len(pl2_replacements) == 1166
    total_spend = len(pl2_replacements) * policy_cost_per_unit
    assert total_spend == 2122120.0


def test_lot_pl2_2510_3_replacement_count(data):
    """Ensure lot PL2-2510-3 has exactly 70 replacements on direct order join, NOT 730."""
    tickets = data["tickets"]
    orders = data["orders"]
    
    tickets_with_order = tickets[tickets["order_id"].notnull()]
    merged = tickets_with_order.merge(
        orders[["order_id", "lot_code"]],
        on="order_id",
        how="inner"
    )
    lot_df = merged[merged["lot_code"] == "PL2-2510-3"]
    repl_count = (lot_df["replacement_issued"] == "Y").sum()
    
    assert len(lot_df) == 171
    assert repl_count == 70
    assert round(repl_count / len(lot_df) * 100, 2) == 40.94


def test_note_quality_reconciliation(data):
    """Ensure note quality denominator is 11,750 and shorthand count is exactly 908 (7.73%)."""
    tickets = data["tickets"]
    notes = tickets["agent_notes"].fillna("")
    
    mask_908 = (notes.str.split().str.len() <= 2) | (notes.str.len() <= 9)
    assert len(tickets) == 11750
    assert mask_908.sum() == 908
    assert round(mask_908.mean() * 100, 2) == 7.73


def test_web_data_pulse2_figure_consistency():
    """Ensure overview.json and replacements.json match canonical 21.22L spend."""
    with open("web/data/overview.json", encoding="utf-8") as f:
        overview = json.load(f)
    pulse2_card = next(c for c in overview["key_signals"] if c["id"] == "pulse2_defect")
    assert "₹21.22L spend" in pulse2_card["evidence"]
    
    with open("web/data/replacements.json", encoding="utf-8") as f:
        replacements = json.load(f)
    pl2_row = next(p for p in replacements["product_breakdown"] if p["sku"] == "VA-EB-PL2")
    assert pl2_row["policy_spend_inr"] == 2122120.0
