from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Singapore Population Forecasting", layout="wide")
st.title("Singapore Population Forecasting & Scenario Analysis")
st.caption("Forecasts are planning scenarios, not certainties. Validate data definitions before use.")

forecast_path = Path("reports/forecast.csv")
metrics_path = Path("reports/model_metrics.csv")
history_path = Path("data/raw/singapore_total_population.csv")
if not forecast_path.exists() or not metrics_path.exists():
    st.info("Run `python -m src.train --input data/raw/singapore_total_population.csv` first.")
    st.stop()

forecast, metrics, history = pd.read_csv(forecast_path), pd.read_csv(metrics_path), pd.read_csv(history_path)
scenario = st.sidebar.selectbox("Population-growth scenario", ["Base", "Lower growth", "Higher growth"])
annual_delta = {"Lower growth": -0.005, "Base": 0.0, "Higher growth": 0.005}[scenario]
adjusted = forecast.copy()
adjusted["scenario_forecast"] = [
    value * (1 + annual_delta) ** step for step, value in enumerate(adjusted.forecast, start=1)
]
backtest = metrics[metrics.split.eq("backtest")].sort_values("rmse")
holdout = metrics[metrics.split.eq("holdout")].sort_values("rmse")
one, two, three = st.columns(3)
one.metric("Selected model", forecast.model.iloc[0])
two.metric("Backtest RMSE", f"{backtest.iloc[0].rmse:,.0f}")
three.metric("2035 base forecast", f"{forecast.iloc[-1].forecast / 1_000_000:.2f}M")

fig = go.Figure()
fig.add_trace(go.Scatter(x=history.year, y=history.population, name="Observed", line={"color": "#334155"}))
fig.add_trace(go.Scatter(x=adjusted.year, y=adjusted.upper_95, line={"width": 0}, showlegend=False))
fig.add_trace(go.Scatter(x=adjusted.year, y=adjusted.lower_95, fill="tonexty", line={"width": 0}, name="Approx. 95% interval"))
fig.add_trace(go.Scatter(x=adjusted.year, y=adjusted.forecast, name="Base forecast", line={"color": "#2563eb", "width": 3}))
if scenario != "Base":
    fig.add_trace(go.Scatter(x=adjusted.year, y=adjusted.scenario_forecast, name=scenario, line={"dash": "dash"}))
fig.update_layout(xaxis_title="Year", yaxis_title="Population", hovermode="x unified")
st.plotly_chart(fig, width="stretch")

st.subheader("Model evaluation")
left, right = st.columns(2)
left.caption("Expanding-window backtest (2002-2021) - used for model selection")
left.dataframe(backtest.style.format({"rmse": "{:,.0f}", "mae": "{:,.0f}", "mape": "{:.2%}"}), width="stretch")
right.caption("Untouched final holdout (2022-2025) - reported after selection")
right.dataframe(holdout.style.format({"rmse": "{:,.0f}", "mae": "{:,.0f}", "mape": "{:.2%}"}), width="stretch")
st.caption("Scenario lines apply a transparent ±0.5 percentage-point annual adjustment. They are sensitivity tests, not causal migration forecasts.")
