"""Reusable Folium choropleth map builder."""

from __future__ import annotations

from pathlib import Path

import folium
import pandas as pd


class ChoroplethBuilder:
    """Build a Folium choropleth map from a GeoJSON file and a metric DataFrame.

    Parameters
    ----------
    geojson_path:
        Path to a GeoJSON file containing the geographic boundaries.
    data:
        DataFrame with at least two columns: the join key and the metric column.
    join_key:
        Column name present in both the GeoJSON ``feature.properties`` and *data*
        that links geographic features to data rows.
    """

    def __init__(self, geojson_path: str | Path, data: pd.DataFrame, join_key: str) -> None:
        self.geojson_path = str(geojson_path)
        self.data = data
        self.join_key = join_key
        self._map: folium.Map | None = None

    def build(
        self,
        column: str,
        legend_name: str = "",
        fill_color: str = "YlOrRd",
        tiles: str = "CartoDB positron",
        location: tuple[float, float] = (54.5, -3.5),
        zoom_start: int = 6,
    ) -> folium.Map:
        """Generate and return a Folium choropleth map.

        Parameters
        ----------
        column:
            Metric column in *data* to visualise.
        legend_name:
            Label shown on the colour scale legend.
        fill_color:
            Brewer colour scale name (e.g. ``"YlOrRd"``, ``"BuGn"``).
        tiles:
            Base map tile layer name.
        location:
            ``[lat, lon]`` centre of the initial map view.
        zoom_start:
            Initial zoom level.
        """
        m = folium.Map(location=list(location), zoom_start=zoom_start, tiles=tiles)

        choropleth = folium.Choropleth(
            geo_data=self.geojson_path,
            data=self.data,
            columns=[self.join_key, column],
            key_on=f"feature.properties.{self.join_key}",
            fill_color=fill_color,
            fill_opacity=0.75,
            line_opacity=0.3,
            legend_name=legend_name or column,
            nan_fill_color="lightgrey",
        )
        choropleth.add_to(m)

        # Add hover tooltip using GeoJsonTooltip
        geojson_layer = choropleth.geojson
        geojson_layer.add_child(
            folium.features.GeoJsonTooltip(
                fields=[self.join_key],
                aliases=["Area code:"],
            )
        )

        folium.LayerControl().add_to(m)
        self._map = m
        return m

    def save(self, output_path: str | Path) -> None:
        """Save the last built map to an HTML file."""
        if self._map is None:
            raise RuntimeError("Call build() before save().")
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        self._map.save(str(output_path))
