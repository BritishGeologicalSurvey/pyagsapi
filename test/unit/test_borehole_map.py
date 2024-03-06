"""
Tests for borehole_map.py
"""
from pathlib import Path

from geojson_pydantic import FeatureCollection

from app.borehole_map import extract_geojson

TEST_FILE_DIR = Path(__file__).parent.parent / 'files'


def test_extract_geojson_example_ags():
    # Arrange
    filepath = TEST_FILE_DIR / 'example_ags.ags'

    # Act
    result = extract_geojson(filepath)

    # Assert
    # Creation of FeatureCollection ensures correct fields exist
    feature_collection = FeatureCollection(**result)
    assert len(feature_collection) == 1

    feature = feature_collection[0]
    assert feature.properties['PROJ_ID'] == '121415'
    assert feature.properties['LOCA_ID'] == '327-16A'
    assert 'LOCA_FILE_FSET' in feature.properties
    assert 'PROJ_FILE_FSET' in feature.properties
    assert feature.id == '121415.327-16A'
    lon, lat = feature.geometry.coordinates
    assert -180 <= lon <= 180
    assert -90 <= lat <= 90
