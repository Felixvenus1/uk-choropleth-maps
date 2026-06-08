"""Tests for ChoroplethBuilder using a minimal synthetic GeoJSON fixture."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pandas as pd
import pytest

from src.choropleth_builder import ChoroplethBuilder


@pytest.fixture()
def geojson_file(tmp_path: Path) -> Path:
    """Write a tiny 3-feature GeoJSON to a temp file."""
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"LAD22CD": f"E0600000{i}", "LAD22NM": f"Area {i}"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-1.0 + i * 0.1, 51.0],
                            [-0.9 + i * 0.1, 51.0],
                            [-0.9 + i * 0.1, 51.1],
                            [-1.0 + i * 0.1, 51.1],
                            [-1.0 + i * 0.1, 51.0],
                        ]
                    ],
                },
            }
            for i in range(3)
        ],
    }
    p = tmp_path / "test.geojson"
    p.write_text(json.dumps(geojson))
    return p


@pytest.fixture()
def metric_df() -> pd.DataFrame:
    return pd.DataFrame({
        "LAD22CD": ["E06000000", "E06000001", "E06000002"],
        "score": [10.5, 25.3, 8.1],
    })


def test_build_returns_folium_map(geojson_file, metric_df):
    import folium
    builder = ChoroplethBuilder(geojson_file, metric_df, join_key="LAD22CD")
    m = builder.build(column="score", legend_name="Test Score")
    assert isinstance(m, folium.Map)


def test_build_sets_internal_map(geojson_file, metric_df):
    builder = ChoroplethBuilder(geojson_file, metric_df, join_key="LAD22CD")
    builder.build(column="score")
    assert builder._map is not None


def test_save_writes_html(geojson_file, metric_df, tmp_path):
    builder = ChoroplethBuilder(geojson_file, metric_df, join_key="LAD22CD")
    builder.build(column="score")
    out = tmp_path / "out.html"
    builder.save(out)
    assert out.exists()
    assert out.stat().st_size > 100


def test_save_creates_parent_dir(geojson_file, metric_df, tmp_path):
    builder = ChoroplethBuilder(geojson_file, metric_df, join_key="LAD22CD")
    builder.build(column="score")
    out = tmp_path / "nested" / "dir" / "map.html"
    builder.save(out)
    assert out.exists()


def test_save_without_build_raises(geojson_file, metric_df):
    builder = ChoroplethBuilder(geojson_file, metric_df, join_key="LAD22CD")
    with pytest.raises(RuntimeError, match="build\\(\\)"):
        builder.save("/tmp/x.html")


def test_custom_fill_color(geojson_file, metric_df):
    builder = ChoroplethBuilder(geojson_file, metric_df, join_key="LAD22CD")
    m = builder.build(column="score", fill_color="BuGn")
    import folium
    assert isinstance(m, folium.Map)
