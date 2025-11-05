"""Tests for ags_log API responses."""
import pytest
import requests

from app.routes import ags_log

from test.fixtures import API_VERSION, IN_GITHUB_ACTIONS


@pytest.mark.parametrize('response_type, response_type_result', [
    ('inline', 'inline'),
    ('attachment', 'attachment'),
    (None, 'inline')  # Defaults to 'inline'
])
@pytest.mark.xfail(IN_GITHUB_ACTIONS, reason="Upstream URL not available from Github Actions")
def test_get_ags_log(client, response_type, response_type_result):
    """
    Confirm that the endpoint can return the expected .pdf.
    """
    # Arrange
    # Define the borehole ID to use for the test
    bgs_loca_id = 20190430093402523419
    query = f'{API_VERSION}/ags_log/?bgs_loca_id={bgs_loca_id}'

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


@pytest.mark.xfail(IN_GITHUB_ACTIONS, reason="Upstream URL not available from Github Actions")
def test_get_ags_log_unknown_borehole(client):
    """
    Confirm that the endpoint can return the expected error when an unknown bgs_loca_id is submitted.
    """
    # Arrange
    # Define the borehole ID to use for the test
    bgs_loca_id = 0
    query = f'{API_VERSION}/ags_log/?bgs_loca_id={bgs_loca_id}'

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
    query = f'{API_VERSION}/ags_log/?bgs_loca_id={bgs_loca_id}'
    # Patch the Borehole Viewer to be something that cannot be reached
    monkeypatch.setattr(ags_log, "BOREHOLE_VIEWER_URL", f'http://unreachable.com/{query}')

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
    query = f'{API_VERSION}/ags_log/?bgs_loca_id={bgs_loca_id}'

    # Patch the requests to return a response that behaves as though the URL had returned a 500 error.
    class MockResponse:
        status_code = 500

        def raise_for_status(self):
            raise requests.exceptions.HTTPError

        monkeypatch.setattr(ags_log.requests, 'get', lambda: MockResponse)

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(ags_log.requests, 'get', mock_get)

    # Act
    with client as ac:
        response = ac.get(query)

    # Assert
    assert response.status_code == 500
    body = response.json()
    assert body['errors'][0]['desc'] == 'The borehole generator returned an error.'
