import json
import subprocess
from pathlib import Path
from textwrap import dedent
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from sphinx_scylladb_theme.extensions.diagram import (
    Diagram,
    _comma_list,
    _image_url,
    _page_url,
    _split,
    depart_diagram_html,
    diagram_node,
    visit_diagram_html,
)

mock_state_machine = Mock()
mock_state_machine.reporter = Mock()
mock_state = Mock()


def _build_directive(options):
    return Diagram(
        "diagram",
        [],
        options,
        ["placeholder"],
        0,
        0,
        "",
        mock_state_machine,
        mock_state,
    )


def test_directive_returns_single_diagram_node_with_metadata():
    directive = _build_directive(
        {
            "id": "auth-flow",
            "tags": "networking,security",
            "categories": "security",
            "deployment": "core",
            "last-reviewed": "2026-06-01",
        }
    )
    result = directive.run()
    assert len(result) == 1
    node = result[0]
    assert isinstance(node, diagram_node)
    assert node["diagram_id"] == "auth-flow"
    assert node["tags"] == "networking,security"
    assert node["categories"] == "security"
    assert node["deployment"] == "core"
    assert node["last-reviewed"] == "2026-06-01"


def test_directive_returns_node_with_empty_metadata_when_no_options():
    result = _build_directive({}).run()
    node = result[0]
    assert isinstance(node, diagram_node)
    assert node["diagram_id"] == ""
    assert all(
        node[k] == "" for k in ("tags", "categories", "deployment", "last-reviewed")
    )


@pytest.mark.parametrize(
    "options, expected_open",
    [
        (
            {
                "id": "auth-flow",
                "tags": "networking,security",
                "categories": "security",
                "deployment": "core",
                "last-reviewed": "2026-06-01",
            },
            '<div class="diagram" id="auth-flow"'
            ' data-tags="networking,security"'
            ' data-categories="security"'
            ' data-deployment="core"'
            ' data-last-reviewed="2026-06-01">',
        ),
        ({}, '<div class="diagram">'),
        ({"id": "diagram-1"}, '<div class="diagram" id="diagram-1">'),
        (
            {"id": 'a"b', "tags": "<x>"},
            '<div class="diagram" id="a&quot;b" data-tags="&lt;x&gt;">',
        ),
    ],
)
def test_html_visitor_emits_expected_wrapper(options, expected_open):
    node = _build_directive(options).run()[0]
    translator = Mock(body=[])
    visit_diagram_html(translator, node)
    depart_diagram_html(translator, node)
    assert translator.body == [expected_open, "</div>"]


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("networking, security", "networking,security"),
        ("  a , b ,c  ", "a,b,c"),
        ("a,,b", "a,b"),
        ("", ""),
        (None, ""),
    ],
)
def test_comma_list_normalizes_values(raw, expected):
    assert _comma_list(raw) == expected


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("a,b,c", ["a", "b", "c"]),
        ("", []),
        (None, []),
    ],
)
def test_split_returns_list(raw, expected):
    assert _split(raw) == expected


# _page_url ------------------------------------------------------------------


def _mock_app(builder_name="dirhtml", html_baseurl="https://example.com"):
    return SimpleNamespace(
        config=SimpleNamespace(html_baseurl=html_baseurl),
        builder=SimpleNamespace(name=builder_name),
        env=SimpleNamespace(images={}),
    )


@pytest.mark.parametrize(
    "builder, docname, anchor, expected",
    [
        # dirhtml
        ("dirhtml", "index", "", "https://example.com/"),
        ("dirhtml", "index", "foo", "https://example.com/#foo"),
        ("dirhtml", "examples/images", "", "https://example.com/examples/images/"),
        (
            "dirhtml",
            "examples/images",
            "auth-flow",
            "https://example.com/examples/images/#auth-flow",
        ),
        # docname that ends in /index becomes a directory URL
        (
            "dirhtml",
            "examples/index",
            "",
            "https://example.com/examples/",
        ),
        # html builder uses .html suffix
        ("html", "examples/images", "", "https://example.com/examples/images.html"),
        (
            "html",
            "examples/images",
            "auth-flow",
            "https://example.com/examples/images.html#auth-flow",
        ),
    ],
)
def test_page_url_combinations(builder, docname, anchor, expected, monkeypatch):
    monkeypatch.delenv("SPHINX_MULTIVERSION_OUTPUTDIR", raising=False)
    app = _mock_app(builder_name=builder)
    assert _page_url(app, docname, anchor=anchor) == expected


def test_page_url_includes_multiversion_slug(monkeypatch):
    monkeypatch.setenv("SPHINX_MULTIVERSION_OUTPUTDIR", "/build/dirhtml/stable")
    app = _mock_app(builder_name="dirhtml")
    assert (
        _page_url(app, "examples/images", anchor="auth-flow")
        == "https://example.com/stable/examples/images/#auth-flow"
    )


def test_page_url_without_baseurl(monkeypatch):
    monkeypatch.delenv("SPHINX_MULTIVERSION_OUTPUTDIR", raising=False)
    app = _mock_app(html_baseurl="")
    assert _page_url(app, "examples/images") == "examples/images/"


# _image_url -----------------------------------------------------------------


