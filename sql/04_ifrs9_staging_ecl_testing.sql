/*
Project: Regulatory Risk Audit Analytics
Module: IFRS 9 - Staging & Expected Credit Loss Testing

Audit Objective:
Assess whether IFRS 9 staging and expected credit loss data are complete,
reasonable and consistent with basic credit deterioration indicators.

Important:
This script does not replicate a full IFRS 9 impairment model.
It performs Internal Audit reasonableness and control testing over simulated credit risk data.
*/

-- ============================================================
-- TEST 1: Loans with 30+ days past due still classified as Stage 1
-- Audit question:
-- Are loans with significant increase in credit risk still classified as Stage 1?
-- ============================================================

SELECT
    loan_id,
    customer_id,
    outstanding_balance,
    days_past_due,
    stage,
    origination_pd,
    current_pd,
    reported_ecl
FROM ifrs9_loans
WHERE days_past_due >= 30
  AND stage = 'STAGE_1'
ORDER BY days_past_due DESC;

-- ============================================================
-- TEST 2: Loans with 90+ days past due not classified as Stage 3
-- Audit question:
-- Are default indicators properly reflected in IFRS 9 staging?
-- ============================================================

SELECT
    loan_id,
    customer_id,
    outstanding_balance,
    days_past_due,
    stage,
    reported_ecl
FROM ifrs9_loans
WHERE days_past_due >= 90
  AND stage <> 'STAGE_3'
ORDER BY days_past_due DESC;

-- ============================================================
-- TEST 3: Significant PD increase but loan remains in Stage 1
-- Audit question:
-- Are significant increases in credit risk reflected in staging?
-- Simplified rule:
-- Current PD greater than twice origination PD.
-- ============================================================

SELECT
    loan_id,
    customer_id,
    outstanding_balance,
    stage,
    origination_pd,
    current_pd,
    current_pd / NULLIF(origination_pd, 0) AS pd_increase_ratio,
    reported_ecl
FROM ifrs9_loans
WHERE current_pd > (origination_pd * 2)
  AND stage = 'STAGE_1'
ORDER BY pd_increase_ratio DESC;

-- ============================================================
-- TEST 4: Missing PD, LGD or EAD inputs
-- Audit question:
-- Are all required ECL input parameters available?
-- ============================================================

SELECT
    loan_id,
    customer_id,
    outstanding_balance,
    stage,
    pd,
    lgd,
    ead,
    reported_ecl
FROM ifrs9_loans
WHERE pd IS NULL
   OR lgd IS NULL
   OR ead IS NULL;

-- ============================================================
-- TEST 5: Simplified ECL reasonableness recalculation
-- Audit question:
-- Does reported ECL reasonably match simplified recalculated ECL?
-- Simplified formula:
-- ECL = PD x LGD x EAD
-- ============================================================

SELECT
    loan_id,
    customer_id,
    outstanding_balance,
    stage,
    pd,
    lgd,
    ead,
    reported_ecl,
    pd * lgd * ead AS recalculated_ecl,
    reported_ecl - (pd * lgd * ead) AS ecl_difference
FROM ifrs9_loans
WHERE ABS(reported_ecl - (pd * lgd * ead)) > 100
ORDER BY ABS(reported_ecl - (pd * lgd * ead)) DESC;

-- ============================================================
-- TEST 6: ECL coverage ratio by stage
-- Audit question:
-- Is ECL coverage consistent across IFRS 9 stages?
-- ============================================================

SELECT
    stage,
    COUNT(*) AS number_of_loans,
    SUM(outstanding_balance) AS total_exposure,
    SUM(reported_ecl) AS total_reported_ecl,
    SUM(reported_ecl) / NULLIF(SUM(outstanding_balance), 0) AS ecl_coverage_ratio
FROM ifrs9_loans
GROUP BY stage
ORDER BY stage;

-- ============================================================
-- TEST 7: Stage distribution by exposure
-- Audit question:
-- Is credit exposure concentrated in deteriorated stages?
-- ============================================================

SELECT
    stage,
    COUNT(*) AS number_of_loans,
    SUM(outstanding_balance) AS total_outstanding_balance,
    AVG(days_past_due) AS average_days_past_due,
    AVG(current_pd) AS average_current_pd
FROM ifrs9_loans
GROUP BY stage
ORDER BY total_outstanding_balance DESC;
