# uk-choropleth-maps

Choropleth maps of deprivation in English local authorities, using the IMD 2019 scores on ONS December 2022 boundaries. There are three Folium maps (overall IMD, income, employment) and one Plotly Express version of the IMD map. Each is saved as a standalone HTML file.

| IMD | Income | Employment |
|---|---|---|
| ![IMD](docs/previews/imd_preview.png) | ![Income](docs/previews/income_preview.png) | ![Employment](docs/previews/employment_preview.png) |

## Run

```bash
pip install -r requirements.txt
python data/download_data.py     # boundary GeoJSON, about 19 MB
jupyter lab notebooks/map_exploration.ipynb
```

The notebook writes `imd_map.html`, `income_map.html`, `employment_map.html` and `imd_plotly.html` to `outputs/maps/`. The three Folium maps are committed. The Plotly one is about 7 MB, so it is only generated locally. IMD 2019 covers England only, so Scottish, Welsh and Northern Irish areas show grey.

`src/choropleth_builder.py` has a small `ChoroplethBuilder` class that takes a GeoJSON path, a DataFrame and a join key, and builds and saves a Folium map.

Tests: `pytest`

Code is MIT. Data is under the Open Government Licence v3.0. See `data/README.md` for sources.
