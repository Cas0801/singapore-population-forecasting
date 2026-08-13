# Sources and data decisions

## Primary series

- **Dataset:** `Indicators On Population, Annual` (`M810001`)
- **Publisher:** Singapore Department of Statistics (SingStat)
- **API:** `https://tablebuilder.singstat.gov.sg/api/table/tabledata/M810001`
- **Selected row:** `Total Population`
- **Extraction date:** 2026-08-10
- **Coverage at extraction:** 1950-2025

`Total Population` includes residents (citizens and permanent residents) and non-residents. The source notes a methodology break: values before 1990 use a *de facto* concept; from 1990 they use a *de jure* usual-residence concept. From 2003 onward, residents overseas continuously for at least 12 months are excluded. This makes a single uninterrupted long-run trend useful for benchmarking but unsuitable for causal interpretation without modelling the breaks.

## Reproducibility

Regenerate the local CSV with:

```bash
python -m src.download_singstat
```

Do not replace this series with resident population or citizen population while keeping the same filename. Those are different targets and should be analysed separately.
