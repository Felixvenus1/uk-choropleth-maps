# Data

`download_data.py` fetches both files. The GeoJSON is git-ignored. The IMD workbook is committed.

| File | Source | Join key |
|---|---|---|
| `geojson/local_authorities_2022.geojson` | ONS Open Geography Portal, Local Authority Districts (December 2022) UK BGC, fetched from the ArcGIS FeatureServer with only `LAD22CD` and `LAD22NM` kept | `LAD22CD` |
| `imd_2019.xlsx` | MHCLG, English Indices of Deprivation 2019, local authority district summaries | `Local Authority District code (2019)`, renamed to `LAD22CD` |

The notebook uses the `IMD`, `Income` and `Employment` sheets of the workbook. The 2019 district codes match `LAD22CD` for most English districts. Districts that merged after 2019 have no match and show grey.

Both datasets are under the Open Government Licence v3.0.
