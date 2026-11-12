"""
Regression tests for upstream parameter-injection hardening.

The ags_export, ags_log and ags_export_by_polygon endpoints forward user input
(borehole IDs, polygon WKT) to upstream BGS services.  Input is now validated
(numeric IDs; a genuine POLYGON) and forwarded via requests' params= so values
are URL-encoded and cannot inject extra query parameters.

These tests stub requests.get, so they make no real network calls.
"""
import pytest

import app.routes.ags_export as ags_export
import app.routes.ags_log as ags_log
import app.routes.ags_export_by_polygon as ags_export_by_polygon
from test.fixtures import API_VERSION


class _FakeResp:
    def __init__(self, json_data=None):
        self.status_code = 200
        self.content = b"data"
        self._json = json_data or {}

    def raise_for_status(self):
        pass

    def json(self):
        return self._json


def _forbid_network(monkeypatch, module):
    """Make any upstream call fail the test - validation must reject first."""
    def boom(*args, **kwargs):
        raise AssertionError("upstream request should not have been made")
    monkeypatch.setattr(module.requests, "get", boom)


def _capture_get(monkeypatch, module, json_data=None):
    """Capture the args passed to requests.get instead of making a call."""
    captured = {}

    def fake_get(url, params=None, timeout=None):
        captured["url"] = url
        captured["params"] = params
        return _FakeResp(json_data=json_data)

    monkeypatch.setattr(module.requests, "get", fake_get)
    return captured


BAD_IDS = ["abc", "1; DROP", "1 2", "1&loca_ids=2", "../etc", "", "1,2"]


@pytest.mark.parametrize("bad_id", BAD_IDS)
def test_ags_export_rejects_non_numeric_ids(client, monkeypatch, bad_id):
    _forbid_network(monkeypatch, ags_export)
    r = client.get(f"{API_VERSION}/ags_export/", params={"bgs_loca_id": bad_id})
    assert r.status_code == 422


@pytest.mark.parametrize("bad_id", BAD_IDS)
def test_ags_log_rejects_non_numeric_ids(client, monkeypatch, bad_id):
    _forbid_network(monkeypatch, ags_log)
    r = client.get(f"{API_VERSION}/ags_log/", params={"bgs_loca_id": bad_id})
    assert r.status_code == 422


def test_ags_export_forwards_ids_via_params(client, monkeypatch):
    captured = _capture_get(monkeypatch, ags_export)
    r = client.get(f"{API_VERSION}/ags_export/", params={"bgs_loca_id": "123;456"})
    assert r.status_code == 200
    # Base URL only (no interpolated query string) and value passed as a param.
    assert captured["url"] == ags_export.BOREHOLE_EXPORT_URL
    assert "?" not in captured["url"]
    assert captured["params"] == {"loca_ids": "123;456"}


def test_ags_log_forwards_id_via_params(client, monkeypatch):
    captured = _capture_get(monkeypatch, ags_log)
    # ags_log streams the upstream bytes as a PDF; a 200 is enough here.
    r = client.get(f"{API_VERSION}/ags_log/", params={"bgs_loca_id": "123"})
    assert r.status_code == 200
    assert captured["url"] == ags_log.BOREHOLE_VIEWER_URL
    assert captured["params"] == {"loca_id": "123"}


@pytest.mark.parametrize("bad_polygon", [
    "not wkt",
    "DROP TABLE",
    "POINT(0 0)",            # valid WKT but not a polygon
    "LINESTRING(0 0,1 1)",
])
def test_polygon_rejects_bad_or_non_polygon(client, monkeypatch, bad_polygon):
    _forbid_network(monkeypatch, ags_export_by_polygon)
    r = client.get(
        f"{API_VERSION}/ags_export_by_polygon/", params={"polygon": bad_polygon}
    )
    assert r.status_code == 422


def test_polygon_forwards_wkt_via_filter_param(client, monkeypatch):
    captured = _capture_get(
        monkeypatch, ags_export_by_polygon, json_data={"numberMatched": 3}
    )
    polygon = "POLYGON((0 0,1 0,1 1,0 1,0 0))"
    r = client.get(
        f"{API_VERSION}/ags_export_by_polygon/",
        params={"polygon": polygon, "count_only": "true"},
    )
    assert r.status_code == 200
    assert captured["url"] == ags_export_by_polygon.BOREHOLE_INDEX_URL
    assert "?" not in captured["url"]
    # WKT travels inside the CQL filter param (re-serialised by shapely),
    # URL-encoded by requests.
    import shapely
    expected_wkt = shapely.wkt.loads(polygon).wkt
    assert captured["params"]["filter"] == f"INTERSECTS(shape,{expected_wkt})"
    assert captured["params"]["limit"] == ags_export_by_polygon.BOREHOLE_EXPORT_LIMIT
