"""Tests for API responses."""
from io import BytesIO
import re
import zipfile

import pytest
import requests

from app.routes import ags_export_by_polygon

from test.fixtures import API_VERSION, IN_GITHUB_ACTIONS


@pytest.mark.xfail(IN_GITHUB_ACTIONS, reason="Upstream URL not available from Github Actions")
@pytest.mark.parametrize('count_only', [None, False])
def test_get_ags_exporter_by_polygon(client, count_only):
    # Arrange
    # There should be 4 boreholes within 2 projects in this area
    polygon = 'POLYGON((-3.946 56.063,-3.640 56.063,-3.640 55.966,-3.946 55.966,-3.946 56.063))'

    query = f'{API_VERSION}/ags_export_by_polygon/?polygon={polygon}'
    if count_only is not None:
        query += '&count_only=False'
    # Define the expected borehole and project IDs and zipped AGS file to use for the test
    bgs_loca_ids = ['20200205093727287903', '20200205093728297906', '20200205093728297908', '20200205093728297910']
    bgs_proj_ids = {id_[:16] for id_ in bgs_loca_ids}  # unique ids when truncated to 16 digits
    ags_file_names = {f'{id_}.ags' for id_ in bgs_proj_ids}
    ags_metadata_file_name = 'FILE/BGSFileSet01/BGS_download_metadata.txt'

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == 'attachment; filename="boreholes.zip"'
    assert response.headers["Content-Type"] == "application/x-zip-compressed"
    assert len(response.content) > 0

    assert zipfile.is_zipfile(BytesIO(response.content))
    with zipfile.ZipFile(BytesIO(response.content)) as ags_zip:
        # Check that zip contains the correct files
        assert ags_file_names | {ags_metadata_file_name} == set(ags_zip.namelist())
        with ags_zip.open(ags_metadata_file_name) as metadata_file:
            metadata_text = metadata_file.read().decode()
            for bgs_loca_id in bgs_loca_ids:
                assert bgs_loca_id in metadata_text
            for bgs_proj_id in bgs_proj_ids:
                assert f'Project : {bgs_proj_id}' in metadata_text


@pytest.mark.xfail(IN_GITHUB_ACTIONS, reason="Upstream URL not available from Github Actions")
def test_get_ags_exporter_by_polygon_with_more_than_10_polygons(client):
    # Arrange
    # There should be 28 boreholes in this area, this should pass for a limit of 50,
    # and it should fail for a limit of 10
    polygon = 'POLYGON((-3.946 56.065,-3.640 56.065,-3.640 55.966,-3.946 55.966,-3.946 56.065))'
    query = f'{API_VERSION}/ags_export_by_polygon/?polygon={polygon}'
    ags_metadata_file_name = 'FILE/BGSFileSet01/BGS_download_metadata.txt'

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == 'attachment; filename="boreholes.zip"'
    assert response.headers["Content-Type"] == "application/x-zip-compressed"
    assert len(response.content) > 0

    assert zipfile.is_zipfile(BytesIO(response.content))
    with zipfile.ZipFile(BytesIO(response.content)) as ags_zip:
        # Check that metadata.txt lists 28 loca IDs
        with ags_zip.open(ags_metadata_file_name) as metadata_file:
            # find the pattern 20200205093727287902;20200205093727287903;2020...
            regex = r'\d+(;\d+)+'
            metadata_text = metadata_file.read().decode()
            match = re.search(regex, metadata_text)
            assert match
            assert len(match.group(0).split(';')) == 28


@pytest.mark.parametrize('polygon, count', [
    ('POLYGON((-3.946 56.061,-3.640 56.061,-3.640 55.966,-3.946 55.966,-3.946 56.061))', 0),
    ('POLYGON((-3.946 56.063,-3.640 56.063,-3.640 55.966,-3.946 55.966,-3.946 56.063))', 4),
    ('POLYGON((-3.946 56.065,-3.640 56.065,-3.640 55.966,-3.946 55.966,-3.946 56.065))', 28),
])
def test_get_ags_exporter_by_polygon_count_only(client, polygon, count):
    # Arrange
    query = f'{API_VERSION}/ags_export_by_polygon/?polygon={polygon}&count_only=True'

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert body['msg'] == 'Borehole count'
    assert body['type'] == 'success'
    assert body['self'] is not None
    assert body['count'] == count


def test_get_ags_exporter_by_polygon_too_many_boreholes(client):
    # Arrange
    # There should be more than BOREHOLE_EXPORT_LIMIT, e.g. 50, boreholes in this area
    polygon = 'POLYGON((-3.109 55.895,-3.109 55.906,-3.077 55.906,-3.077 55.895,-3.109 55.895))'
    query = f'{API_VERSION}/ags_export_by_polygon/?polygon={polygon}'

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 422
    body = response.json()
    assert body['errors'][0]['desc'].startswith(f'More than {ags_export_by_polygon.BOREHOLE_EXPORT_LIMIT} boreholes (')
    assert body['errors'][0]['desc'].endswith(') found in the given polygon. Please try with a smaller polygon')
    assert int(body['errors'][0]['desc'].replace(')', '(').split('(')[1]) > ags_export_by_polygon.BOREHOLE_EXPORT_LIMIT


def test_get_ags_exporter_by_polygon_no_boreholes(client):
    # Arrange
    polygon = 'POLYGON((-3.946 56.061,-3.640 56.061,-3.640 55.966,-3.946 55.966,-3.946 56.061))'
    query = f'{API_VERSION}/ags_export_by_polygon/?polygon={polygon}'

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 422
    body = response.json()
    assert body['errors'][0]['desc'] == 'No boreholes found in the given polygon'


@pytest.mark.parametrize('polygon', [
    'NOTPOLYGON((0 0, 0 1, 1 1, 1 0, 0 0))',
    'POLYGON((0 0, 0 1, 1 1, 1 0))'
])
def test_get_ags_exporter_by_polygon_not_polygon(client, polygon):
    # Arrange
    query = f'{API_VERSION}/ags_export_by_polygon/?polygon={polygon}'

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 422
    body = response.json()
    assert body['errors'][0]['desc'] == 'Invalid polygon'


def test_get_ags_exporter_by_polygon_ogcapi_unreachable(client, monkeypatch):
    # Arrange
    polygon = 'POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))'
    query = f'{API_VERSION}/ags_export_by_polygon/?polygon={polygon}'
    # Patch the Borehole index to be something that cannot be reached
    monkeypatch.setattr(ags_export_by_polygon, "BOREHOLE_INDEX_URL", f'http://unreachable.com/{query}')

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 500
    body = response.json()
    assert body['errors'][0]['desc'] == 'The borehole index could not be reached.  Please try again later.'


def test_get_ags_exporter_by_polygon_ogcapi_error(client, monkeypatch):
    # Arrange
    polygon = 'POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))'
    query = f'{API_VERSION}/ags_export_by_polygon/?polygon={polygon}'

    # Patch the requests to return a response that behaves as though the URL had returned a 500 error.
    class MockResponse:
        status_code = 500

        def raise_for_status(self):
            raise requests.exceptions.HTTPError

        monkeypatch.setattr(ags_export_by_polygon.requests, 'get', lambda: MockResponse)

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(ags_export_by_polygon.requests, 'get', mock_get)

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 500
    body = response.json()
    assert body['errors'][0]['desc'] == 'The borehole index returned an error.'
