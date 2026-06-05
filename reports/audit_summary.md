# Regulatory Risk Audit Analytics — Audit Summary

## Objective

This report summarises the results of simulated data-driven Internal Audit tests over capital and RWA, ICAAP and RAF, ILAAP, and IFRS 9.

## Important Disclaimer

The datasets are fully synthetic and the tests are simplified. The purpose of this project is not to replicate full regulatory, capital, liquidity or IFRS 9 models, but to demonstrate how Internal Audit can use SQL and Python to identify control exceptions, data quality issues and reasonableness concerns.

## Findings Summary

### IFRS 9 — Loans with missing PD, LGD or EAD inputs

- Exceptions identified: 81
- Risk rating: HIGH
- Audit interpretation: Missing IFRS 9 model inputs may affect the completeness and reliability of expected credit loss calculations.

### Capital & RWA — Reported RWA differs from simplified recalculated RWA

- Exceptions identified: 77
- Risk rating: HIGH
- Audit interpretation: Differences between reported and recalculated RWA may indicate calculation, mapping or reconciliation issues requiring further audit investigation.

### IFRS 9 — Reported ECL differs from simplified recalculated ECL

- Exceptions identified: 61
- Risk rating: HIGH
- Audit interpretation: Differences between reported and recalculated ECL may indicate model input, calculation or reconciliation issues requiring further review.

### ICAAP & RAF — Risk Appetite Framework limit breaches

- Exceptions identified: 7
- Risk rating: LOW
- Audit interpretation: RAF breaches indicate areas where current risk levels exceed approved appetite and require governance attention.

### ILAAP — Funding concentration above 10% by counterparty

- Exceptions identified: 6
- Risk rating: LOW
- Audit interpretation: High funding concentration may increase vulnerability to counterparty withdrawal or market stress.

### ICAAP & RAF — Material risks without assigned internal capital

- Exceptions identified: 3
- Risk rating: LOW
- Audit interpretation: Material risks without assigned capital may indicate weaknesses in ICAAP completeness, risk quantification or governance.

### ICAAP & RAF — Material risks without assigned risk owner

- Exceptions identified: 3
- Risk rating: LOW
- Audit interpretation: Material risks without clear ownership may weaken accountability, monitoring and escalation within the risk governance framework.

### ILAAP — Negative liquidity gaps by maturity bucket

- Exceptions identified: 3
- Risk rating: LOW
- Audit interpretation: Negative liquidity gaps in maturity buckets may indicate liquidity mismatch requiring monitoring, escalation or contingency funding actions.

### ICAAP & RAF — RAF breaches not escalated to committee

- Exceptions identified: 2
- Risk rating: LOW
- Audit interpretation: Risk appetite breaches without escalation may indicate weaknesses in governance discipline and breach management procedures.

### ILAAP — Non-eligible assets identified in liquidity buffer population

- Exceptions identified: 42
- Risk rating: MEDIUM
- Audit interpretation: Non-eligible assets within the liquidity buffer population may indicate classification or data quality issues.

### Capital & RWA — Exposures without regulatory exposure class

- Exceptions identified: 29
- Risk rating: MEDIUM
- Audit interpretation: Missing regulatory exposure classifications may indicate data quality weaknesses affecting RWA calculation and prudential reporting.

### IFRS 9 — Loans with 30+ days past due still classified as Stage 1

- Exceptions identified: 28
- Risk rating: MEDIUM
- Audit interpretation: Loans with 30+ days past due remaining in Stage 1 may indicate staging inconsistencies or delayed recognition of credit deterioration.

### Capital & RWA — Exposures without risk weight

- Exceptions identified: 23
- Risk rating: MEDIUM
- Audit interpretation: Missing risk weights may prevent accurate RWA calculation and weaken regulatory reporting controls.

### IFRS 9 — Loans with 90+ days past due not classified as Stage 3

- Exceptions identified: 21
- Risk rating: MEDIUM
- Audit interpretation: Loans with default indicators not classified as Stage 3 may indicate weaknesses in default identification or staging controls.

## Audit Interpretation

The results show how data analytics can support Internal Audit by moving from sample-based review to population-level exception identification. The findings would require validation with process owners, assessment of data lineage, review of control design and evaluation of whether issues are isolated or systemic.

## Recommended Next Steps

1. Validate exceptions with process owners.
2. Confirm data lineage and source system reliability.
3. Assess whether exceptions are isolated or systemic.
4. Identify root causes and control weaknesses.
5. Agree remediation actions, owners and deadlines.
6. Perform follow-up testing.

## Interview Explanation

I used Python to consolidate exceptions from multiple regulatory risk audit areas, assign severity levels and generate an audit-style summary. The purpose was to demonstrate how data analytics can help Internal Audit prioritise findings, structure evidence and support professional judgement.
