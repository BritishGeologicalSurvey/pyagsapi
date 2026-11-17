"""
Unit tests for the client-side XSS escaping helpers.

The validation results page and the maps build HTML by concatenating values
that originate from uploaded AGS files / the OGC borehole API, so each dynamic
value must be HTML-escaped (and URLs sanitised) before insertion.  These tests
execute the *actual shipped* JavaScript helpers in a V8 context and assert that
hostile input is neutralised.

This test needs a JavaScript engine (py_mini_racer).  It is intentionally
self-contained in one module so the whole thing - test and its dev dependency -
can be dropped in a single commit if the extra overhead is not wanted.  If the
engine is not installed the test skips rather than failing.
"""
from pathlib import Path

import pytest

py_mini_racer = pytest.importorskip("py_mini_racer")

JS_DIR = Path(__file__).resolve().parents[2] / "app" / "static" / "js"

# Minimal browser/library globals so the files load in a bare V8 context.  The
# helpers under test do not use them; they are only referenced inside other
# functions that we never call.  A Proxy that no-ops any property access or call
# stands in for jQuery ($) and Leaflet (L) so top-level chained calls succeed
# without having to enumerate every method name.
_STUBS = """
var window = {};
var document = {};
var api_version_path = "/v7";
var _stub = new Proxy(function(){ return _stub; }, {
    get: function(){ return _stub; },
    apply: function(){ return _stub; }
});
var $ = _stub;
var L = _stub;
"""


def _context_for(filename):
    ctx = py_mini_racer.MiniRacer()
    ctx.eval(_STUBS)
    ctx.eval((JS_DIR / filename).read_text())
    return ctx


# (js file, namespace) for each escapeHtml helper that ships.
ESCAPE_NAMESPACES = [
    ("htmlView.js", "agsHtml"),
    ("validation-map.js", "vMap"),
    ("map.js", "agsMap"),
]


@pytest.mark.parametrize("filename, namespace", ESCAPE_NAMESPACES)
def test_escape_html_neutralises_markup(filename, namespace):
    ctx = _context_for(filename)
    payload = "<img src=x onerror=alert(1)>"
    result = ctx.call(f"{namespace}.escapeHtml", payload)
    assert "<" not in result and ">" not in result
    assert result == "&lt;img src=x onerror=alert(1)&gt;"


@pytest.mark.parametrize("filename, namespace", ESCAPE_NAMESPACES)
def test_escape_html_escapes_quotes_and_amp(filename, namespace):
    ctx = _context_for(filename)
    # & must be escaped first so existing entities are not double-decoded.
    assert ctx.call(f"{namespace}.escapeHtml", 'a & "b" \'c\'') == "a &amp; &quot;b&quot; &#39;c&#39;"


@pytest.mark.parametrize("filename, namespace", ESCAPE_NAMESPACES)
def test_escape_html_handles_null_and_undefined(filename, namespace):
    ctx = _context_for(filename)
    assert ctx.call(f"{namespace}.escapeHtml", None) == ""


def test_safe_url_blocks_dangerous_schemes():
    ctx = _context_for("map.js")
    assert ctx.call("agsMap.safeUrl", "javascript:alert(1)") == "#"
    assert ctx.call("agsMap.safeUrl", "data:text/html,<script>alert(1)</script>") == "#"
    assert ctx.call("agsMap.safeUrl", "  JavaScript:alert(1)") == "#"


def test_safe_url_allows_http_and_relative():
    ctx = _context_for("map.js")
    assert ctx.call("agsMap.safeUrl", "https://example.org/x") == "https://example.org/x"
    assert ctx.call("agsMap.safeUrl", "http://example.org/x") == "http://example.org/x"
    assert ctx.call("agsMap.safeUrl", "/relative/path") == "/relative/path"
