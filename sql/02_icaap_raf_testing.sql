/*
Project: Regulatory Risk Audit Analytics
Module: ICAAP & Risk Appetite Framework Testing

Audit Objective:
Assess whether material risks are properly identified, owned, reviewed,
capitalised and monitored against the Risk Appetite Framework.

Important:
This script does not replicate a full ICAAP model.
It performs Internal Audit reasonableness and control testing over simulated risk governance data.
*/

-- ============================================================
-- TEST 1: Material risks without assigned internal capital
-- Audit question:
-- Are all material risks assessed and capitalised under ICAAP?
-- ============================================================

SELECT
    risk_id,
    risk_type,
    materiality,
    risk_owner,
    capital_required,
    methodology,
    last_review_date
FROM risk_inventory
WHERE materiality = 'MATERIAL'
  AND (capital_required IS NULL OR capital_required = 0);

-- ============================================================
-- TEST 2: Material risks without assigned risk owner
-- Audit question:
-- Does each material risk have clear ownership?
-- ============================================================

SELECT
    risk_id,
    risk_type,
    materiality,
    risk_owner,
    capital_required,
    methodology,
    last_review_date
FROM risk_inventory
WHERE materiality = 'MATERIAL'
  AND (risk_owner IS NULL OR risk_owner = '');

-- ============================================================
-- TEST 3: Material risks not reviewed in the last 12 months
-- Audit question:
-- Are material risks reviewed periodically?
-- ============================================================

SELECT
    risk_id,
    risk_type,
    materiality,
    risk_owner,
    capital_required,
    methodology,
    last_review_date,
    DATEDIFF(CURRENT_DATE, last_review_date) AS days_since_review
FROM risk_inventory
WHERE materiality = 'MATERIAL'
  AND last_review_date < DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
ORDER BY days_since_review DESC;

-- ============================================================
-- TEST 4: Risk Appetite Framework breaches
-- Audit question:
-- Are risk appetite limits being breached?
-- ============================================================

SELECT
    risk_type,
    metric_name,
    limit_value,
    current_value,
    current_value - limit_value AS excess_amount,
    breach_status,
    reporting_date
FROM risk_appetite_limits
WHERE current_value > limit_value
ORDER BY excess_amount DESC;

-- ============================================================
-- TEST 5: RAF breaches not escalated
-- Audit question:
-- Are risk appetite breaches escalated according to governance procedures?
-- ============================================================

SELECT
    risk_type,
    metric_name,
    limit_value,
    current_value,
    current_value - limit_value AS excess_amount,
    breach_status,
    escalated_to_committee,
    reporting_date
FROM risk_appetite_limits
WHERE current_value > limit_value
  AND (escalated_to_committee IS NULL OR escalated_to_committee = 'NO')
ORDER BY excess_amount DESC;

-- ============================================================
-- TEST 6: ICAAP capital concentration by risk type
-- Audit question:
-- Which risk types consume the highest amount of internal capital?
-- ============================================================

SELECT
    risk_type,
    COUNT(*) AS number_of_risks,
    SUM(capital_required) AS total_internal_capital,
    AVG(capital_required) AS average_capital_required
FROM risk_inventory
WHERE materiality = 'MATERIAL'
GROUP BY risk_type
ORDER BY total_internal_capital DESC;