@pytest.mark.parametrize(
    "uri, expected",
    [
        ("https://cdn.example.com/foo.png", "https://cdn.example.com/foo.png"),
        ("http://cdn.example.com/foo.png", "http://cdn.example.com/foo.png"),
        (
            "data:image/svg+xml;base64,PHN2Zz48L3N2Zz4=",
            "data:image/svg+xml;base64,PHN2Zz48L3N2Zz4=",
        ),
    ],
)
def test_image_url_passes_through_absolute_uris(uri, expected, monkeypatch):
    monkeypatch.delenv("SPHINX_MULTIVERSION_OUTPUTDIR", raising=False)
    assert _image_url(_mock_app(), uri) == expected


def test_image_url_passes_through_already_prefixed(monkeypatch):
    monkeypatch.delenv("SPHINX_MULTIVERSION_OUTPUTDIR", raising=False)
    assert (
        _image_url(_mock_app(), "_images/diagram.svg")
        == "https://example.com/_images/diagram.svg"
    )


def test_image_url_uses_env_images_mapping(monkeypatch):
    monkeypatch.delenv("SPHINX_MULTIVERSION_OUTPUTDIR", raising=False)
    app = _mock_app()
    app.env.images = {"images/diagram.svg": ({"index"}, "diagram1.svg")}
    assert (
        _image_url(app, "images/diagram.svg")
        == "https://example.com/_images/diagram1.svg"
    )


def test_image_url_falls_back_to_basename(monkeypatch):
    monkeypatch.delenv("SPHINX_MULTIVERSION_OUTPUTDIR", raising=False)
    app = _mock_app()
    app.env.images = {}
    assert (
        _image_url(app, "deep/nested/checkmark.png")
        == "https://example.com/_images/checkmark.png"
    )


def test_image_url_returns_none_for_empty_uri():
    assert _image_url(_mock_app(), "") is None


def test_image_url_without_baseurl_returns_root_relative(monkeypatch):
    monkeypatch.delenv("SPHINX_MULTIVERSION_OUTPUTDIR", raising=False)
    app = _mock_app(html_baseurl="")
    assert _image_url(app, "images/foo.png") == "/_images/foo.png"


# End-to-end integration: build a tiny Sphinx project and inspect diagrams.json
# to verify both image and mermaid entries are emitted with absolute URLs.


def _write_min_project(root: Path):
    (root / "conf.py").write_text(
        dedent(
            """
            extensions = ["sphinx_scylladb_theme"]
            html_theme = "sphinx_scylladb_theme"
            master_doc = "index"
            html_baseurl = "https://example.com"
            project = "diagrams-test"
            html_theme_options = {"site_description": "test"}
            html_context = {"html_baseurl": html_baseurl}
            """
        )
    )
    (root / "img.png").write_bytes(b"")
    (root / "index.rst").write_text(
        dedent(
            """
            Diagram E2E
            ===========

            .. diagram::
               :id: img-diagram
               :tags: networking, security
               :categories: security
               :deployment: core
               :last-reviewed: 2026-06-01

               .. figure:: img.png
                  :alt: An image

                  An image.

            .. diagram::
               :id: mermaid-diagram
               :tags: arch

               .. mermaid::

                  graph TD
                  A --> B

            .. diagram::

               .. mermaid::

                  graph TD
                  X --> Y
            """
        )
    )


def test_diagrams_json_includes_image_and_mermaid_entries(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    out = tmp_path / "out"
    _write_min_project(src)

    result = subprocess.run(
        ["uv", "run", "sphinx-build", "-q", "-b", "dirhtml", str(src), str(out)],
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parents[2],
    )
    assert result.returncode == 0, result.stderr

    data = json.loads((out / "diagrams.json").read_text())
    assert "diagrams" in data
    entries_by_id = {e["id"]: e for e in data["diagrams"] if e["id"] is not None}
    assert set(entries_by_id) == {"img-diagram", "mermaid-diagram"}

    # Diagram without :id: still appears (no anchor in page_url, null id).
    anonymous = [e for e in data["diagrams"] if e["id"] is None]
    assert len(anonymous) == 1
    assert anonymous[0]["type"] == "mermaid"
    assert "X --> Y" in anonymous[0]["content"]
    assert anonymous[0]["page_url"] == "https://example.com/"
    assert anonymous[0]["last_reviewed"] is None
    assert anonymous[0]["deployment"] is None

    entries = entries_by_id

    img = entries["img-diagram"]
    assert img["type"] == "image"
    assert img["content"].startswith("https://example.com/_images/")
    assert img["content"].endswith(".png")
    assert img["page"] == "index"
    assert img["page_url"] == "https://example.com/#img-diagram"
    assert img["tags"] == ["networking", "security"]
    assert img["categories"] == ["security"]
    assert img["deployment"] == "core"
    assert img["last_reviewed"] == "2026-06-01"

    mmd = entries["mermaid-diagram"]
    assert mmd["type"] == "mermaid"
    assert "graph TD" in mmd["content"]
    assert "A --> B" in mmd["content"]
    assert mmd["page_url"] == "https://example.com/#mermaid-diagram"
    assert mmd["tags"] == ["arch"]
    assert mmd["categories"] == []
    assert mmd["deployment"] is None
