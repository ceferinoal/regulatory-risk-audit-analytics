"""
Project: Regulatory Risk Audit Analytics
Script: Synthetic Regulatory Data Generator

Objective:
Generate synthetic banking datasets to simulate Internal Audit testing over:
- Capital & RWA
- ICAAP & RAF
- ILAAP
- IFRS 9

Important:
The data is fully synthetic and does not represent any real bank, client or transaction.
"""

import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# ============================================================
# Configuration
# ============================================================

np.random.seed(42)
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

today = datetime.today().date()


# ============================================================
# 1. CAPITAL & RWA DATA
# ============================================================

def generate_capital_rwa_data(n_exposures=1000):
    exposure_classes = [
        "Retail",
        "Corporate",
        "Institutions",
        "Sovereigns",
        "Secured by mortgages",
        "Defaulted exposures"
    ]

    risk_weight_map = {
        "Retail": 0.75,
        "Corporate": 1.00,
        "Institutions": 0.50,
        "Sovereigns": 0.00,
        "Secured by mortgages": 0.35,
        "Defaulted exposures": 1.50
    }

    exposures = []

    for i in range(1, n_exposures + 1):
        exposure_id = f"EXP_{i:05d}"
        customer_id = f"CUST_{random.randint(1, 300):04d}"
        exposure_amount = round(np.random.uniform(10_000, 2_000_000), 2)

        exposure_class = random.choice(exposure_classes)
        risk_weight = risk_weight_map[exposure_class]

        # Introduce intentional data quality exceptions
        if random.random() < 0.03:
            exposure_class = None

        if random.random() < 0.03:
            risk_weight = None

        exposures.append([
            exposure_id,
            customer_id,
            exposure_amount,
            exposure_class,
            risk_weight,
            today
        ])

    exposures_df = pd.DataFrame(exposures, columns=[
        "exposure_id",
        "customer_id",
        "exposure_amount",
        "exposure_class",
        "risk_weight",
        "reporting_date"
    ])

    rwa_records = []

    for _, row in exposures_df.iterrows():
        if pd.isna(row["risk_weight"]):
            reported_rwa = np.nan
        else:
            expected_rwa = row["exposure_amount"] * row["risk_weight"]

            # Introduce calculation differences in some cases
            if random.random() < 0.08:
                reported_rwa = expected_rwa + random.choice([-5000, -2500, 2500, 5000, 10000])
            else:
                reported_rwa = expected_rwa

        rwa_records.append([
            row["exposure_id"],
            round(reported_rwa, 2) if not pd.isna(reported_rwa) else np.nan,
            today
        ])

    rwa_df = pd.DataFrame(rwa_records, columns=[
        "exposure_id",
        "reported_rwa",
        "calculation_date"
    ])

    capital_position_df = pd.DataFrame({
        "reporting_date": [today],
        "cet1_capital": [12_000_000],
        "tier1_capital": [13_500_000],
        "total_capital": [15_000_000],
        "total_rwa": [rwa_df["reported_rwa"].sum(skipna=True)]
    })

    exposures_df.to_csv(os.path.join(DATA_DIR, "exposures.csv"), index=False)
    rwa_df.to_csv(os.path.join(DATA_DIR, "rwa_calculations.csv"), index=False)
    capital_position_df.to_csv(os.path.join(DATA_DIR, "capital_position.csv"), index=False)


# ============================================================
# 2. ICAAP & RAF DATA
# ============================================================

