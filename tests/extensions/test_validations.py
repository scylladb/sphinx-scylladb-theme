import subprocess
from pathlib import Path
from textwrap import dedent
from unittest.mock import MagicMock

import pytest
from docutils import nodes

from sphinx_scylladb_theme.extensions.validations import (
    warn_on_internal_docs_as_external_links,
    warn_on_underscores,
)


def test_warn_on_underscores():
    app_mock = MagicMock()
    html_theme_options = {}
    app_mock.config.html_theme_options = html_theme_options

    assert warn_on_underscores(app_mock, "file_name.rst", None)


def test_skip_warn_on_underscores():
    app_mock = MagicMock()
    html_theme_options = {"skip_warnings": "document_has_underscores"}
    app_mock.config.html_theme_options = html_theme_options

    assert warn_on_underscores(app_mock, "file_name.rst", None) is False


# warn_on_internal_docs_as_external_links -----------------------------------


def _make_app(skip_warnings=None):
    app = MagicMock()
    app.config.html_theme_options = {"skip_warnings": skip_warnings or []}
    return app


def _make_doctree(references):
    refs = [nodes.reference(**kw) for kw in references]
    tree = MagicMock()
    tree.traverse = lambda cls: [r for r in refs if isinstance(r, cls)]
    return tree


@pytest.mark.parametrize(
    "refuri",
    [
        "disable-housekeeping",
        "bar.html",
        "../other/",
        "www.example.com",
        "/stable/thing/",
    ],
)
def test_warns_when_external_syntax_lacks_url_scheme(refuri, caplog):
    app = _make_app()
    doctree = _make_doctree([{"refuri": refuri, "internal": False}])
    with caplog.at_level("WARNING"):
        assert (
            warn_on_internal_docs_as_external_links(app, doctree, "current-doc") is True
        )
    joined = "\n".join(caplog.messages)
    assert refuri in joined
    assert ":doc:" in joined


@pytest.mark.parametrize(
    "refuri",
    [
        "https://example.com",
        "http://example.com/path",
        "ftp://example.com",
        "mailto:foo@example.com",
        "javascript:void(0)",
        "file:///path",
        "#some-section",
    ],
)
def test_silent_when_refuri_has_scheme_or_is_anchor(refuri, caplog):
    app = _make_app()
    doctree = _make_doctree([{"refuri": refuri, "internal": False}])
    with caplog.at_level("WARNING"):
        assert (
            warn_on_internal_docs_as_external_links(app, doctree, "current-doc")
            is False
        )
    assert caplog.messages == []


def test_silent_for_resolved_doc_reference(caplog):
    app = _make_app()
    doctree = _make_doctree([{"refuri": "disable-housekeeping", "internal": True}])
    with caplog.at_level("WARNING"):
        assert (
            warn_on_internal_docs_as_external_links(app, doctree, "current-doc")
            is False
        )
    assert caplog.messages == []


def test_silent_when_skip_flag_set(caplog):
    app = _make_app(skip_warnings=["internal_docs_as_external_link"])
    doctree = _make_doctree([{"refuri": "disable-housekeeping", "internal": False}])
    with caplog.at_level("WARNING"):
        assert (
            warn_on_internal_docs_as_external_links(app, doctree, "current-doc")
            is False
        )
    assert caplog.messages == []


def test_silent_for_empty_refuri(caplog):
    app = _make_app()
    doctree = _make_doctree([{"refuri": "", "internal": False}])
    with caplog.at_level("WARNING"):
        assert (
            warn_on_internal_docs_as_external_links(app, doctree, "current-doc")
            is False
        )
    assert caplog.messages == []


# End-to-end: parse the two real RST syntaxes from issue #532 and verify only
# the external-syntax form triggers the warning.


def _write_min_project(root: Path):
    (root / "conf.py").write_text(
        dedent(
            """
            extensions = ["sphinx_scylladb_theme"]
            html_theme = "sphinx_scylladb_theme"
            master_doc = "index"
            html_baseurl = "https://example.com"
            project = "validations-test"
            html_theme_options = {"site_description": "test"}
            html_context = {"html_baseurl": html_baseurl}
            """
        )
    )
    (root / "disable-housekeeping.rst").write_text(
        "Disable housekeeping\n====================\n\nBody.\n"
    )
    (root / "index.rst").write_text(
        dedent(
            """
            Validations E2E
            ===============

            * :doc:`Scylla Housekeeping and how to disable it <disable-housekeeping>`
            * `Scylla Housekeeping and how to disable it <disable-housekeeping>`_
            """
        )
    )


def test_end_to_end_only_external_syntax_triggers_warning(tmp_path):
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
    combined = result.stdout + result.stderr

    warnings = [
        line
        for line in combined.splitlines()
        if "has no URL scheme" in line and "disable-housekeeping" in line
    ]
    assert len(warnings) == 1, f"expected 1 warning, got {len(warnings)}:\n{combined}"
    assert ":doc:" in warnings[0]
