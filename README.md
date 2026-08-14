# Singapore Population Forecasting and Scenario Analysis

An end to end forecasting system built from 76 years of official Singapore population data. It compares five statistical and machine learning models using temporal validation, produces population forecasts from 2026 to 2035, and presents the results through an interactive dashboard.

<a href="https://singapore&#45;population&#45;forecasting&#45;cas0801.streamlit.app/">Open the live dashboard</a> · <a href="PROJECT_REPORT.md">Read the project report</a> · <a href="data/SOURCES.md">Review the data source</a>

## Project overview

<table>
  <tr>
    <th>Data</th>
    <th>Validation</th>
    <th>Selected model</th>
    <th>Backtest RMSE</th>
    <th>2035 forecast</th>
  </tr>
  <tr>
    <td>SingStat, 1950 to 2025</td>
    <td>20 rolling origin folds</td>
    <td>SARIMAX</td>
    <td>80,974 people</td>
    <td>7.29 million</td>
  </tr>
</table>

## Why this project matters

A random split is misleading for forecasting because it can train on future observations and test on earlier observations. This project follows chronological order so that every prediction uses only information available before the target year.

Model selection uses 20 historical forecasts covering 2002 to 2021. The observations from 2022 to 2025 remain untouched until the final stress test.

The most important finding is not the headline population estimate. SARIMAX performs best during historical rolling validation, but performs poorly through the population rebound after COVID. This reversal demonstrates why forecast horizon, structural change, and model monitoring matter.

## Workflow

1. Download the official annual population series from SingStat.
2. Validate the schema, year sequence, duplicate records, and population values.
3. Generate 20 expanding window forecasts using only historical information.
4. Compare naive drift, linear regression, polynomial ridge, random forest, and SARIMAX.
5. Select the model using historical backtest RMSE.
6. Evaluate the selected model once on the untouched final period.
7. Refit the model on all available observations and forecast 2026 to 2035.
8. Present forecasts, uncertainty bands, and growth scenarios in Streamlit.

## Model results

<table>
  <tr>
    <th>Model</th>
    <th>Backtest RMSE, 2002 to 2021</th>
    <th>Final holdout RMSE, 2022 to 2025</th>
  </tr>
  <tr><td>SARIMAX</td><td><strong>80,974</strong></td><td>1,025,400</td></tr>
  <tr><td>Naive drift</td><td>97,438</td><td>336,534</td></tr>
  <tr><td>Random forest</td><td>248,936</td><td>376,237</td></tr>
  <tr><td>Polynomial ridge</td><td>360,299</td><td><strong>93,558</strong></td></tr>
  <tr><td>Linear regression</td><td>453,240</td><td>264,471</td></tr>
</table>

SARIMAX improves rolling RMSE by 16.9% compared with naive drift. Its weak final holdout result shows that a model optimized for repeated one year forecasts can still fail during a longer structural shock.

Polynomial ridge performs best during the final holdout period. It is reported transparently, but it is not selected after viewing the final test results because doing so would introduce selection bias.

The selected model estimates 6.67 million people in 2030 and 7.29 million in 2035. The approximate 2035 sensitivity interval is 6.78 million to 7.79 million. These values are planning scenarios rather than official demographic projections.

## Validation design

```text
Train through 2001 → predict 2002
Train through 2002 → predict 2003
Continue until the prediction for 2021
Select the model using all 20 historical folds
Evaluate once using the untouched 2022 to 2025 period
Refit using all available data
Forecast 2026 to 2035
```

RMSE is the main selection metric. MAE and MAPE are also reported for interpretation. Detailed predictions for every fold are available in [`reports/backtest_predictions.csv`](reports/backtest_predictions.csv).

## Data

The target is the SingStat `Total Population` series with resource identifier `M810001`. It includes residents and non residents. The source contains definition changes around 1990 and 2003. These changes are documented in [`data/SOURCES.md`](data/SOURCES.md).

The included downloader can regenerate the official dataset. The data validation module checks required columns, numeric values, unique years, positive population values, and annual continuity.

## Run the project

Create a Python environment and install the packages listed in `requirements.txt`. Then run the training module, followed by the dashboard:

```text
streamlit run app.py
```

Run the automated checks with:

```text
pytest
```

## Repository structure

```text
├── app.py
├── src/
│   ├── data.py
│   ├── download_singstat.py
│   ├── models.py
│   └── train.py
├── data/
├── reports/
├── tests/
├── PROJECT_REPORT.md
└── requirements.txt
```

## Technology

Python · pandas · NumPy · scikit learn · statsmodels · Plotly · Streamlit · pytest

## Limitations and future work

1. The dataset contains only 76 annual observations, so deep learning is not well justified.
2. Total population is strongly affected by migration policy and non resident flows.
3. Model selection currently focuses on one year forecasts, while the published forecast covers ten years.
4. The uncertainty bands are empirical sensitivity bands rather than official confidence intervals.
5. A future version should evaluate one, three, five, and ten year horizons and include explicit assumptions for births, deaths, and migration.
