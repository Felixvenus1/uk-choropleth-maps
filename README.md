# uk-choropleth-maps

Interactive and static choropleth maps of UK Local Authority statistics, built with [Folium](https://python-visualization.github.io/folium/) and [Plotly Express](https://plotly.com/python/plotly-express/).

Maps are exported as self-contained `.html` files — download and open locally, no server required.

## Maps Produced

| Map | Metric | Tool | Output |
|---|---|---|---|
| Index of Multiple Deprivation | IMD Score (2019) | Folium | `outputs/maps/imd_map.html` |
| Median Household Income | £ per year (2020) | Folium | `outputs/maps/income_map.html` |
| Unemployment Rate | % (2022) | Folium + Plotly | `outputs/maps/unemployment_map.html` |

## Quick Start

```bash
pip install -r requirements.txt

# Download GeoJSON + metric CSVs from ONS
python data/download_data.py

# Run the notebook
jupyter lab notebooks/map_exploration.ipynb

# Or run the builder directly
python -c "
from src.choropleth_builder import ChoroplethBuilder
import pandas as pd
df = pd.read_csv('data/imd_2019.csv')
m = ChoroplethBuilder('data/geojson/local_authorities.geojson', df, join_key='lad19cd').build(column='imd_score', legend_name='IMD Score')
m.save('outputs/maps/imd_map.html')
"
```

## `ChoroplethBuilder` API

```python
from src.choropleth_builder import ChoroplethBuilder

builder = ChoroplethBuilder(
    geojson_path="data/geojson/local_authorities.geojson",
    data=df,           # pandas DataFrame
    join_key="lad19cd" # column in both GeoJSON and df that links them
)

folium_map = builder.build(
    column="imd_score",      # metric column in df
    legend_name="IMD Score", # label for map legend
    fill_color="YlOrRd",     # Brewer colour scale
    tiles="CartoDB positron" # base tile layer
)
folium_map.save("outputs/maps/imd_map.html")
```

## Data Sources

| Dataset | Source | Licence |
|---|---|---|
| Local Authority GeoJSON (2019) | ONS Open Geography Portal | OGL v3 |
| Index of Multiple Deprivation 2019 | MHCLG / data.gov.uk | OGL v3 |
| Median Household Income 2020 | ONS | OGL v3 |
| Unemployment Rate 2022 | ONS NOMIS | OGL v3 |

## Project Structure

```
uk-choropleth-maps/
├── notebooks/
│   └── map_exploration.ipynb  # EDA + all 3 maps
├── src/
│   └── choropleth_builder.py  # ChoroplethBuilder class
├── data/
│   ├── download_data.py       # Fetch GeoJSON + CSVs
│   ├── geojson/               # UK LA boundary files (git-ignored)
│   └── README.md              # Data source provenance
├── outputs/
│   └── maps/                  # Exported .html maps (git-ignored)
├── tests/
│   └── test_builder.py
├── requirements.txt
└── pyproject.toml
```

## Licence

Code: MIT. Data: Open Government Licence v3.0.
