from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error

from src.data import load_population
from src.models import fit_predict_sarimax, make_models, predict_drift


def score(actual, predicted):
    return {
        "rmse": mean_squared_error(actual, predicted) ** 0.5,
        "mae": mean_absolute_error(actual, predicted),
        "mape": mean_absolute_percentage_error(actual, predicted),
    }


def predict_model(name: str, model, train: pd.DataFrame, years: np.ndarray) -> np.ndarray:
    if name == "naive_drift":
        return predict_drift(train, years)
    if name == "sarimax":
        return fit_predict_sarimax(train, years)
    fitted = clone(model).fit(train[["year"]], train.population)
    return fitted.predict(pd.DataFrame({"year": years}))


def run(input_path: str, horizon: int = 10) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    data = load_population(input_path)
    holdout_size = 4
    train, holdout = data.iloc[:-holdout_size], data.iloc[-holdout_size:]
    models = {"naive_drift": None, **make_models(), "sarimax": None}
    rows, prediction_rows = [], []

    # Model selection uses only pre-holdout history: one-step expanding-window forecasts.
    backtest_start = max(30, len(train) - 20)
    for cutoff in range(backtest_start, len(train)):
        fold_train = train.iloc[:cutoff]
        actual = train.iloc[cutoff]
        for name, model in models.items():
            predicted = float(predict_model(name, model, fold_train, np.array([actual.year]))[0])
            prediction_rows.append(
                {"split": "backtest", "model": name, "year": int(actual.year),
                 "actual": float(actual.population), "predicted": predicted,
                 "error": float(actual.population - predicted)}
            )

    predictions = pd.DataFrame(prediction_rows)
    for name, group in predictions.groupby("model"):
        rows.append({"model": name, "split": "backtest", "n": len(group), **score(group.actual, group.predicted)})

    # The untouched 2022-2025 holdout is reported once, after selection.
    for name, model in models.items():
        predicted = predict_model(name, model, train, holdout.year.to_numpy())
        rows.append({"model": name, "split": "holdout", "n": len(holdout), **score(holdout.population, predicted)})
        for (_, actual), value in zip(holdout.iterrows(), predicted):
            prediction_rows.append(
                {"split": "holdout", "model": name, "year": int(actual.year),
                 "actual": float(actual.population), "predicted": float(value),
                 "error": float(actual.population - value)}
            )

    metrics = pd.DataFrame(rows).sort_values(["split", "rmse"]).reset_index(drop=True)
    winner = metrics.loc[metrics.split.eq("backtest")].iloc[0].model
    future_years = np.arange(data.year.max() + 1, data.year.max() + horizon + 1)
    future = predict_model(winner, models[winner], data, future_years)
    forecast = pd.DataFrame({"year": future_years, "forecast": future, "model": winner})
    residual_scale = metrics.loc[(metrics.model.eq(winner)) & metrics.split.eq("backtest"), "rmse"].iloc[0]
    forecast["lower_95"] = (forecast.forecast - 1.96 * residual_scale * np.sqrt(np.arange(1, horizon + 1))).clip(lower=0)
    forecast["upper_95"] = forecast.forecast + 1.96 * residual_scale * np.sqrt(np.arange(1, horizon + 1))
    return metrics, forecast, pd.DataFrame(prediction_rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--horizon", type=int, default=10)
    args = parser.parse_args()
    metrics, forecast, predictions = run(args.input, args.horizon)
    Path("reports").mkdir(parents=True, exist_ok=True)
    metrics.to_csv("reports/model_metrics.csv", index=False)
    forecast.to_csv("reports/forecast.csv", index=False)
    predictions.to_csv("reports/backtest_predictions.csv", index=False)
    print(metrics.to_string(index=False))
    print("Saved metrics, forecast, and backtest predictions under reports/")


if __name__ == "__main__":
    main()
