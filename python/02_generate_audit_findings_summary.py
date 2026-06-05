"""
Project: Regulatory Risk Audit Analytics
Script: Audit Findings Summary Generator

Objective:
Read synthetic regulatory risk datasets and generate a structured Internal Audit
findings summary across:
- Capital & RWA
- ICAAP & RAF
- ILAAP
- IFRS 9

Important:
This script does not replace professional audit judgement.
It simulates how Python can help Internal Audit consolidate exceptions,
assign risk severity and generate audit-ready evidence.
"""

import os
import pandas as pd


# ============================================================
# Paths
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)


# ============================================================
# Helper functions
# ============================================================

def read_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    return pd.read_csv(path)


def assign_risk_rating(exception_count):
    if exception_count >= 50:
        return "HIGH"
    elif exception_count >= 15:
        return "MEDIUM"
    elif exception_count > 0:
        return "LOW"
    else:
        return "NO EXCEPTIONS"


def add_finding(findings, module, test_name, exception_count, audit_interpretation):
    findings.append({
        "module": module,
        "test_name": test_name,
        "exception_count": int(exception_count),
        "risk_rating": assign_risk_rating(exception_count),
        "audit_interpretation": audit_interpretation
    })


# ============================================================
# Load datasets
# ============================================================

exposures = read_csv("exposures.csv")
rwa = read_csv("rwa_calculations.csv")
risk_inventory = read_csv("risk_inventory.csv")
raf = read_csv("risk_appetite_limits.csv")
liquidity_cashflows = read_csv("liquidity_cashflows.csv")
funding_sources = read_csv("funding_sources.csv")
liquidity_buffer = read_csv("liquidity_buffer.csv")
ifrs9_loans = read_csv("ifrs9_loans.csv")

findings = []


# ============================================================
# 1. Capital & RWA findings
# ============================================================

missing_exposure_class = exposures[
    exposures["exposure_class"].isna() | (exposures["exposure_class"] == "")
]

add_finding(
    findings,
    "Capital & RWA",
    "Exposures without regulatory exposure class",
    len(missing_exposure_class),
    "Missing regulatory exposure classifications may indicate data quality weaknesses affecting RWA calculation and prudential reporting."
)

missing_risk_weight = exposures[
    exposures["risk_weight"].isna()
]

add_finding(
    findings,
    "Capital & RWA",
    "Exposures without risk weight",
    len(missing_risk_weight),
    "Missing risk weights may prevent accurate RWA calculation and weaken regulatory reporting controls."
)

rwa_merged = exposures.merge(rwa, on="exposure_id", how="inner")
rwa_merged["recalculated_rwa"] = rwa_merged["exposure_amount"] * rwa_merged["risk_weight"]
rwa_merged["rwa_difference"] = rwa_merged["reported_rwa"] - rwa_merged["recalculated_rwa"]

rwa_exceptions = rwa_merged[
    rwa_merged["rwa_difference"].abs() > 1000
]

add_finding(
    findings,
    "Capital & RWA",
    "Reported RWA differs from simplified recalculated RWA",
    len(rwa_exceptions),
    "Differences between reported and recalculated RWA may indicate calculation, mapping or reconciliation issues requiring further audit investigation."
)


# ============================================================
# 2. ICAAP & RAF findings
# ============================================================

material_risks_without_capital = risk_inventory[
    (risk_inventory["materiality"] == "MATERIAL") &
    ((risk_inventory["capital_required"].isna()) | (risk_inventory["capital_required"] == 0))
]

add_finding(
    findings,
    "ICAAP & RAF",
    "Material risks without assigned internal capital",
    len(material_risks_without_capital),
    "Material risks without assigned capital may indicate weaknesses in ICAAP completeness, risk quantification or governance."
)

material_risks_without_owner = risk_inventory[
    (risk_inventory["materiality"] == "MATERIAL") &
    ((risk_inventory["risk_owner"].isna()) | (risk_inventory["risk_owner"] == ""))
]

