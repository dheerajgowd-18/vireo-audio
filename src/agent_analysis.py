"""Agent scorecard and defensible peer-group benchmarking analysis."""

from typing import Dict, Any, List
import pandas as pd
import numpy as np

from .config import HARDWARE_TRIAGE_AGENTS


def build_agent_scorecard(
    tickets: pd.DataFrame, agents: pd.DataFrame
) -> pd.DataFrame:
    """Build agent scorecard strictly joining on agent_id and establishing peer benchmarks.
    
    Rule: Never join on agent name; preserve distinct entries for duplicate display names.
    Rule: Exclude blank CSAT from averages.
    Rule: Keep Tier 2 distinct from Tier 1.
    """
    # 1. Aggregate ticket performance metrics by agent_id
    agent_metrics = (
        tickets.groupby("agent_id")
        .agg(
            tickets=("ticket_id", "count"),
            csat_n=("csat_score", lambda s: s.notnull().sum()),
            mean_csat=("csat_score", "mean"),
            median_csat=("csat_score", "median"),
            handle_time_tickets=("handle_time_hours", lambda s: s.notnull().sum()),
            mean_handle_hours=("handle_time_hours", "mean"),
            median_handle_hours=("handle_time_hours", "median"),
            sla_breaches=("sla_breach", "sum"),
            transfer_count=("transfers", "sum"),
            replacement_count=("replacement_issued", lambda s: (s == "Y").sum()),
        )
        .reset_index()
    )
    
    agent_metrics["csat_response_rate"] = (
        agent_metrics["csat_n"] / agent_metrics["tickets"]
    )
    agent_metrics["sla_breach_rate"] = (
        agent_metrics["sla_breaches"] / agent_metrics["tickets"]
    )
    
    # 2. Join strictly on agent_id
    scorecard = agents.merge(agent_metrics, on="agent_id", how="left")
    
    # Fill defaults if an agent resolved zero tickets (none in this dataset, but robust)
    scorecard["tickets"] = scorecard["tickets"].fillna(0).astype(int)
    scorecard["csat_n"] = scorecard["csat_n"].fillna(0).astype(int)
    scorecard["sla_breaches"] = scorecard["sla_breaches"].fillna(0).astype(int)
    scorecard["transfer_count"] = scorecard["transfer_count"].fillna(0).astype(int)
    scorecard["replacement_count"] = scorecard["replacement_count"].fillna(0).astype(int)
    
    # 3. Establish benchmark groups (Tier + Team operational stratification)
    scorecard["benchmark_group"] = scorecard.apply(
        lambda r: f"Tier {r['tier']} - {r['team']}", axis=1
    )
    
    # 4. Tag the hardware triage rota subset identified in email-thread and audit
    scorecard["is_hardware_triage_rota"] = scorecard["agent_id"].isin(HARDWARE_TRIAGE_AGENTS)
    
    # 5. Provide intra-group CSAT rank (1 = lowest CSAT within the same benchmark group)
    scorecard["intra_group_csat_rank_asc"] = (
        scorecard.groupby("benchmark_group")["mean_csat"]
        .rank(ascending=True, method="min")
    )
    
    # Top CSAT rank (1 = highest CSAT within benchmark group)
    scorecard["intra_group_csat_rank_desc"] = (
        scorecard.groupby("benchmark_group")["mean_csat"]
        .rank(ascending=False, method="min")
    )
    
    # Order columns cleanly
    ordered_cols = [
        "agent_id",
        "name",
        "tier",
        "team",
        "site",
        "shift",
        "benchmark_group",
        "is_hardware_triage_rota",
        "tickets",
        "csat_n",
        "csat_response_rate",
        "mean_csat",
        "median_csat",
        "mean_handle_hours",
        "median_handle_hours",
        "sla_breaches",
        "sla_breach_rate",
        "transfer_count",
        "replacement_count",
        "intra_group_csat_rank_asc",
        "intra_group_csat_rank_desc",
    ]
    return scorecard[ordered_cols]


def summarize_by_tier_and_team(scorecard: pd.DataFrame) -> pd.DataFrame:
    """Produce benchmark summary table by Tier and Team."""
    summary = (
        scorecard.groupby(["tier", "team"])
        .agg(
            agent_count=("agent_id", "count"),
            total_tickets=("tickets", "sum"),
            avg_tickets_per_agent=("tickets", "mean"),
            mean_csat=("mean_csat", "mean"),
            avg_handle_hours=("mean_handle_hours", "mean"),
            median_handle_hours=("median_handle_hours", "mean"),
            total_sla_breaches=("sla_breaches", "sum"),
            total_replacements=("replacement_count", "sum"),
        )
        .reset_index()
    )
    return summary
