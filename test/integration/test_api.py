"""Tests for API responses."""
from io import BytesIO
import os
from pathlib import Path
import zipfile

from fastapi.testclient import TestClient
from freezegun import freeze_time
import pytest
from httpx import AsyncClient
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import pandas as pd
from python_ags4 import AGS4

from app.main import app
from app.checkers import load_AGS4_as_numeric
import app.routes as app_routes
from test.fixtures import (BAD_FILE_DATA, DICTIONARIES, FROZEN_TIME,
                           GOOD_FILE_DATA)
from test.fixtures_json import JSON_RESPONSES
from test.fixtures_plain_text import PLAIN_TEXT_RESPONSES

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"
TEST_FILE_DIR = Path(__file__).parent.parent / 'files'


def test_openapi_json(client):
    """A hello-world type test to confirm testing framework works."""
    response = client.get('/openapi.json')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    assert '/validate' in response.text


@pytest.mark.parametrize('filename, expected',
                         [item for item in JSON_RESPONSES.items()])
@pytest.mark.asyncio
async def test_validate_json(async_client, filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
    fields = []
    fields.append(file)
    fields.append(('checkers', 'ags'))
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            '/validate/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    body = response.json()
    assert set(body.keys()) == {'msg', 'type', 'self', 'data'}
    assert body['msg'] is not None
    assert body['type'] == 'success'
    assert body['self'] is not None
    assert len(body['data']) == 1
    assert set(body['data'][0]) == set(expected.keys())
    assert body['data'][0]['filename'] == expected['filename']


@pytest.mark.asyncio
async def test_validate_many_json(async_client):
    # Arrange
    fields = []
    for name in JSON_RESPONSES.keys():
        filename = TEST_FILE_DIR / name
        file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
        fields.append(file)
    fields.append(('checkers', 'ags'))
    fields.append(('std_dictionary', 'v4_1'))
    fields.append(('fmt', 'json'))
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            '/validate/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    body = response.json()
    assert set(body.keys()) == {'msg', 'type', 'self', 'data'}
    assert body['msg'] is not None
    assert body['type'] == 'success'
    assert body['self'] is not None
    assert len(body['data']) == len(JSON_RESPONSES)


@pytest.mark.parametrize('dictionary, expected',
                         [item for item in DICTIONARIES.items()])
@pytest.mark.asyncio
async def test_validate_custom_dictionary(async_client, dictionary, expected):
    # Arrange
    filename = TEST_FILE_DIR / 'example_ags.ags'
    file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
    fields = []
    fields.append(file)
    fields.append(('checkers', 'ags'))
    fields.append(('std_dictionary', dictionary))
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            '/validate/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    body = response.json()
    assert len(body['data']) == 1
    # Assert
    assert body['data'][0]['filename'] == 'example_ags.ags'
    assert body['data'][0]['dictionary'] == expected


@freeze_time(FROZEN_TIME)
@pytest.mark.parametrize('filename, expected',
                         [item for item in PLAIN_TEXT_RESPONSES.items()])
@pytest.mark.asyncio
async def test_validate_text(async_client, filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
    fields = []
    fields.append(file)
    fields.append(('checkers', 'ags'))
    fields.append(('std_dictionary', 'v4_1_1'))
    fields.append(('fmt', 'text'))
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            '/validate/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    assert 'text/plain' in response.headers['content-type']
    assert filename.name in expected.strip()


@freeze_time(FROZEN_TIME)
@pytest.mark.asyncio
async def test_validate_many_text(async_client):
    # Arrange
    fields = []
    for name in PLAIN_TEXT_RESPONSES.keys():
        filename = TEST_FILE_DIR / name
        file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
        fields.append(file)
    fields.append(('checkers', 'ags'))
    fields.append(('std_dictionary', 'v4_1_1'))
    fields.append(('fmt', 'text'))
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            '/validate/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    # Just check that API responds and contains each file name
    assert response.status_code == 200
    assert 'text/plain' in response.headers['content-type']
    for filename in PLAIN_TEXT_RESPONSES.keys():
        assert Path(filename).name in response.text


@pytest.mark.asyncio
async def test_convert_good_files(async_client, tmp_path):
    # Arrange
    fields = []
    for name, expected in GOOD_FILE_DATA:
        filename = TEST_FILE_DIR / name
        file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
        fields.append(file)
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            '/convert/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/x-zip-compressed'
    assert response.headers['content-disposition'] == 'attachment; filename=results.zip'

    assert zipfile.is_zipfile(BytesIO(response.content))
    with zipfile.ZipFile(BytesIO(response.content)) as ags_zip:
        assert 'conversion.log' in ags_zip.namelist()
        with ags_zip.open('conversion.log') as log_file:
            log = log_file.read().decode()
        ags_path = zipfile.Path(ags_zip)
        for name, expected in GOOD_FILE_DATA:
            expected_message, expected_new_file_name = expected
            assert expected_new_file_name in ags_zip.namelist()
            assert (ags_path / expected_new_file_name).is_file()
            assert expected_message in log


@pytest.mark.asyncio
@pytest.mark.parametrize('sort_tables', [True, False, None])
async def test_convert_sort_tables(async_client, tmp_path, sort_tables):
    # Arrange
    fields = []
    filename = TEST_FILE_DIR / 'example_ags.ags'
    tables, headings = AGS4.AGS4_to_dataframe(filename)
    groups = list(tables.keys())

    file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
    fields.append(file)
    if sort_tables is not None:
        fields.append(('sort_tables', str(sort_tables)))
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            '/convert/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/x-zip-compressed'
    assert response.headers['content-disposition'] == 'attachment; filename=results.zip'

    assert zipfile.is_zipfile(BytesIO(response.content))
    with zipfile.ZipFile(BytesIO(response.content)) as ags_zip:
        assert 'example_ags.xlsx' in ags_zip.namelist()
        assert (zipfile.Path(ags_zip) / 'example_ags.xlsx').is_file()
        with ags_zip.open('example_ags.xlsx') as xl_file:
            xl = pd.ExcelFile(xl_file)
        if sort_tables:
            assert xl.sheet_names == sorted(groups)
        else:
            assert xl.sheet_names == groups


@pytest.mark.asyncio
async def test_convert_bad_files(async_client, tmp_path):
    # Arrange
    fields = []
    for name, expected in BAD_FILE_DATA:
        filename = TEST_FILE_DIR / name
        file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
        fields.append(file)
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            '/convert/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/x-zip-compressed'
    assert response.headers['content-disposition'] == 'attachment; filename=results.zip'

    assert zipfile.is_zipfile(BytesIO(response.content))
    with zipfile.ZipFile(BytesIO(response.content)) as ags_zip:
        assert 'conversion.log' in ags_zip.namelist()
        with ags_zip.open('conversion.log') as log_file:
            log = log_file.read().decode()
        ags_path = zipfile.Path(ags_zip)
        for name, expected in BAD_FILE_DATA:
            expected_message, expected_file_size = expected
            assert not (ags_path / name).is_file()
            assert expected_message in log


@pytest.mark.asyncio
async def test_validate_bgs_json(async_client):
    # Arrange
    filename = TEST_FILE_DIR / 'example_ags.ags'
    file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
    fields = [file]
    fields.append(('checkers', 'bgs'))
    fields.append(('fmt', 'json'))
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            '/validate/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    body = response.json()
    assert set(body.keys()) == {'msg', 'type', 'self', 'data'}
    assert body['msg'] is not None
    assert body['type'] == 'success'
    assert body['self'] is not None
    assert len(body['data']) == 1
    assert len(body['data'][0]['checkers']) == 1


@pytest.mark.asyncio
async def test_validate_ags_bgs_json(async_client):
    # Arrange
    filename = TEST_FILE_DIR / 'example_ags.ags'
    file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
    fields = [file]
    fields.append(('checkers', 'ags'))
    fields.append(('checkers', 'bgs'))
    fields.append(('fmt', 'json'))
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            '/validate/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    body = response.json()
    assert set(body.keys()) == {'msg', 'type', 'self', 'data'}
    assert body['msg'] is not None
    assert body['type'] == 'success'
    assert body['self'] is not None
    assert len(body['data']) == 1
    assert len(body['data'][0]['checkers']) == 2


@pytest.mark.asyncio
async def test_validate_bgs_text(async_client):
    # Arrange
    filename = TEST_FILE_DIR / 'example_ags.ags'
    file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
    fields = [file]
    fields.append(('checkers', 'bgs'))
    fields.append(('fmt', 'text'))
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            '/validate/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    assert 'text/plain' in response.headers['content-type']


@pytest.mark.parametrize('dictionary, filename, expected', [
    ('v4_1_1', 'example_ags.ags', 'Standard_dictionary_v4_1_1.ags'),
    ('v4_1', 'example_ags.ags', 'Standard_dictionary_v4_1.ags'),
    ('v4_0_4', 'example_ags.ags', 'Standard_dictionary_v4_0_4.ags'),
    (None, 'example_ags.ags', 'Standard_dictionary_v4_1.ags'),  # Defaults to value set in the file
    (None, 'nonsense.AGS', 'Standard_dictionary_v4_1_1.ags'),  # Defaults to latest dictionary
])
@pytest.mark.asyncio
async def test_validate_dictionary_choice(async_client, dictionary, filename, expected):
    """
    Confirm that the specified dictionary is used, or if not, either the one in the file
    where specified, or the latest.
    """
    # Arrange
    filename = TEST_FILE_DIR / filename
    file_ = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))

    fields = []
    fields.append(file_)
    fields.append(('checkers', 'ags'))
    fields.append(('std_dictionary', dictionary))
    fields.append(('fmt', 'json'))
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            '/validate/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    assert 'application/json' in response.headers['content-type']
    assert response.json()['data'][0]['dictionary'] == expected


