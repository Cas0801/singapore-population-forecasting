# Project findings

## Executive summary

This project forecasts Singapore's total population using 76 annual observations from the Singapore Department of Statistics (1950-2025). It compares a transparent drift baseline with linear regression, polynomial ridge regression, random forest, and SARIMAX.

Model selection is based on 20 expanding-window, one-year-ahead forecasts covering 2002-2021. SARIMAX has the lowest backtest RMSE (80,974), narrowly outperforming naive drift (97,438). The selected model estimates a total population of 6.67 million in 2030 and 7.29 million in 2035.

## The most important result

The untouched 2022-2025 stress test reverses the model ranking. Polynomial ridge records the lowest error in that specific four-year window, while SARIMAX performs poorly. Singapore's sharp 2021 population decline and subsequent rebound expose the difference between repeated one-step forecasting and a fixed multi-step forecast through a structural shock.

This is the project's strongest interview insight: validation must match the intended forecast horizon, and demographic models require monitoring and recalibration when migration policy or external shocks alter the data-generating process.

## Limitations

- Annual data provides only 76 observations, limiting the value of highly flexible models.
- Total population includes non-residents and is strongly affected by migration and policy.
- Statistical definitions change in 1990 and 2003.
- The current models are univariate and do not incorporate fertility, mortality, migration, or policy assumptions.
- Forecast bands approximate uncertainty from historical backtest error and should not be treated as official projections.

## Recommended next iteration

Add lagged births, deaths, resident/non-resident composition, and net migration when future assumptions for those variables can be stated explicitly. Evaluate direct multi-horizon models at 1-, 3-, 5-, and 10-year horizons instead of optimizing only one-step accuracy.
