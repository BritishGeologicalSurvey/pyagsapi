"""
Tests for borehole_map.py
"""
from pathlib import Path

from geojson_pydantic import FeatureCollection
import pytest

from app.borehole_map import extract_geojson

TEST_FILE_DIR = Path(__file__).parent.parent / 'files'


def test_extract_geojson_example_ags():
    # Arrange
    ags_filepath = TEST_FILE_DIR / 'example_ags.ags'

    # Act
    result = extract_geojson(ags_filepath)

    # Assert
    # Creation of FeatureCollection ensures correct fields exist
    feature_collection = FeatureCollection(**result)
    assert isinstance(feature_collection, FeatureCollection)
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


@pytest.mark.parametrize('ags_filepath, expected_error',  [
    (TEST_FILE_DIR / 'real' / 'Cowlairs park.ags',
     'ERROR: File contains duplicate headers'),
    (TEST_FILE_DIR / 'real' / 'A4106.ags',
     'ERROR: LOCA group missing from '),
    (TEST_FILE_DIR / 'real' / 'A487 Pont ar Dyfi Improvement.ags',
     'Line 106 does not have the same number of entries as the HEADING row in GEOL.'),
    (TEST_FILE_DIR / 'real' / 'PE131061.ags',
     'ERROR: File cannot be read, please use AGS checker to confirm format errors'),
])
def test_extract_geojson_bad_files(ags_filepath, expected_error):
    # Act and assert
    with pytest.raises(ValueError, match=expected_error):
        extract_geojson(ags_filepath)


"""
# This commented-out test can be used to attempt to parse all files and
# see the range of potential exceptions.

@pytest.mark.skip(reason="Only used to find range of potential exceptions")
@pytest.mark.parametrize('ags_filepath',
    list((TEST_FILE_DIR / 'real').glob('*.ags'))
    )
def test_extract_geojson_real_files(ags_filepath):
    # Act
    result = extract_geojson(ags_filepath)

    # Assert
    # Creation of FeatureCollection ensures correct fields exist
    feature_collection = FeatureCollection(**result)
    assert isinstance(feature_collection, FeatureCollection)
"""