@pytest.mark.parametrize('response_type, response_type_result', [
    ('inline', 'inline'),
    ('attachment', 'attachment'),
    (None, 'inline')  # Defaults to 'inline'
])
@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Upstream URL not avilable from Github Actions")
def test_get_ags_log(client, response_type, response_type_result):
    """
    Confirm that the endpoint can return the expected .pdf.
    """
    # Arrange
    # Define the borehole ID to use for the test
    bgs_loca_id = 20190430093402523419
    query = f'/ags_log/?bgs_loca_id={bgs_loca_id}'

    if response_type:
        query += f'&response_type={response_type}'

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 200
    content_disposition = f'{response_type_result}; filename="{bgs_loca_id}_log.pdf"'
    assert response.headers["Content-Disposition"] == content_disposition
    assert response.headers["Content-Type"] == "application/pdf"
    assert len(response.content) > 0
    assert response.content.startswith(b'%PDF')


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Upstream URL not avilable from Github Actions")
def test_get_ags_log_unknown_borehole(client):
    """
    Confirm that the endpoint can return the expected error when an unknown bgs_loca_id is submitted.
    """
    # Arrange
    # Define the borehole ID to use for the test
    bgs_loca_id = 0
    query = f'/ags_log/?bgs_loca_id={bgs_loca_id}'

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 404
    body = response.json()
    assert body['errors'][0]['desc'] == 'Failed to retrieve borehole 0. It may not exist or may be confidential'


