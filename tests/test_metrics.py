"""Automated tests for CSAT, Handle Time, SLA, and timestamp adjustment logic."""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.metrics import (
    calculate_csat_metrics,
    calculate_handle_time_metrics,
    calculate_sla_metrics,
)
from src.data_loader import load_tickets
from src.config import LEGACY_TIMESTAMP_OFFSET, SLA_TARGET_MINUTES


def test_blank_csat_excluded_not_zero():
    """Verify that blank CSAT scores are excluded from averages and not converted to zero."""
    # 3 tickets: scores 5.0, 3.0, and blank (NaN)
    tickets = pd.DataFrame([
        {"ticket_id": "T1", "status": "resolved", "csat_score": 5.0},
        {"ticket_id": "T2", "status": "resolved", "csat_score": 3.0},
        {"ticket_id": "T3", "status": "resolved", "csat_score": np.nan},
    ])
    
    metrics = calculate_csat_metrics(tickets)
    
    assert metrics["total_tickets"] == 3
    assert metrics["csat_responses"] == 2
    assert metrics["csat_response_rate"] == 2 / 3
    # If blanks were converted to 0, mean would be (5 + 3 + 0) / 3 = 2.67
    # Under policy, mean must be (5 + 3) / 2 = 4.0
    assert metrics["mean_csat"] == 4.0
    assert metrics["median_csat"] == 4.0
    assert metrics["score_distribution"][5]["count"] == 1
    assert metrics["score_distribution"][3]["count"] == 1
    assert metrics["score_distribution"][1]["count"] == 0


def test_handle_time_attendance_only():
    """Verify handle time is only calculated for attendance tickets (resolved/closed), not open/pending."""
    # Create controlled fixture
    tickets = pd.DataFrame([
        {
            "ticket_id": "T1",
            "status": "resolved",
            "handle_time_hours": 2.5,
        },
        {
            "ticket_id": "T2",
            "status": "closed",
            "handle_time_hours": 1.5,
        },
        {
            "ticket_id": "T3",
            "status": "open",
            "handle_time_hours": np.nan,  # Must be NaN for open tickets
        },
        {
            "ticket_id": "T4",
            "status": "pending",
            "handle_time_hours": np.nan,  # Must be NaN for pending tickets
        },
    ])
    
    metrics = calculate_handle_time_metrics(tickets)
    assert metrics["usable_tickets"] == 2
    assert metrics["mean_hours"] == (2.5 + 1.5) / 2.0
    assert metrics["median_hours"] == 2.0


def test_channel_specific_sla_targets_and_breaches():
    """Verify channel SLA targets differ and breaches are properly calculated."""
    # Chat: 15 min, Voice: 120 min, Social: 240 min, Email: 480 min
    tickets = pd.DataFrame([
        # Chat: 20 min response -> Breach (>15m)
        {
            "ticket_id": "T1",
            "channel": "chat",
            "missing_first_response": False,
            "first_response_minutes": 20.0,
            "sla_target_minutes": 15,
            "sla_breach": True,
        },
        # Chat: 10 min response -> No Breach
        {
            "ticket_id": "T2",
            "channel": "chat",
            "missing_first_response": False,
            "first_response_minutes": 10.0,
            "sla_target_minutes": 15,
            "sla_breach": False,
        },
        # Email: 300 min (5h) response -> No Breach (<480m)
        {
            "ticket_id": "T3",
            "channel": "email",
            "missing_first_response": False,
            "first_response_minutes": 300.0,
            "sla_target_minutes": 480,
            "sla_breach": False,
        },
        # Email: 500 min (8.3h) response -> Breach (>480m)
        {
            "ticket_id": "T4",
            "channel": "email",
            "missing_first_response": False,
            "first_response_minutes": 500.0,
            "sla_target_minutes": 480,
            "sla_breach": True,
        },
        # Voice: Missing first response -> NOT a breach, tracked separately
        {
            "ticket_id": "T5",
            "channel": "voice",
            "missing_first_response": True,
            "first_response_minutes": np.nan,
            "sla_target_minutes": 120,
            "sla_breach": False,
        },
    ])
    
    sla_res = calculate_sla_metrics(tickets)
    assert sla_res["total_tickets"] == 5
    assert sla_res["missing_first_response_count"] == 1
    assert sla_res["eligible_tickets"] == 4
    assert sla_res["total_breaches"] == 2
    assert sla_res["overall_breach_rate"] == 2 / 4
    assert sla_res["total_credit_exposure_inr"] == 2 * 350
    
    chat_summary = sla_res["by_channel"]["chat"]
    assert chat_summary["total_tickets"] == 2
    assert chat_summary["breaches"] == 1
    assert chat_summary["breach_rate"] == 0.5


def test_legacy_timestamp_offset_adjustment(tmp_path):
    """Verify that +05:30 offset is applied ONLY to legacy_fd tickets, eliminating negative handle time."""
    # Write a temporary CSV to test load_tickets logic directly
    csv_content = """ticket_id,created_at,first_response_at,resolved_at,status,channel,customer_id,order_id,product_sku,category,priority,assigned_team,agent_id,transfers,csat_score,refund_amount_inr,refund_reason_code,replacement_issued,customer_message,agent_notes,source_system
TK-LEG1,2025-01-01 08:00,2025-01-01 08:30,2025-01-01 03:20,resolved,chat,C1,O1,SKU1,Other,Normal,Chat Frontline,A1,0,4.0,,,N,Hello,Done,legacy_fd
TK-HLP1,2026-01-01 08:00,2026-01-01 08:30,2026-01-01 09:00,resolved,chat,C1,O1,SKU1,Other,Normal,Chat Frontline,A1,0,5.0,,,N,Hello,Done,helpdesk
"""
    test_csv = tmp_path / "test_tickets.csv"
    test_csv.write_text(csv_content, encoding="utf-8")
    
    df = load_tickets(test_csv)
    
    leg_row = df[df["ticket_id"] == "TK-LEG1"].iloc[0]
    hlp_row = df[df["ticket_id"] == "TK-HLP1"].iloc[0]
    
    # 1. Verify raw handle time for legacy was negative: (03:20 - 08:30) = -5 hours 10 mins = -5.167 hrs
    assert leg_row["raw_handle_time_hours"] < 0
    
    # 2. Verify legacy resolved_at_reporting has +05:30 applied: 03:20 UTC + 5:30 = 08:50 IST
    expected_leg_res = pd.to_datetime("2025-01-01 03:20") + timedelta(hours=5, minutes=30)
    assert leg_row["resolved_at_reporting"] == expected_leg_res
    
    # 3. Verify adjusted handle_time_hours is positive: (08:50 - 08:30) = 20 mins = 0.333 hrs
    assert leg_row["handle_time_hours"] > 0
    assert pytest.approx(leg_row["handle_time_hours"], 0.01) == (20.0 / 60.0)
    
    # 4. Verify helpdesk ticket was NOT shifted
    assert hlp_row["resolved_at_reporting"] == pd.to_datetime("2026-01-01 09:00")
    assert pytest.approx(hlp_row["handle_time_hours"], 0.01) == 0.5
    assert bool(hlp_row["legacy_timestamp_adjusted"]) is False
    assert bool(leg_row["legacy_timestamp_adjusted"]) is True