def generate_icaap_raf_data():
    risk_types = [
        "Credit Risk",
        "Market Risk",
        "Operational Risk",
        "Liquidity Risk",
        "IRRBB",
        "Model Risk",
        "Concentration Risk"
    ]

    methodologies = [
        "Economic capital model",
        "Stress scenario",
        "Standardised approach",
        "Expert judgement",
        "Historical loss analysis"
    ]

    risk_records = []

    for i in range(1, 61):
        risk_id = f"RISK_{i:03d}"
        risk_type = random.choice(risk_types)
        materiality = np.random.choice(["MATERIAL", "NON_MATERIAL"], p=[0.70, 0.30])
        risk_owner = f"Owner_{random.randint(1, 15)}"
        capital_required = round(np.random.uniform(100_000, 2_500_000), 2)
        methodology = random.choice(methodologies)
        last_review_date = today - timedelta(days=random.randint(30, 900))

        # Intentional ICAAP governance exceptions
        if materiality == "MATERIAL" and random.random() < 0.10:
            capital_required = 0

        if materiality == "MATERIAL" and random.random() < 0.08:
            risk_owner = None

        risk_records.append([
            risk_id,
            risk_type,
            materiality,
            risk_owner,
            capital_required,
            methodology,
            last_review_date
        ])

    risk_inventory_df = pd.DataFrame(risk_records, columns=[
        "risk_id",
        "risk_type",
        "materiality",
        "risk_owner",
        "capital_required",
        "methodology",
        "last_review_date"
    ])

    raf_records = []

    for risk_type in risk_types:
        for metric_id in range(1, 4):
            metric_name = f"{risk_type} Metric {metric_id}"
            limit_value = round(np.random.uniform(50, 100), 2)

            # Some values breach limits
            if random.random() < 0.30:
                current_value = limit_value + round(np.random.uniform(1, 30), 2)
                breach_status = "BREACH"
                escalated_to_committee = np.random.choice(["YES", "NO"], p=[0.65, 0.35])
            else:
                current_value = limit_value - round(np.random.uniform(1, 30), 2)
                breach_status = "OK"
                escalated_to_committee = "NO"

            raf_records.append([
                risk_type,
                metric_name,
                limit_value,
                current_value,
                breach_status,
                escalated_to_committee,
                today
            ])

    raf_df = pd.DataFrame(raf_records, columns=[
        "risk_type",
        "metric_name",
        "limit_value",
        "current_value",
        "breach_status",
        "escalated_to_committee",
        "reporting_date"
    ])

    risk_inventory_df.to_csv(os.path.join(DATA_DIR, "risk_inventory.csv"), index=False)
    raf_df.to_csv(os.path.join(DATA_DIR, "risk_appetite_limits.csv"), index=False)


# ============================================================
# 3. ILAAP DATA
# ============================================================

def generate_ilaap_data():
    maturity_buckets = [
        "Overnight",
        "2-7 days",
        "8-30 days",
        "1-3 months",
        "3-6 months",
        "6-12 months",
        "> 1 year"
    ]

    currencies = ["EUR", "USD", "GBP"]

    cashflow_records = []

    for bucket in maturity_buckets:
        for currency in currencies:
            inflow_amount = round(np.random.uniform(500_000, 5_000_000), 2)
            outflow_amount = round(np.random.uniform(500_000, 6_500_000), 2)

            cashflow_records.append([
                f"CF_{len(cashflow_records) + 1:04d}",
                bucket,
                inflow_amount,
                outflow_amount,
                currency,
                today
            ])

    liquidity_cashflows_df = pd.DataFrame(cashflow_records, columns=[
        "cashflow_id",
        "maturity_bucket",
        "inflow_amount",
        "outflow_amount",
        "currency",
        "reporting_date"
    ])

    counterparties = [
        "Counterparty A",
        "Counterparty B",
        "Counterparty C",
        "Counterparty D",
        "Counterparty E",
        "Counterparty F"
    ]

    funding_types = [
        "Wholesale funding",
        "Retail deposits",
        "Covered bonds",
        "Interbank funding",
        "Central bank facility"
    ]

    funding_records = []

    for i in range(1, 101):
        source_id = f"FUND_{i:04d}"
        counterparty = random.choice(counterparties)
        funding_amount = round(np.random.uniform(250_000, 8_000_000), 2)
        maturity_date = today + timedelta(days=random.randint(15, 720))
        funding_type = random.choice(funding_types)

        funding_records.append([
            source_id,
            counterparty,
            funding_amount,
            maturity_date,
            funding_type
        ])

    funding_sources_df = pd.DataFrame(funding_records, columns=[
        "source_id",
        "counterparty",
        "funding_amount",
        "maturity_date",
        "funding_type"
    ])

    asset_types = [
        "Cash",
        "Government bonds",
        "Covered bonds",
        "Corporate bonds",
        "Equities"
    ]

    liquidity_buffer_records = []

    for i in range(1, 151):
        asset_id = f"LIQ_{i:04d}"
        asset_type = random.choice(asset_types)
        market_value = round(np.random.uniform(100_000, 5_000_000), 2)

        if asset_type == "Cash":
            haircut = 0.00
            eligible_flag = "YES"
        elif asset_type == "Government bonds":
            haircut = 0.05
            eligible_flag = "YES"
        elif asset_type == "Covered bonds":
            haircut = 0.10
            eligible_flag = "YES"
        elif asset_type == "Corporate bonds":
            haircut = 0.25
            eligible_flag = np.random.choice(["YES", "NO"], p=[0.50, 0.50])
        else:
            haircut = 0.50
            eligible_flag = "NO"

        liquidity_buffer_records.append([
            asset_id,
            asset_type,
            market_value,
            haircut,
            eligible_flag
        ])

    liquidity_buffer_df = pd.DataFrame(liquidity_buffer_records, columns=[
        "asset_id",
        "asset_type",
        "market_value",
        "haircut",
        "eligible_flag"
    ])

    liquidity_cashflows_df.to_csv(os.path.join(DATA_DIR, "liquidity_cashflows.csv"), index=False)
    funding_sources_df.to_csv(os.path.join(DATA_DIR, "funding_sources.csv"), index=False)
    liquidity_buffer_df.to_csv(os.path.join(DATA_DIR, "liquidity_buffer.csv"), index=False)


