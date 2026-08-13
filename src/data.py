from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {"year", "population"}


def load_population(path: str | Path) -> pd.DataFrame:
    """Load and validate annual population data without silently repairing it."""
    data = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    data = data.loc[:, ["year", "population"]].copy()
    data["year"] = pd.to_numeric(data["year"], errors="raise").astype(int)
    data["population"] = pd.to_numeric(data["population"], errors="raise")
    data = data.sort_values("year").reset_index(drop=True)
    if data.year.duplicated().any() or (data.population <= 0).any():
        raise ValueError("Years must be unique and population values must be positive.")
    if not data.year.diff().dropna().eq(1).all():
        raise ValueError("Annual data must contain consecutive years; resolve gaps explicitly.")
    return data
