# IFRS 9 Staging & ECL Testing — Audit Explanation

## Audit Objective

The objective of this module is to assess whether IFRS 9 staging and expected credit loss data are complete, reasonable and consistent with basic credit deterioration indicators.

## Regulatory Context

IFRS 9 requires financial institutions to recognise expected credit losses based on credit risk deterioration. Loans are generally classified into stages depending on whether credit risk has increased significantly or whether the exposure is credit-impaired.

From an Internal Audit perspective, the objective is not to rebuild the full impairment model, but to test whether staging, input data and ECL outputs are reasonable, consistent and supported by reliable data.

## Tests Performed

1. Loans with 30+ days past due still classified as Stage 1.
2. Loans with 90+ days past due not classified as Stage 3.
3. Significant PD increase while the loan remains in Stage 1.
4. Missing PD, LGD or EAD inputs.
5. Simplified ECL reasonableness recalculation.
6. ECL coverage ratio by stage.
7. Stage distribution by exposure.

## Potential Audit Finding

Loans were identified with potential staging inconsistencies, including exposures with 30+ days past due still classified as Stage 1 and loans with 90+ days past due not classified as Stage 3. Differences between reported ECL and simplified recalculated ECL may indicate weaknesses in data quality, staging logic, model inputs or reconciliation controls.

## Audit Recommendation

Management should strengthen IFRS 9 staging controls, ensure timely identification of significant increases in credit risk, validate PD/LGD/EAD input completeness and implement periodic reasonableness checks over ECL outputs.

## Interview Explanation

I used SQL to simulate Internal Audit testing over IFRS 9 staging and expected credit loss data. The objective was not to replicate the full IFRS 9 impairment model, but to identify potential control exceptions such as loans with deterioration indicators remaining in Stage 1, default indicators not reflected in Stage 3, missing model inputs and material differences between reported and simplified recalculated ECL.