# ============================================================
# 4. IFRS 9 DATA
# ============================================================

def generate_ifrs9_data(n_loans=800):
    loans = []

    for i in range(1, n_loans + 1):
        loan_id = f"LOAN_{i:05d}"
        customer_id = f"CUST_{random.randint(1, 300):04d}"
        outstanding_balance = round(np.random.uniform(5_000, 1_000_000), 2)

        days_past_due = np.random.choice(
            [0, 10, 20, 30, 45, 60, 90, 120],
            p=[0.45, 0.15, 0.10, 0.08, 0.07, 0.05, 0.05, 0.05]
        )

        origination_pd = round(np.random.uniform(0.005, 0.08), 4)

        if days_past_due >= 90:
            current_pd = round(np.random.uniform(0.20, 0.60), 4)
            stage = "STAGE_3"
        elif days_past_due >= 30:
            current_pd = round(np.random.uniform(0.08, 0.25), 4)
            stage = "STAGE_2"
        else:
            current_pd = round(np.random.uniform(0.005, 0.10), 4)
            stage = "STAGE_1"

        lgd = round(np.random.uniform(0.20, 0.70), 4)
        ead = outstanding_balance
        pd_value = current_pd
        reported_ecl = round(pd_value * lgd * ead, 2)

        # Intentional staging exceptions
        if days_past_due >= 30 and random.random() < 0.12:
            stage = "STAGE_1"

        if days_past_due >= 90 and random.random() < 0.10:
            stage = "STAGE_2"

        # Intentional ECL difference
        if random.random() < 0.08:
            reported_ecl = reported_ecl + random.choice([-1000, -500, 500, 1000, 2500])

        # Intentional missing model input
        if random.random() < 0.03:
            pd_value = np.nan

        if random.random() < 0.03:
            lgd = np.nan

        if random.random() < 0.03:
            ead = np.nan

        loans.append([
            loan_id,
            customer_id,
            outstanding_balance,
            days_past_due,
            stage,
            origination_pd,
            current_pd,
            pd_value,
            lgd,
            ead,
            reported_ecl
        ])

    ifrs9_loans_df = pd.DataFrame(loans, columns=[
        "loan_id",
        "customer_id",
        "outstanding_balance",
        "days_past_due",
        "stage",
        "origination_pd",
        "current_pd",
        "pd",
        "lgd",
        "ead",
        "reported_ecl"
    ])

    ifrs9_loans_df.to_csv(os.path.join(DATA_DIR, "ifrs9_loans.csv"), index=False)


# ============================================================
# Main execution
# ============================================================

if __name__ == "__main__":
    generate_capital_rwa_data()
    generate_icaap_raf_data()
    generate_ilaap_data()
    generate_ifrs9_data()

    print("Synthetic regulatory risk audit datasets generated successfully.")
    print(f"CSV files saved in: {DATA_DIR}")
