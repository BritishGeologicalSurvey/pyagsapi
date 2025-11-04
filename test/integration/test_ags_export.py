"""Tests for API responses."""
from io import BytesIO
import zipfile

import pytest
import requests

from app.checkers import load_ags4_as_numeric
from app.routes import ags_export

from test.fixtures import API_VERSION, IN_GITHUB_ACTIONS


@pytest.mark.xfail(IN_GITHUB_ACTIONS, reason="Upstream URL not available from Github Actions")
def test_get_ags_export_single_id(client, tmp_path):
    """
    Confirm that the endpoint can return the expected .zip.
    """
    # Arrange
    # Define the borehole and project IDs and zipped AGS file to use for the test
    bgs_loca_id = 20190430093402523419
    bgs_proj_id = str(bgs_loca_id)[:16]
    ags_file_name = f'{bgs_proj_id}.ags'
    ags_metadata_file_name = 'FILE/BGSFileSet01/BGS_download_metadata.txt'

    query = f'{API_VERSION}/ags_export/?bgs_loca_id={bgs_loca_id}'

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
        # Check that zip contains only the two correct files
        assert {ags_file_name, ags_metadata_file_name} == set(ags_zip.namelist())
        # Confirm the AGS file is correct
        with ags_zip.open(ags_file_name) as ags_file:
            unzipped_ags_file = tmp_path / 'test.ags'
            with open(unzipped_ags_file, 'wb') as f:
                f.write(ags_file.read())
            tables, _, _ = load_ags4_as_numeric(unzipped_ags_file)
            assert tables['PROJ']['BGS_PROJ_ID'][0] == bgs_proj_id
        # Confirm the metadata file is correct
        with ags_zip.open(ags_metadata_file_name) as metadata_file:
            metadata_text = metadata_file.read().decode()
            assert f'loca_ids={bgs_loca_id}' in metadata_text
            assert f'Project : {bgs_proj_id}' in metadata_text


@pytest.mark.parametrize('bgs_loca_ids', [
    ['20200205093728297908', '20200205093728297910'],  # One project
    ['20200205093727287903', '20200205093728297906'],  # Two projects
])
@pytest.mark.xfail(IN_GITHUB_ACTIONS, reason="Upstream URL not available from Github Actions")
def test_get_ags_export_multiple_ids(client, bgs_loca_ids):
    """
    Confirm that the endpoint can return the expected .zip.
    """
    # Arrange
    # Define the borehole and project IDs and zipped AGS file to use for the test
    bgs_proj_ids = {id_[:16] for id_ in bgs_loca_ids}  # unique ids when truncated to 16 digits
    ags_file_names = {f'{id_}.ags' for id_ in bgs_proj_ids}
    ags_metadata_file_name = 'FILE/BGSFileSet01/BGS_download_metadata.txt'

    query = f'{API_VERSION}/ags_export/?bgs_loca_id={";".join(bgs_loca_ids)}'

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
def test_get_ags_export_unknown_borehole(client):
    """
    Confirm that the endpoint can return the expected error when an unknown bgs_loca_id is submitted.
    """
    # Arrange
    # Define the borehole ID to use for the test
    bgs_loca_id = 0
    query = f'{API_VERSION}/ags_export/?bgs_loca_id={bgs_loca_id}'

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 404
    body = response.json()
    assert body['errors'][0]['desc'] == 'Failed to retrieve borehole 0. It may not exist or may be confidential'


def test_get_ags_export_too_many_borehole_ids(client):
    """
    Confirm that an error is returned when bgs_loca_id comprises more than 10 IDs.
    """
    # Arrange
    # Define the borehole IDs to use for the test
    bgs_loca_ids = ['20200205093728297908'] * (ags_export.BOREHOLE_EXPORT_LIMIT + 1)
    bgs_loca_ids = ';'.join(bgs_loca_ids)
    query = f'{API_VERSION}/ags_export/?bgs_loca_id={bgs_loca_ids}'

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 422
    body = response.json()
    assert body['errors'][0]['desc'] == f'More than {ags_export.BOREHOLE_EXPORT_LIMIT} borehole IDs.'


def test_get_ags_exporter_unreachable(client, monkeypatch):
    # Arrange
    bgs_loca_id = 0
    query = f'{API_VERSION}/ags_export/?bgs_loca_id={bgs_loca_id}'
    # Patch the Borehole export to be something that cannot be reached
    monkeypatch.setattr(ags_export, "BOREHOLE_EXPORT_URL", f'http://unreachable.com/{query}')

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 500
    body = response.json()
    assert body['errors'][0]['desc'] == 'The borehole exporter could not be reached.  Please try again later.'


def test_get_ags_exporter_error(client, monkeypatch):
    # Arrange
    bgs_loca_id = 0
    query = f'{API_VERSION}/ags_export/?bgs_loca_id={bgs_loca_id}'

    # Patch the requests to return a response that behaves as though the URL had returned a 500 error.
    class MockResponse:
        status_code = 500

        def raise_for_status(self):
            raise requests.exceptions.HTTPError

        monkeypatch.setattr(ags_export.requests, 'get', lambda: MockResponse)

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(ags_export.requests, 'get', mock_get)

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 500
    body = response.json()
    assert body['errors'][0]['desc'] == 'The borehole exporter returned an error.'
