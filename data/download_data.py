"""Download ONS Local Authority boundary GeoJSON and metric CSVs."""

from __future__ import annotations

import urllib.request
from pathlib import Path

GEOJSON_DIR = Path(__file__).parent / "geojson"
DATA_DIR = Path(__file__).parent

GEOJSON_URL = (
    "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/"
    "Local_Authority_Districts_December_2022_UK_BGC_V2/FeatureServer/0/query"
    "?where=1%3D1&outFields=LAD22CD,LAD22NM&outSR=4326&f=geojson"
)

# MHCLG / ONS IMD 2019 — Local Authority District summaries (England).
# The workbook has one sheet per deprivation domain (IMD, Income, Employment, ...),
# from which the notebook builds three different choropleth metrics.
IMD_URL = (
    "https://assets.publishing.service.gov.uk/government/uploads/"
    "system/uploads/attachment_data/file/833995/"
    "File_10_-_IoD2019_Local_Authority_District_Summaries__lower-tier__.xlsx"
)


def _download(url: str, dest: Path) -> None:
    if dest.exists():
        print(f"  already exists: {dest.name}")
        return
    print(f"  downloading {dest.name} ...")
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=120) as resp, open(dest, "wb") as fh:
        fh.write(resp.read())
    print(f"  saved {dest.stat().st_size // 1024:,} KB")


def main() -> None:
    GEOJSON_DIR.mkdir(parents=True, exist_ok=True)

    print("Fetching LA boundary GeoJSON ...")
    _download(GEOJSON_URL, GEOJSON_DIR / "local_authorities_2022.geojson")

    print("Fetching IMD 2019 summary (XLSX) ...")
    _download(IMD_URL, DATA_DIR / "imd_2019.xlsx")

    print("Done. Run the notebook to generate maps.")


if __name__ == "__main__":
    main()
