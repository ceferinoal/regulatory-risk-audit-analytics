# ILAAP Liquidity Testing — Audit Explanation

## Audit Objective

The objective of this module is to assess whether liquidity risk data supports effective monitoring of liquidity gaps, funding concentration and liquidity buffer adequacy.

## Regulatory Context

ILAAP is the internal process through which a bank assesses whether it has sufficient liquidity and funding resources to meet its obligations, including under stressed conditions.

From an Internal Audit perspective, the objective is not to replicate the full liquidity risk framework, but to assess whether liquidity risk monitoring is supported by complete, reliable and well-controlled data.

## Tests Performed

1. Liquidity gaps by maturity bucket.
2. Liquidity gap concentration by currency.
3. Funding concentration by counterparty.
4. Short-term funding concentration.
5. Eligible liquidity buffer after haircut.
6. Non-eligible assets included in liquidity buffer.
7. Liquidity buffer coverage of stressed net outflows.

## Potential Audit Finding

Liquidity gaps were identified in specific maturity buckets and currencies. Funding concentration was also observed among certain counterparties. In addition, non-eligible assets appeared in the liquidity buffer population, indicating potential weaknesses in liquidity data quality, eligibility classification or control monitoring.

## Audit Recommendation

Management should strengthen liquidity risk data controls, ensure consistent classification of eligible liquid assets, monitor funding concentration and enhance escalation procedures for material liquidity gaps or short-term funding pressures.

## Interview Explanation

I used SQL to simulate Internal Audit testing over liquidity risk data. The tests identify maturity buckets with liquidity gaps, currencies with negative net positions, counterparties with high funding concentration and potential issues in the eligibility of liquidity buffer assets. The objective is to show how Internal Audit can use data analytics to assess the quality and effectiveness of liquidity risk controls under ILAAP.