add_finding(
    findings,
    "ICAAP & RAF",
    "Material risks without assigned risk owner",
    len(material_risks_without_owner),
    "Material risks without clear ownership may weaken accountability, monitoring and escalation within the risk governance framework."
)

raf_breaches = raf[
    raf["current_value"] > raf["limit_value"]
]

add_finding(
    findings,
    "ICAAP & RAF",
    "Risk Appetite Framework limit breaches",
    len(raf_breaches),
    "RAF breaches indicate areas where current risk levels exceed approved appetite and require governance attention."
)

raf_breaches_not_escalated = raf[
    (raf["current_value"] > raf["limit_value"]) &
    (raf["escalated_to_committee"] == "NO")
]

add_finding(
    findings,
    "ICAAP & RAF",
    "RAF breaches not escalated to committee",
    len(raf_breaches_not_escalated),
    "Risk appetite breaches without escalation may indicate weaknesses in governance discipline and breach management procedures."
)


# ============================================================
# 3. ILAAP findings
# ============================================================

liquidity_gap_by_bucket = (
    liquidity_cashflows
    .groupby("maturity_bucket", as_index=False)
    .agg(
        total_inflows=("inflow_amount", "sum"),
        total_outflows=("outflow_amount", "sum")
    )
)

liquidity_gap_by_bucket["liquidity_gap"] = (
    liquidity_gap_by_bucket["total_inflows"] -
    liquidity_gap_by_bucket["total_outflows"]
)

negative_liquidity_buckets = liquidity_gap_by_bucket[
    liquidity_gap_by_bucket["liquidity_gap"] < 0
]

add_finding(
    findings,
    "ILAAP",
    "Negative liquidity gaps by maturity bucket",
    len(negative_liquidity_buckets),
    "Negative liquidity gaps in maturity buckets may indicate liquidity mismatch requiring monitoring, escalation or contingency funding actions."
)

funding_total = funding_sources["funding_amount"].sum()

funding_concentration = (
    funding_sources
    .groupby("counterparty", as_index=False)
    .agg(total_funding=("funding_amount", "sum"))
)

funding_concentration["funding_concentration_ratio"] = (
    funding_concentration["total_funding"] / funding_total
)

high_funding_concentration = funding_concentration[
    funding_concentration["funding_concentration_ratio"] > 0.10
]

add_finding(
    findings,
    "ILAAP",
    "Funding concentration above 10% by counterparty",
    len(high_funding_concentration),
    "High funding concentration may increase vulnerability to counterparty withdrawal or market stress."
)

non_eligible_assets = liquidity_buffer[
    liquidity_buffer["eligible_flag"] == "NO"
]

add_finding(
    findings,
    "ILAAP",
    "Non-eligible assets identified in liquidity buffer population",
    len(non_eligible_assets),
    "Non-eligible assets within the liquidity buffer population may indicate classification or data quality issues."
)


# ============================================================
# 4. IFRS 9 findings
# ============================================================

stage1_30dpd = ifrs9_loans[
    (ifrs9_loans["days_past_due"] >= 30) &
    (ifrs9_loans["stage"] == "STAGE_1")
]

add_finding(
    findings,
    "IFRS 9",
    "Loans with 30+ days past due still classified as Stage 1",
    len(stage1_30dpd),
    "Loans with 30+ days past due remaining in Stage 1 may indicate staging inconsistencies or delayed recognition of credit deterioration."
)

not_stage3_90dpd = ifrs9_loans[
    (ifrs9_loans["days_past_due"] >= 90) &
    (ifrs9_loans["stage"] != "STAGE_3")
]

add_finding(
    findings,
    "IFRS 9",
    "Loans with 90+ days past due not classified as Stage 3",
    len(not_stage3_90dpd),
    "Loans with default indicators not classified as Stage 3 may indicate weaknesses in default identification or staging controls."
)

missing_ifrs9_inputs = ifrs9_loans[
    ifrs9_loans["pd"].isna() |
    ifrs9_loans["lgd"].isna() |
    ifrs9_loans["ead"].isna()
]

