"""Test for openapi responses."""

from test.fixtures import API_VERSION


def test_openapi_json(client):
    """ Check that the openapi is accessible and it display the correct endpoints """
    response = client.get('/openapi.json')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    # exposed endpoints
    assert f'{API_VERSION}/validate' in response.text
    assert f'{API_VERSION}/convert' in response.text
    assert f'{API_VERSION}/ags_log' in response.text
    assert f'{API_VERSION}/ags_export' in response.text
    assert f'{API_VERSION}/ags_export_by_polygon' in response.text
