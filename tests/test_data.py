import pandas as pd
import pytest

from src.data import load_population
from src.models import predict_drift


def test_load_population_rejects_missing_year(tmp_path):
    path = tmp_path / "population.csv"
    pd.DataFrame({"year": [2020, 2022], "population": [5, 6]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="consecutive"):
        load_population(path)


def test_load_population_sorts_valid_data(tmp_path):
    path = tmp_path / "population.csv"
    pd.DataFrame({"year": [2021, 2020], "population": [6, 5]}).to_csv(path, index=False)
    assert load_population(path).year.tolist() == [2020, 2021]


def test_drift_uses_only_training_change():
    train = pd.DataFrame({"year": [2018, 2019, 2020], "population": [100, 110, 120]})
    assert predict_drift(train, pd.Series([2021, 2022]).to_numpy()).tolist() == [130, 140]
