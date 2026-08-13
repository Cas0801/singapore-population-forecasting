import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.tsa.statespace.sarimax import SARIMAX


def make_models() -> dict:
    return {
        "linear": LinearRegression(),
        "polynomial_ridge": make_pipeline(PolynomialFeatures(2), Ridge(alpha=1.0)),
        "random_forest": RandomForestRegressor(n_estimators=300, min_samples_leaf=2, random_state=42),
    }


def predict_drift(train: pd.DataFrame, forecast_years: np.ndarray) -> np.ndarray:
    """Forecast by extending the average annual change observed in the training set."""
    elapsed = train.year.iloc[-1] - train.year.iloc[0]
    annual_change = (train.population.iloc[-1] - train.population.iloc[0]) / elapsed
    steps = forecast_years - train.year.iloc[-1]
    return train.population.iloc[-1] + annual_change * steps


def fit_predict_sarimax(train: pd.DataFrame, forecast_years: np.ndarray) -> np.ndarray:
    series = train.set_index("year")["population"]
    series.index = pd.PeriodIndex(series.index.astype(str), freq="Y")
    model = SARIMAX(series, order=(1, 1, 0), trend="t", enforce_stationarity=False).fit(disp=False)
    return model.forecast(len(forecast_years)).to_numpy()
