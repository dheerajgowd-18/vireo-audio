"""Configuration, business constants, and dynamic file discovery for Vireo Audio."""

import os
import glob
from pathlib import Path
from datetime import timedelta

# Project Root Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# File Discovery Patterns (supports direct names and UUID-prefixed names)
def resolve_data_file(filename_pattern: str, base_dir: Path = BASE_DIR) -> Path:
    """Find a data file by exact name or glob pattern (e.g. *tickets.csv)."""
    # Check exact match first
    exact_path = base_dir / filename_pattern
    if exact_path.exists():
        return exact_path
    
    # Check glob pattern
    glob_pattern = str(base_dir / f"*{filename_pattern}")
    matches = glob.glob(glob_pattern)
    if matches:
        # Sort to ensure deterministic selection if multiple
        matches.sort()
        return Path(matches[0])
    
    raise FileNotFoundError(f"Could not locate data file matching pattern '{filename_pattern}' in {base_dir}")

# Policy Constants: SLAs (minutes)
SLA_TARGET_MINUTES = {
    "chat": 15,
    "voice": 120,    # 2 hours
    "social": 240,   # 4 hours
    "email": 480     # 8 hours
}

# Policy Constants: Costs (INR)
SLA_BREACH_CREDIT_INR = 350
TRANSFER_COST_INR = 305
REPLACEMENT_LOGISTICS_INR = 340
AGENT_HOURLY_COST_INR = 165
GOODWILL_CAP_INR = 500

# Channel Contact Costs (INR)
CONTACT_COSTS_INR = {
    "chat": 210,
    "email": 260,
    "voice": 520,
    "social": 240
}
BLENDED_CONTACT_COST_INR = 290

# Legacy Reconstructed Timestamp Offset (Freshdesk UTC to IST)
LEGACY_TIMESTAMP_OFFSET = timedelta(hours=5, minutes=30)

# Valid Categories & Statuses defined in Policy
VALID_STATUSES = {"resolved", "closed", "open", "pending"}
ATTENDANCE_STATUSES = {"resolved", "closed"}

VALID_REFUND_REASONS = {
    "GW-OTHER", "DOA-REPL", "LOST-TRANSIT", "DUP-PAYMENT",
    "CANCEL", "PRICE-ADJ", "RETURN-QC-OK", "WTY-BUYBACK"
}

# Hardware Triage Frontline Rota Agents identified in audit ("Kavya's four")
HARDWARE_TRIAGE_AGENTS = {"A3004", "A3005", "A3006", "A3007"}
