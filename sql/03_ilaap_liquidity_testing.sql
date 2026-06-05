/*
Project: Regulatory Risk Audit Analytics
Module: ILAAP - Liquidity Risk Testing

Audit Objective:
Assess whether liquidity risk data supports effective monitoring of liquidity gaps,
funding concentration and liquidity buffer adequacy.

Important:
This script does not replicate a full ILAAP model.
It performs Internal Audit reasonableness and control testing over simulated liquidity data.
*/

-- ============================================================
-- TEST 1: Liquidity gaps by maturity bucket
-- Audit question:
-- Are there maturity buckets where expected outflows exceed inflows?
-- ============================================================

SELECT
    maturity_bucket,
    SUM(inflow_amount) AS total_inflows,
    SUM(outflow_amount) AS total_outflows,
    SUM(inflow_amount) - SUM(outflow_amount) AS liquidity_gap
FROM liquidity_cashflows
GROUP BY maturity_bucket
HAVING SUM(inflow_amount) - SUM(outflow_amount) < 0
ORDER BY maturity_bucket;

-- ============================================================
-- TEST 2: Liquidity gap concentration by currency
-- Audit question:
-- Are liquidity gaps concentrated in specific currencies?
-- ============================================================

SELECT
    currency,
    SUM(inflow_amount) AS total_inflows,
    SUM(outflow_amount) AS total_outflows,
    SUM(inflow_amount) - SUM(outflow_amount) AS net_liquidity_position
FROM liquidity_cashflows
GROUP BY currency
HAVING SUM(inflow_amount) - SUM(outflow_amount) < 0
ORDER BY net_liquidity_position ASC;

-- ============================================================
-- TEST 3: Funding concentration by counterparty
-- Audit question:
-- Is the bank excessively dependent on a small number of funding providers?
-- ============================================================

SELECT
    counterparty,
    SUM(funding_amount) AS total_funding,
    SUM(funding_amount) / (
        SELECT SUM(funding_amount) FROM funding_sources
    ) AS funding_concentration_ratio
FROM funding_sources
GROUP BY counterparty
HAVING funding_concentration_ratio > 0.10
ORDER BY funding_concentration_ratio DESC;

-- ============================================================
-- TEST 4: Short-term funding concentration
-- Audit question:
-- Is funding concentrated in short-term maturities?
-- ============================================================

SELECT
    funding_type,
    COUNT(*) AS number_of_positions,
    SUM(funding_amount) AS total_funding,
    AVG(DATEDIFF(maturity_date, CURRENT_DATE)) AS average_days_to_maturity
FROM funding_sources
WHERE maturity_date <= DATE_ADD(CURRENT_DATE, INTERVAL 90 DAY)
GROUP BY funding_type
ORDER BY total_funding DESC;

-- ============================================================
-- TEST 5: Eligible liquidity buffer after haircut
-- Audit question:
-- What is the available liquidity buffer after applying haircuts?
-- ============================================================

SELECT
    asset_type,
    COUNT(*) AS number_of_assets,
    SUM(market_value) AS total_market_value,
    SUM(market_value * (1 - haircut)) AS post_haircut_value
FROM liquidity_buffer
WHERE eligible_flag = 'YES'
GROUP BY asset_type
ORDER BY post_haircut_value DESC;

-- ============================================================
-- TEST 6: Non-eligible assets included in liquidity buffer
-- Audit question:
-- Are non-eligible assets incorrectly included in the liquidity buffer?
-- ============================================================

SELECT
    asset_id,
    asset_type,
    market_value,
    haircut,
    eligible_flag
FROM liquidity_buffer
WHERE eligible_flag = 'NO'
ORDER BY market_value DESC;

-- ============================================================
-- TEST 7: Liquidity buffer coverage of net outflows
-- Audit question:
-- Does the liquidity buffer cover stressed net outflows?
-- Simplified test:
-- Post-haircut eligible liquidity buffer vs total net outflows.
-- ============================================================

SELECT
    lb.total_liquidity_buffer,
    cf.total_net_outflows,
    lb.total_liquidity_buffer / NULLIF(cf.total_net_outflows, 0) AS liquidity_coverage_ratio
FROM
    (
        SELECT
            SUM(market_value * (1 - haircut)) AS total_liquidity_buffer
        FROM liquidity_buffer
        WHERE eligible_flag = 'YES'
    ) lb
CROSS JOIN
    (
        SELECT
            SUM(outflow_amount - inflow_amount) AS total_net_outflows
        FROM liquidity_cashflows
        WHERE outflow_amount > inflow_amount
    ) cf;
