# Singapore Population Forecasting & Scenario Analysis

An end-to-end, reproducible forecasting project that estimates Singapore's population and communicates uncertainty for planning decisions. It extends a basic linear-regression course assignment into a portfolio project with time-aware validation, model benchmarking, prediction intervals, and an interactive dashboard.

**[Open the live Streamlit dashboard](https://singapore-population-forecasting-cas0801.streamlit.app/)**

## What this project demonstrates

- Data engineering: ingestion, schema checks, and reproducible processing
- Data science: naive-drift, linear, polynomial-ridge, random-forest, and SARIMAX benchmarks
- Evaluation: expanding-window backtesting instead of random train/test splitting
- Decision support: 10-year forecasts, prediction intervals, and low/base/high migration scenarios
- Product delivery: an interactive Streamlit dashboard and documented CLI workflow

## Data

`data/raw/singapore_total_population.csv` is the included, source-traceable primary series. Regenerate it with `python -m src.download_singstat`. The required schema is:

```csv
year,population
1950,1022200
...
```

Use official SingStat annual total-population data as the primary source. Keep a source URL, extraction date, and definition of `population` in `data/SOURCES.md`.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.train --input data/raw/singapore_total_population.csv
streamlit run app.py
```

The training command writes `reports/model_metrics.csv`, `reports/backtest_predictions.csv`, and `reports/forecast.csv`; the dashboard renders the interactive Plotly chart.

## Evaluation design

Models use only past observations to forecast future years. Model selection uses 20 expanding-window one-step forecasts over 2002-2021. The most recent four years (2022-2025) remain untouched until the final stress test. This separation prevents choosing a model after looking at the final evaluation period.

## Current results

| Model | Backtest RMSE (2002-2021) | Holdout RMSE (2022-2025) |
| --- | ---: | ---: |
| SARIMAX | 80,974 | 1,025,400 |
| Naive drift | 97,438 | 336,534 |
| Random forest | 248,936 | 376,237 |
| Polynomial ridge | 360,299 | 93,558 |
| Linear regression | 453,240 | 264,471 |

SARIMAX wins the pre-registered backtest and is therefore used for the published 2026-2035 forecast. Its weak final holdout is an important finding rather than something to hide: a model that performs well on repeated one-year forecasts can fail on a multi-year period containing a structural shock and rebound. The 2035 base estimate is **7.29 million**, with an approximate interval of **6.78-7.79 million**. These intervals are empirical sensitivity bands based on backtest error, not formal demographic confidence intervals.

## Portfolio narrative

Avoid presenting a long-horizon forecast as a certainty. The dashboard should state that demographic forecasts depend on policy, migration, fertility, and shocks. Use scenario analysis to make assumptions explicit.

## Suggested resume bullet

> Built a reproducible Singapore population-forecasting pipeline from 76 years of official SingStat data; benchmarked five regression and time-series approaches across 20 rolling-origin folds and delivered 10-year scenario forecasts in an interactive Streamlit dashboard.

Alternative results-focused bullet:

> Evaluated five forecasting approaches with leakage-safe temporal validation; achieved an 80,974-person rolling RMSE with SARIMAX, diagnosed post-COVID holdout degradation, and communicated model risk through scenario and uncertainty bands.

Do not claim that SARIMAX improved final-holdout accuracy: the results do not support that statement.
