"""Tests for convert API responses."""
from io import BytesIO
import zipfile

import pytest
from requests_toolbelt.multipart.encoder import MultipartEncoder
import pandas as pd
from python_ags4 import AGS4

from test.fixtures import (API_VERSION, TEST_FILE_DIR, BAD_FILE_DATA,
                           GOOD_FILE_DATA, ZIP_FILES_CONVERT)


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
            f'{API_VERSION}/convert/',
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
@pytest.mark.parametrize('sort_tables', ['alphabetical', 'default'])
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
            f'{API_VERSION}/convert/',
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
        if sort_tables == 'alphabetical':
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
            f'{API_VERSION}/convert/',
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
@pytest.mark.parametrize('filename, expected_files',
                         [item for item in ZIP_FILES_CONVERT.items()])
async def test_convert_zip_file(async_client, tmp_path, filename, expected_files):
    # Arrange
    fields = []
    filename = TEST_FILE_DIR / filename
    file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
    fields.append(file)
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            f'{API_VERSION}/convert/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/x-zip-compressed'
    assert response.headers['content-disposition'] == 'attachment; filename=results.zip'

    assert zipfile.is_zipfile(BytesIO(response.content))
    with zipfile.ZipFile(BytesIO(response.content)) as ags_zip:
        for file in expected_files:
            assert file in ags_zip.namelist()
            assert (zipfile.Path(ags_zip) / file).is_file()


@pytest.mark.asyncio
async def test_convert_mixed_files(async_client, tmp_path):
    # Arrange
    filenames = ['one_good_xlsx.zip', 'one_good_two_bad_ags.zip', 'example_2_xlsx.xlsx', 'example_ags.ags']
    expected_files = (ZIP_FILES_CONVERT['one_good_xlsx.zip'] + ZIP_FILES_CONVERT['one_good_xlsx.zip']
                      + ['example_2_xlsx.ags', 'example_ags.xlsx'])
    fields = []
    for name in filenames:
        filename = TEST_FILE_DIR / name
        file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
        fields.append(file)
    mp_encoder = MultipartEncoder(fields=fields)

    # Act
    async with async_client as ac:
        response = await ac.post(
            f'{API_VERSION}/convert/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/x-zip-compressed'
    assert response.headers['content-disposition'] == 'attachment; filename=results.zip'

    assert zipfile.is_zipfile(BytesIO(response.content))
    with zipfile.ZipFile(BytesIO(response.content)) as ags_zip:
        for file in expected_files:
            assert file in ags_zip.namelist()
            assert (zipfile.Path(ags_zip) / file).is_file()
