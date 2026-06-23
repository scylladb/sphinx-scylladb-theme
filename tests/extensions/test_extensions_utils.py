from types import SimpleNamespace

import pytest

from sphinx_scylladb_theme.extensions.utils import (
    base_url,
    build_redirect_body,
    generate_template,
    is_url,
    latest_version_slug,
    version_slug,
)


def test_generate_content():
    expected = "<div>Hello World!</div>"
    result = generate_template(
        """
            <div>{value_a} {value_b}!</div>
            """,
        value_a="Hello",
        value_b="World",
    )
    assert result.split() == expected.split()


def test_build_redirect_body():
    path = "/redirect"
    result = build_redirect_body(path)
    assert "url=/redirect" in result
    assert "zendesk" not in result


def test_build_redirect_body_with_zendesk_tag():
    path = "/redirect"
    zendesk_tag = "test-zendesk-tag"

    # Call the function with a Zendesk tag
    result = build_redirect_body(path, zendesk_tag)

    # Check if the Zendesk meta tag is in the result
    assert zendesk_tag in result
    assert "url=/redirect" in result


def test_is_url_external():
    path = "https://scylladb.com"
    assert is_url(path)


def test_is_url_relative_path():
    path = "/relative_path"
    assert not is_url(path)


# version_slug ---------------------------------------------------------------


def test_version_slug_empty_outside_multiversion(monkeypatch):
    monkeypatch.delenv("SPHINX_MULTIVERSION_OUTPUTDIR", raising=False)
    assert version_slug() == ""


@pytest.mark.parametrize(
    "outdir, expected",
    [
        ("/build/dirhtml/stable", "stable"),
        ("/build/dirhtml/branch-1.9/", "branch-1.9"),
        ("stable", "stable"),
    ],
)
def test_version_slug_returns_basename_of_outputdir(monkeypatch, outdir, expected):
    monkeypatch.setenv("SPHINX_MULTIVERSION_OUTPUTDIR", outdir)
    assert version_slug() == expected


# base_url -------------------------------------------------------------------


def test_base_url_empty_when_html_baseurl_unset(monkeypatch):
    monkeypatch.delenv("SPHINX_MULTIVERSION_OUTPUTDIR", raising=False)
    config = SimpleNamespace(html_baseurl="")
    assert base_url(config) == ""


def test_base_url_strips_trailing_slash(monkeypatch):
    monkeypatch.delenv("SPHINX_MULTIVERSION_OUTPUTDIR", raising=False)
    config = SimpleNamespace(html_baseurl="https://example.com/")
    assert base_url(config) == "https://example.com"


def test_base_url_appends_multiversion_slug(monkeypatch):
    monkeypatch.setenv("SPHINX_MULTIVERSION_OUTPUTDIR", "/build/dirhtml/stable")
    config = SimpleNamespace(html_baseurl="https://example.com")
    assert base_url(config) == "https://example.com/stable"


# latest_version_slug --------------------------------------------------------


def test_latest_version_slug_prefers_rename():
    config = SimpleNamespace(
        smv_rename_latest_version="stable",
        smv_latest_version="branch-1.9",
    )
    assert latest_version_slug(config) == "stable"


def test_latest_version_slug_falls_back_to_latest():
    config = SimpleNamespace(
        smv_rename_latest_version=None,
        smv_latest_version="branch-1.9",
    )
    assert latest_version_slug(config) == "branch-1.9"


def test_latest_version_slug_empty_when_neither_configured():
    config = SimpleNamespace(smv_rename_latest_version=None, smv_latest_version="")
    assert latest_version_slug(config) == ""