def test_get_ags_log_generator_unreachable(client, monkeypatch):
    # Arrange
    bgs_loca_id = 0
    query = f'/ags_log/?bgs_loca_id={bgs_loca_id}'
    # Patch the Borehole Viewer to be something that cannot be reached
    monkeypatch.setattr(app_routes, "BOREHOLE_VIEWER_URL", f'http://unreachable.com/{bgs_loca_id}')

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 500
    body = response.json()
    assert body['errors'][0]['desc'] == 'The borehole generator could not be reached.  Please try again later.'


def test_get_ags_log_generator_error(client, monkeypatch):
    # Arrange
    bgs_loca_id = 0
    query = f'/ags_log/?bgs_loca_id={bgs_loca_id}'

    # Patch the requests to return a response that behaves as though the URL had returned a 500 error.
    class MockResponse:
        status_code = 500

        def raise_for_status(self):
            raise requests.exceptions.HTTPError

        monkeypatch.setattr(app_routes.requests, 'get', lambda: MockResponse)

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(app_routes.requests, 'get', mock_get)

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 500
    body = response.json()
    assert body['errors'][0]['desc'] == 'The borehole generator returned an error.'


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Upstream URL not avilable from Github Actions")
def test_get_ags_export(client, tmp_path):
    """
    Confirm that the endpoint can return the expected .zip.
    """
    # Arrange
    # Define the borehole and project IDs and zipped AGS file to use for the test
    bgs_loca_id = 20190430093402523419
    bgs_proj_id = str(bgs_loca_id)[:16]
    ags_file_name = f'{bgs_proj_id}.ags'

    query = f'/ags_export/?bgs_loca_id={bgs_loca_id}'

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == f'attachment; filename="{bgs_loca_id}.zip"'
    assert response.headers["Content-Type"] == "application/x-zip-compressed"
    assert len(response.content) > 0

    assert zipfile.is_zipfile(BytesIO(response.content))
    with zipfile.ZipFile(BytesIO(response.content)) as ags_zip:
        assert ags_file_name in ags_zip.namelist()
        with ags_zip.open(ags_file_name) as ags_file:
            unzipped_file = tmp_path / 'test.ags'
            with open(unzipped_file, 'wb') as f:
                f.write(ags_file.read())
            tables, _, _ = load_AGS4_as_numeric(unzipped_file)
            assert tables['PROJ']['BGS_PROJ_ID'][0] == bgs_proj_id


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Upstream URL not avilable from Github Actions")
def test_get_ags_export_unknown_borehole(client):
    """
    Confirm that the endpoint can return the expected error when an unknown bgs_loca_id is submitted.
    """
    # Arrange
    # Define the borehole ID to use for the test
    bgs_loca_id = 0
    query = f'/ags_export/?bgs_loca_id={bgs_loca_id}'

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 404
    body = response.json()
    assert body['errors'][0]['desc'] == 'Failed to retrieve borehole 0. It may not exist or may be confidential'


def test_get_ags_exporter_unreachable(client, monkeypatch):
    # Arrange
    bgs_loca_id = 0
    query = f'/ags_export/?bgs_loca_id={bgs_loca_id}'
    # Patch the Borehole export to be something that cannot be reached
    monkeypatch.setattr(app_routes, "BOREHOLE_EXPORT_URL", f'http://unreachable.com/{bgs_loca_id}')

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
    query = f'/ags_export/?bgs_loca_id={bgs_loca_id}'

    # Patch the requests to return a response that behaves as though the URL had returned a 500 error.
    class MockResponse:
        status_code = 500

        def raise_for_status(self):
            raise requests.exceptions.HTTPError

        monkeypatch.setattr(app_routes.requests, 'get', lambda: MockResponse)

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(app_routes.requests, 'get', mock_get)

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 500
    body = response.json()
    assert body['errors'][0]['desc'] == 'The borehole exporter returned an error.'


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


@pytest.fixture(scope="function")
def async_client():
    return AsyncClient(app=app, base_url="http://test")
