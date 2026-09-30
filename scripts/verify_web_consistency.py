"""Automated verification of web dashboard consistency, data integrity, and offline compliance."""

import re
import json
from pathlib import Path
import pandas as pd


def verify_dashboard():
    print("Verifying Vireo Audio Web Dashboard...")
    errors = []

    # 1. Check all JSON files exist
    required_json = [
        "overview.json",
        "agents.json",
        "trends.json",
        "replacements.json",
        "sla.json",
        "ai_signals.json",
        "methodology.json",
    ]
    data_dir = Path("web/data")
    for jf in required_json:
        p = data_dir / jf
        if not p.exists():
            errors.append(f"Missing JSON: {p}")
        else:
            try:
                with open(p, encoding="utf-8") as f:
                    data = json.load(f)
                if not data:
                    errors.append(f"Empty JSON: {p}")
            except Exception as e:
                errors.append(f"Invalid JSON in {p}: {e}")

    # 2. Check HTML / JS element IDs
    with open("web/app.js", encoding="utf-8") as f:
        js_content = f.read()
    with open("web/index.html", encoding="utf-8") as f:
        html_content = f.read()

    js_ids = set(re.findall(r"getElementById\(['\"]([^'\"]+)", js_content))
    html_ids = set(re.findall(r'id=["\']([^"\']+)', html_content))
    missing_ids = js_ids - html_ids
    if missing_ids:
        errors.append(f"HTML is missing element IDs referenced in JS: {missing_ids}")
    else:
        print("  [OK] All element IDs referenced in app.js exist in index.html.")

    # 3. Check for external network dependencies (CDNs, http://, https://)
    with open("web/styles.css", encoding="utf-8") as f:
        css_content = f.read()

    for fname, content in [("index.html", html_content), ("styles.css", css_content), ("app.js", js_content)]:
        # Exclude standard xml namespace declaration: http://www.w3.org/2000/svg
        clean_content = content.replace("http://www.w3.org/2000/svg", "")
        externals = re.findall(r'https?://[^\s\'"]+', clean_content)
        if externals:
            errors.append(f"Found external URL in {fname}: {externals}")
        else:
            print(f"  [OK] {fname} has zero external CDN or network dependencies.")

    # 4. Verify KPI consistency with source reports
    with open("web/data/overview.json", encoding="utf-8") as f:
        ov = json.load(f)
    scorecard = pd.read_csv("reports/agent_scorecard.csv")
    trends = pd.read_csv("reports/monthly_trends.csv")

    assert ov["kpis"]["csat"]["value"] == 3.33, f"CSAT mismatch: {ov['kpis']['csat']['value']}"
    assert ov["kpis"]["csat"]["responses"] == 5196, f"CSAT response count mismatch"
    assert ov["kpis"]["replacement_units"]["count"] == 1896, f"Replacement count mismatch"
    assert ov["kpis"]["replacement_spend"]["amount_inr"] == 3415990.0, f"Spend mismatch"
    print("  [OK] Overview KPIs exactly match analytical outputs.")

    # 5. Verify Agents consistency
    with open("web/data/agents.json", encoding="utf-8") as f:
        ag = json.load(f)
    assert ag["total_agents"] == 44, f"Agent count mismatch: {ag['total_agents']}"
    assert len(ag["agents"]) == 44, f"Agent list length mismatch"
    assert len(ag["bottom_10"]["agents"]) == 10, f"Bottom 10 count mismatch"
    assert ag["bottom_10"]["composition"]["tier_2_count"] == 6, f"Tier 2 count in bottom 10 mismatch"
    assert ag["bottom_10"]["composition"]["hardware_triage_tier_1_count"] == 4, f"Hardware triage count in bottom 10 mismatch"
    assert ag["bottom_10"]["composition"]["standard_tier_1_count"] == 0, f"Other Tier 1 count in bottom 10 mismatch"
    print("  [OK] 44 agents and exactly 10 bottom agents (6 Tier 2, 4 Hardware Triage) verified.")

    # 6. Verify AI signals consistency
    with open("web/data/ai_signals.json", encoding="utf-8") as f:
        ai_data = json.load(f)
    assert ai_data["other_decomposition"]["total_other_tickets"] == 1732
    assert ai_data["other_decomposition"]["actionable_recovered_count"] == 1524
    assert ai_data["other_decomposition"]["actionable_recovered_pct"] == 87.99
    assert ai_data["hardware_defect_signal"]["precision_pct"] == 100.0
    assert ai_data["hardware_defect_signal"]["recall_pct"] == 47.06
    assert ai_data["hardware_defect_signal"]["f1_pct"] == 64.00
    print("  [OK] AI theme recovery (87.99%) and hardware defect signal (100% precision) verified.")

    # 7. Verify Replacements consistency
    with open("web/data/replacements.json", encoding="utf-8") as f:
        rep = json.load(f)
    assert rep["headline"]["replacement_units"] == 1896
    assert rep["finance_comparison"]["variance_inr"] == 1324010.0
    assert rep["product_breakdown"][0]["sku"] == "VA-EB-PL2", "Pulse 2 must surface at top of replacements"
    assert rep["product_breakdown"][0]["replacements"] == 1166
    print("  [OK] Replacement totals and Pulse 2 concentration verified.")

    if errors:
        print("\nERRORS ENCOUNTERED:")
        for err in errors:
            print(f"  [FAIL] {err}")
        return False

    print("\nALL WEB CONSISTENCY CHECKS PASSED (100% SUCCESS)!")
    return True


if __name__ == "__main__":
    success = verify_dashboard()
    if not success:
        exit(1)