add_finding(
    findings,
    "IFRS 9",
    "Loans with missing PD, LGD or EAD inputs",
    len(missing_ifrs9_inputs),
    "Missing IFRS 9 model inputs may affect the completeness and reliability of expected credit loss calculations."
)

ifrs9_loans["recalculated_ecl"] = (
    ifrs9_loans["pd"] *
    ifrs9_loans["lgd"] *
    ifrs9_loans["ead"]
)

ifrs9_loans["ecl_difference"] = (
    ifrs9_loans["reported_ecl"] -
    ifrs9_loans["recalculated_ecl"]
)

ecl_exceptions = ifrs9_loans[
    ifrs9_loans["ecl_difference"].abs() > 100
]

add_finding(
    findings,
    "IFRS 9",
    "Reported ECL differs from simplified recalculated ECL",
    len(ecl_exceptions),
    "Differences between reported and recalculated ECL may indicate model input, calculation or reconciliation issues requiring further review."
)


# ============================================================
# Generate findings summary
# ============================================================

findings_df = pd.DataFrame(findings)
findings_df = findings_df.sort_values(
    by=["risk_rating", "exception_count"],
    ascending=[True, False]
)

findings_csv_path = os.path.join(REPORTS_DIR, "findings_summary.csv")
findings_df.to_csv(findings_csv_path, index=False)


# ============================================================
# Generate markdown audit summary
# ============================================================

audit_summary_path = os.path.join(REPORTS_DIR, "audit_summary.md")

with open(audit_summary_path, "w", encoding="utf-8") as report:
    report.write("# Regulatory Risk Audit Analytics — Audit Summary\n\n")

    report.write("## Objective\n\n")
    report.write(
        "This report summarises the results of simulated data-driven Internal Audit tests "
        "over capital and RWA, ICAAP and RAF, ILAAP, and IFRS 9.\n\n"
    )

    report.write("## Important Disclaimer\n\n")
    report.write(
        "The datasets are fully synthetic and the tests are simplified. "
        "The purpose of this project is not to replicate full regulatory, capital, liquidity or IFRS 9 models, "
        "but to demonstrate how Internal Audit can use SQL and Python to identify control exceptions, "
        "data quality issues and reasonableness concerns.\n\n"
    )

    report.write("## Findings Summary\n\n")

    for _, row in findings_df.iterrows():
        report.write(f"### {row['module']} — {row['test_name']}\n\n")
        report.write(f"- Exceptions identified: {row['exception_count']}\n")
        report.write(f"- Risk rating: {row['risk_rating']}\n")
        report.write(f"- Audit interpretation: {row['audit_interpretation']}\n\n")

    report.write("## Audit Interpretation\n\n")
    report.write(
        "The results show how data analytics can support Internal Audit by moving from sample-based review "
        "to population-level exception identification. The findings would require validation with process owners, "
        "assessment of data lineage, review of control design and evaluation of whether issues are isolated or systemic.\n\n"
    )

    report.write("## Recommended Next Steps\n\n")
    report.write("1. Validate exceptions with process owners.\n")
    report.write("2. Confirm data lineage and source system reliability.\n")
    report.write("3. Assess whether exceptions are isolated or systemic.\n")
    report.write("4. Identify root causes and control weaknesses.\n")
    report.write("5. Agree remediation actions, owners and deadlines.\n")
    report.write("6. Perform follow-up testing.\n\n")

    report.write("## Interview Explanation\n\n")
    report.write(
        "I used Python to consolidate exceptions from multiple regulatory risk audit areas, "
        "assign severity levels and generate an audit-style summary. "
        "The purpose was to demonstrate how data analytics can help Internal Audit prioritise findings, "
        "structure evidence and support professional judgement.\n"
    )

print("Audit findings summary generated successfully.")
print(f"CSV report saved in: {findings_csv_path}")
print(f"Markdown report saved in: {audit_summary_path}")