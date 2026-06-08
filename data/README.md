# Data Sources

## Boundary GeoJSON

| Field | Value |
|---|---|
| Dataset | Local Authority Districts (December 2022) UK BGC |
| Source | ONS Open Geography Portal |
| URL | `https://geoportal.statistics.gov.uk` → *Boundaries → Administrative → Local Authority Districts* |
| CRS | WGS84 (EPSG:4326) |
| **Join key** | `LAD22CD` — 9-character ONS Local Authority code (e.g. `E06000001`) |
| Licence | Open Government Licence v3.0 |

The script `download_data.py` fetches a lightweight GeoJSON via the ArcGIS FeatureServer REST API retaining only `LAD22CD` and `LAD22NM` fields to keep the file small.

## Metric CSVs

| File | Description | Source | Join key column |
|---|---|---|---|
| `imd_2019.xlsx` | Index of Multiple Deprivation 2019 — LA average score | MHCLG / data.gov.uk | `Local Authority District code (2019)` → rename to `lad19cd` |
| `unemployment_2023.csv` | Claimant count (April 2023) as % of 16–64 population | ONS NOMIS | `GEOGRAPHY_CODE` → rename to `LAD22CD` |

> **Note**: IMD 2019 uses `lad19cd` codes which map to the same values as `LAD22CD` for most English districts. Scottish and Welsh LAs require separate IMD datasets.

## Git-ignored files

All downloaded files are excluded from version control via `.gitignore`:
```
data/geojson/*.geojson
data/*.csv
data/*.xlsx
```

Re-generate at any time by running:
```bash
python data/download_data.py
```
