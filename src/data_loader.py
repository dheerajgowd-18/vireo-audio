"""Data loaders for Vireo Audio support datasets with safe derivation of reporting fields."""

from pathlib import Path
from typing import Dict, Optional, Union
import pandas as pd
import numpy as np

from .config import (
    resolve_data_file,
    LEGACY_TIMESTAMP_OFFSET,
    SLA_TARGET_MINUTES,
    ATTENDANCE_STATUSES,
)


def load_customers(filepath: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """Load and validate customers.csv."""
    path = Path(filepath) if filepath else resolve_data_file("customers.csv")
    if not path.exists():
        raise FileNotFoundError(f"Customers file not found at {path}")
    
    df = pd.read_csv(
        path,
        dtype={
            "customer_id": "string",
            "name": "string",
            "city": "string",
            "state": "string",
            "care_plus": "string",
        },
    )
    required_cols = {"customer_id", "name", "city", "state", "signup_date", "care_plus"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in customers.csv: {missing}")
    
    df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
    df["care_plus"] = df["care_plus"].str.strip().str.upper()
    return df


def load_orders(filepath: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """Load and validate orders.csv."""
    path = Path(filepath) if filepath else resolve_data_file("orders.csv")
    if not path.exists():
        raise FileNotFoundError(f"Orders file not found at {path}")
    
    df = pd.read_csv(
        path,
        dtype={
            "order_id": "string",
            "customer_id": "string",
            "sku": "string",
            "channel": "string",
            "qty": "int64",
            "order_value_inr": "int64",
            "lot_code": "string",
        },
    )
    required_cols = {
        "order_id", "customer_id", "sku", "order_date",
        "channel", "qty", "order_value_inr", "lot_code"
    }
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in orders.csv: {missing}")
    
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    return df


def load_agents(filepath: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """Load and validate agents.csv."""
    path = Path(filepath) if filepath else resolve_data_file("agents.csv")
    if not path.exists():
        raise FileNotFoundError(f"Agents file not found at {path}")
    
    df = pd.read_csv(
        path,
        dtype={
            "agent_id": "string",
            "name": "string",
            "site": "string",
            "team": "string",
            "shift": "string",
            "tier": "int64",
        },
    )
    required_cols = {"agent_id", "name", "site", "team", "shift", "tier", "from_date", "to_date"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in agents.csv: {missing}")
    
    df["from_date"] = pd.to_datetime(df["from_date"], errors="coerce")
    df["to_date"] = pd.to_datetime(df["to_date"], errors="coerce")
    return df


def load_products(filepath: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """Load and validate products.csv."""
    path = Path(filepath) if filepath else resolve_data_file("products.csv")
    if not path.exists():
        raise FileNotFoundError(f"Products file not found at {path}")
    
    df = pd.read_csv(
        path,
        dtype={
            "sku": "string",
            "product_name": "string",
            "family": "string",
            "unit_cost_inr": "int64",
            "retail_price_inr": "int64",
            "warranty_months": "int64",
        },
    )
    required_cols = {
        "sku", "product_name", "family", "launch_date",
        "unit_cost_inr", "retail_price_inr", "warranty_months"
    }
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in products.csv: {missing}")
    
    df["launch_date"] = pd.to_datetime(df["launch_date"], errors="coerce")
    return df


def load_tickets(filepath: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """Load and validate tickets.csv, deriving policy fields cleanly."""
    path = Path(filepath) if filepath else resolve_data_file("tickets.csv")
    if not path.exists():
        raise FileNotFoundError(f"Tickets file not found at {path}")
    
    df = pd.read_csv(
        path,
        dtype={
            "ticket_id": "string",
            "status": "string",
            "channel": "string",
            "customer_id": "string",
            "order_id": "string",
            "product_sku": "string",
            "category": "string",
            "priority": "string",
            "assigned_team": "string",
            "agent_id": "string",
            "transfers": "int64",
            "csat_score": "float64",
            "refund_amount_inr": "float64",
            "refund_reason_code": "string",
            "replacement_issued": "string",
            "customer_message": "string",
            "agent_notes": "string",
            "source_system": "string",
        },
    )
    
    required_cols = {
        "ticket_id", "created_at", "first_response_at", "resolved_at", "status",
        "channel", "customer_id", "order_id", "product_sku", "category",
        "priority", "assigned_team", "agent_id", "transfers", "csat_score",
        "refund_amount_inr", "refund_reason_code", "replacement_issued",
        "customer_message", "agent_notes", "source_system"
    }
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in tickets.csv: {missing}")
    
    # 1. Parse raw timestamps (preserving original text columns)
    df["created_dt"] = pd.to_datetime(df["created_at"], errors="coerce")
    df["first_response_dt"] = pd.to_datetime(df["first_response_at"], errors="coerce")
    df["resolved_dt"] = pd.to_datetime(df["resolved_at"], errors="coerce")
    
    # 2. Normalize flags
    df["replacement_issued"] = df["replacement_issued"].str.strip().str.upper()
    df["channel"] = df["channel"].str.strip().str.lower()
    df["status"] = df["status"].str.strip().str.lower()
    
    # 3. Derive resolved_at_reporting (reconcile UTC Freshdesk event log offset)
    # Helpdesk rows: resolved_at_reporting = raw resolved_dt
    # Legacy_fd rows: resolved_at_reporting = raw resolved_dt + 5h 30m
    df["resolved_at_reporting"] = df["resolved_dt"]
    legacy_mask = (df["source_system"] == "legacy_fd") & df["resolved_dt"].notnull()
    df.loc[legacy_mask, "resolved_at_reporting"] = df.loc[legacy_mask, "resolved_dt"] + LEGACY_TIMESTAMP_OFFSET
    df["legacy_timestamp_adjusted"] = legacy_mask
    
    # 4. Handle time calculations
    # Raw handle time (strictly for diagnostics)
    df["raw_handle_time_hours"] = (
        (df["resolved_dt"] - df["first_response_dt"]).dt.total_seconds() / 3600.0
    )
    
    # Policy handle time: first_response_at -> resolved_at_reporting
    # Populated ONLY for attendance tickets (resolved or closed) where both timestamps exist
    is_attendance = df["status"].isin(ATTENDANCE_STATUSES)
    valid_time_mask = is_attendance & df["first_response_dt"].notnull() & df["resolved_at_reporting"].notnull()
    
    df["handle_time_hours"] = np.nan
    df.loc[valid_time_mask, "handle_time_hours"] = (
        (df.loc[valid_time_mask, "resolved_at_reporting"] - df.loc[valid_time_mask, "first_response_dt"])
        .dt.total_seconds() / 3600.0
    )
    
    # 5. SLA Metrics: created_at -> first_response_at
    df["first_response_minutes"] = np.nan
    has_resp_mask = df["created_dt"].notnull() & df["first_response_dt"].notnull()
    df.loc[has_resp_mask, "first_response_minutes"] = (
        (df.loc[has_resp_mask, "first_response_dt"] - df.loc[has_resp_mask, "created_dt"])
        .dt.total_seconds() / 60.0
    )
    
    df["missing_first_response"] = df["first_response_dt"].isnull()
    df["sla_target_minutes"] = df["channel"].map(SLA_TARGET_MINUTES)
    
    # SLA Breach: only evaluated when first response exists; missing is tracked separately
    df["sla_breach"] = False
    valid_sla_mask = df["first_response_minutes"].notnull() & df["sla_target_minutes"].notnull()
    df.loc[valid_sla_mask, "sla_breach"] = (
        df.loc[valid_sla_mask, "first_response_minutes"] > df.loc[valid_sla_mask, "sla_target_minutes"]
    )
    
    # 6. Integrity check: Verify no legacy tickets have negative handle time after adjustment
    remaining_neg_legacy = df[legacy_mask & (df["handle_time_hours"] < 0)]
    if len(remaining_neg_legacy) > 0:
        raise ValueError(
            f"Data integrity error: {len(remaining_neg_legacy)} legacy tickets still have "
            f"negative handle time after +05:30 adjustment."
        )
        
    return df


def load_all_datasets() -> Dict[str, pd.DataFrame]:
    """Load all 5 datasets and return in a dictionary."""
    return {
        "customers": load_customers(),
        "orders": load_orders(),
        "agents": load_agents(),
        "products": load_products(),
        "tickets": load_tickets(),
    }
