# Capital & RWA Testing — Audit Explanation

## Audit Objective

The objective of this module is to assess whether regulatory exposure data is complete, reasonably classified and traceable for capital and RWA reporting purposes.

## Regulatory Context

Under prudential regulation, banks must calculate capital requirements based on exposure amounts, regulatory classifications and risk weights. Internal Audit does not replace the regulatory reporting function, but can perform independent reasonableness testing to identify data quality issues, missing classifications or calculation inconsistencies.

## Tests Performed

1. Exposures without regulatory exposure class.
2. Exposures without risk weight.
3. Difference between reported RWA and simplified recalculated RWA.
4. Concentration of RWA exceptions by exposure class.

## Potential Audit Finding

RWA calculation differences and missing regulatory classifications were identified in the simulated dataset. These issues may indicate weaknesses in data quality controls, regulatory classification processes or reconciliation between source systems and reporting outputs.

## Audit Recommendation

Management should strengthen data quality controls over regulatory exposure data, ensure all exposures are assigned valid regulatory classifications and risk weights, and implement periodic reconciliation between source systems and reported RWA figures.

## Interview Explanation

I used SQL to perform reasonableness testing over capital and RWA data, identifying missing classifications, missing risk weights and differences between reported and recalculated RWA. The objective was not to replicate the full Basel III calculation engine, but to demonstrate how Internal Audit can use data analytics to challenge regulatory reporting controls.
