"""Download the official SingStat annual total-population series."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from urllib.request import urlopen

import pandas as pd


API_URL = "https://tablebuilder.singstat.gov.sg/api/table/tabledata/M810001"


def download(output: str | Path) -> pd.DataFrame:
    with urlopen(API_URL, timeout=30) as response:
        payload = json.load(response)
    series = next(row for row in payload["Data"]["row"] if row["rowText"] == "Total Population")
    result = pd.DataFrame(series["columns"]).rename(columns={"key": "year", "value": "population"})
    result["year"] = result["year"].astype(int)
    result["population"] = pd.to_numeric(result["population"], errors="raise").astype(int)
    result = result.sort_values("year").reset_index(drop=True)
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=False)
    print(f"Saved {len(result)} annual observations to {output}; extracted {date.today().isoformat()}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/raw/singapore_total_population.csv")
    args = parser.parse_args()
    download(args.output)
