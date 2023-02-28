"""Tests for API responses."""
from pathlib import Path
import shutil

from fastapi.testclient import TestClient
from freezegun import freeze_time
import pytest
from httpx import AsyncClient
from requests_toolbelt.multipart.encoder import MultipartEncoder
import pandas as pd
from python_ags4 import AGS4

from app.main import app
from test.fixtures import (BAD_FILE_DATA, DICTIONARIES, FROZEN_TIME,
                           GOOD_FILE_DATA)
from test.fixtures_json import JSON_RESPONSES
from test.fixtures_plain_text import PLAIN_TEXT_RESPONSES

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

    zip_file = tmp_path / 'results.zip'
    unzipped_files = tmp_path / 'results'
    with open(zip_file, 'wb') as f:
        f.write(response.content)
    shutil.unpack_archive(zip_file, unzipped_files, 'zip')
    assert (unzipped_files / 'conversion.log').is_file()
    with open(unzipped_files / 'conversion.log', 'rt') as f:
        log = f.read()
    for name, expected in GOOD_FILE_DATA:
        expected_message, expected_new_file_name = expected
        assert (unzipped_files / expected_new_file_name).is_file()
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

    zip_file = tmp_path / 'results.zip'
    unzipped_files = tmp_path / 'results'
    with open(zip_file, 'wb') as f:
        f.write(response.content)
    shutil.unpack_archive(zip_file, unzipped_files, 'zip')
    xl_file = unzipped_files / 'example_ags.xlsx'
    assert xl_file.is_file()
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

    zip_file = tmp_path / 'results.zip'
    unzipped_files = tmp_path / 'results'
    with open(zip_file, 'wb') as f:
        f.write(response.content)
    shutil.unpack_archive(zip_file, unzipped_files, 'zip')
    assert (unzipped_files / 'conversion.log').is_file()
    with open(unzipped_files / 'conversion.log', 'rt') as f:
        log = f.read()
    for name, expected in BAD_FILE_DATA:
        expected_message, expected_file_size = expected
        assert not (unzipped_files / name).is_file()
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


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


@pytest.fixture(scope="function")
def async_client():
    return AsyncClient(app=app, base_url="http://test")
