"""Tests for validate API responses."""
from pathlib import Path

from freezegun import freeze_time
import pytest

from requests_toolbelt.multipart.encoder import MultipartEncoder

from test.fixtures import API_VERSION, TEST_FILE_DIR, DICTIONARIES, FROZEN_TIME, ZIP_FILES_VALIDATE
from test.fixtures_json import JSON_RESPONSES, GEOJSON_RESPONSES, UNKNOWN_RULES_RESPONSE
from test.fixtures_plain_text import PLAIN_TEXT_RESPONSES


@pytest.mark.parametrize('filename, expected',
                         [item for item in JSON_RESPONSES.items()])
@pytest.mark.parametrize('return_geometry', [False, None])
@pytest.mark.asyncio
async def test_validate_json(async_client, filename, expected, return_geometry):
    # Arrange
    filename = TEST_FILE_DIR / filename
    file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
    fields = []
    fields.append(file)
    fields.append(('checkers', 'ags'))
    if return_geometry is not None:
        fields.append(('return_geometry', str(return_geometry)))
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            f'{API_VERSION}/validate/',
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
    assert body['data'][0]['geojson'] == expected['geojson']
    assert body['data'][0]['geojson_error'] == expected['geojson_error']


@pytest.mark.parametrize('filename, expected',
                         [item for item in GEOJSON_RESPONSES.items()])
@pytest.mark.asyncio
async def test_geojson_response(async_client, filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
    fields = []
    fields.append(file)
    fields.append(('checkers', 'ags'))
    fields.append(('return_geometry', str(True)))
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            f'{API_VERSION}/validate/',
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
    assert body['data'][0]['geojson'] == expected['geojson']
    assert body['data'][0]['geojson_error'] == expected['geojson_error']


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
            f'{API_VERSION}/validate/',
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
            f'{API_VERSION}/validate/',
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
            f'{API_VERSION}/validate/',
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
            f'{API_VERSION}/validate/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    # Just check that API responds and contains each file name
    assert response.status_code == 200
    assert 'text/plain' in response.headers['content-type']
    for filename in PLAIN_TEXT_RESPONSES.keys():
        assert Path(filename).name in response.text


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
            f'{API_VERSION}/validate/',
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
    projects = body['data'][0]['additional_metadata']['bgs_projects']
    assert projects == '1 projects found: 121415 (ACME Gas Works Redevelopment)'


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
            f'{API_VERSION}/validate/',
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
    projects = body['data'][0]['additional_metadata']['bgs_projects']
    assert projects == '1 projects found: 121415 (ACME Gas Works Redevelopment)'


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
            f'{API_VERSION}/validate/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    assert 'text/plain' in response.headers['content-type']


@pytest.mark.parametrize('dictionary, filename, expected', [
    ('v4_1_1', 'example_ags.ags', 'Standard_dictionary_v4_1_1.ags'),
    ('v4_1', 'example_ags.ags', 'Standard_dictionary_v4_1.ags'),
    ('v4_0_4', 'example_ags.ags', 'Standard_dictionary_v4_0_4.ags'),
    # Defaults to value set in the file
    (None, 'example_ags.ags', 'Standard_dictionary_v4_1.ags'),
    # Defaults to latest due to unknown dictionary in file (FYI)
    (None, 'example_fyis_ags.ags', 'Standard_dictionary_v4_1_1.ags'),
    # Defaults to latest dictionary due to no dictionary specified in file
    (None, 'nonsense.AGS', 'Standard_dictionary_v4_1_1.ags'),
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
            f'{API_VERSION}/validate/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    assert 'application/json' in response.headers['content-type']
    assert response.json()['data'][0]['dictionary'] == expected


@pytest.mark.parametrize('filename, zipped_files',
                         [item for item in ZIP_FILES_VALIDATE.items()])
@pytest.mark.asyncio
async def test_validate_single_zip(async_client, filename, zipped_files):
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
            f'{API_VERSION}/validate/',
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
    assert len(body['data']) == len(zipped_files)
    assert {d['filename'] for d in body['data']} == set(zipped_files)


@pytest.mark.asyncio
async def test_validate_multiple_zip(async_client):
    # Arrange
    fields = []
    for filename in ZIP_FILES_VALIDATE.keys():
        filename = TEST_FILE_DIR / filename
        file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
        fields.append(file)
    fields.append(('checkers', 'ags'))
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            f'{API_VERSION}/validate/',
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
    all_files = [file for filelist in ZIP_FILES_VALIDATE.values() for file in filelist]
    assert len(body['data']) == len(all_files)
    assert [d['filename'] for d in body['data']] == all_files


@pytest.mark.parametrize('filename, zipped_files',
                         [item for item in ZIP_FILES_VALIDATE.items()])
@pytest.mark.asyncio
async def test_validate_ags_and_zip(async_client, filename, zipped_files):
    # Arrange
    expected_files = set(zipped_files) | {'random_binary.ags'}
    fields = []
    # Upload ZIP file ...
    filename = TEST_FILE_DIR / filename
    file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
    fields.append(file)
    # ... with AGS file
    filename = TEST_FILE_DIR / 'random_binary.ags'
    file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
    fields.append(file)
    fields.append(('checkers', 'ags'))
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            f'{API_VERSION}/validate/',
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
    assert len(body['data']) == len(expected_files)
    assert {d['filename'] for d in body['data']} == expected_files


@pytest.mark.asyncio
async def test_validate_unknown_rules_json(async_client):
    # Arrange
    filename = TEST_FILE_DIR / 'example_ags.ags'
    file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
    fields = [file]
    fields.append(('checkers', 'ags'))
    fields.append(('checkers', 'unknown'))
    fields.append(('fmt', 'json'))
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            f'{API_VERSION}/validate/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 422
    body = response.json()
    assert body == UNKNOWN_RULES_RESPONSE
