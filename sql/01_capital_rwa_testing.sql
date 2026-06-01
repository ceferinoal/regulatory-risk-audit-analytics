/*
Project: Regulatory Risk Audit Analytics
Module: CRR / CRD / Basel III - Capital & RWA Testing

Audit Objective:
Assess whether regulatory exposure data is complete, reasonably classified
and traceable for capital and RWA reporting purposes.

Important:
This script does not replicate a full regulatory reporting engine.
It performs Internal Audit reasonableness tests over simulated banking data.
*/

-- ============================================================
-- TEST 1: Exposures without regulatory exposure class
-- Audit question:
-- Are all credit exposures assigned to a regulatory exposure class?
-- ============================================================

SELECT
    exposure_id,
    customer_id,
    exposure_amount,
    exposure_class,
    risk_weight,
    reporting_date
FROM exposures
WHERE exposure_class IS NULL
   OR exposure_class = '';

-- ============================================================
-- TEST 2: Exposures without risk weight
-- Audit question:
-- Are all exposures assigned a valid risk weight?
-- ============================================================

SELECT
    exposure_id,
    customer_id,
    exposure_amount,
    exposure_class,
    risk_weight,
    reporting_date
FROM exposures
WHERE risk_weight IS NULL;

-- ============================================================
-- TEST 3: Independent RWA reasonableness recalculation
-- Audit question:
-- Does reported RWA reasonably match recalculated RWA?
-- Simplified formula:
-- Recalculated RWA = Exposure Amount x Risk Weight
-- ============================================================

SELECT
    e.exposure_id,
    e.customer_id,
    e.exposure_amount,
    e.exposure_class,
    e.risk_weight,
    r.reported_rwa,
    e.exposure_amount * e.risk_weight AS recalculated_rwa,
    r.reported_rwa - (e.exposure_amount * e.risk_weight) AS rwa_difference
FROM exposures e
JOIN rwa_calculations r
    ON e.exposure_id = r.exposure_id
WHERE ABS(r.reported_rwa - (e.exposure_amount * e.risk_weight)) > 1000
ORDER BY ABS(r.reported_rwa - (e.exposure_amount * e.risk_weight)) DESC;

-- ============================================================
-- TEST 4: RWA exceptions by exposure class
-- Audit question:
-- Are RWA differences concentrated in specific exposure classes?
-- ============================================================

SELECT
    e.exposure_class,
    COUNT(*) AS exception_count,
    SUM(ABS(r.reported_rwa - (e.exposure_amount * e.risk_weight))) AS total_rwa_difference
FROM exposures e
JOIN rwa_calculations r
    ON e.exposure_id = r.exposure_id
WHERE ABS(r.reported_rwa - (e.exposure_amount * e.risk_weight)) > 1000
GROUP BY e.exposure_class
ORDER BY total_rwa_difference DESC;
