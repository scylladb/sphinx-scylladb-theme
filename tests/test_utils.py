import requests
from sphinx_scylladb_theme.utils import multiversion_regex_builder, fetch_multiversion_configuration
from sphinx_scylladb_theme.extensions.utils import resolve_link
from unittest.mock import patch, MagicMock


def test_multiversion_regex_builder_empty():
    versions = []
    assert multiversion_regex_builder(versions) == "None"


def test_multiversion_regex_builder_all():
    versions = ["*"]
    assert multiversion_regex_builder(versions) == "^.*"


def test_multiversion_regex_builder_one_version():
    versions = ["1.0"]
    assert multiversion_regex_builder(versions) == r"^1.0$"


def test_multiversion_regex_builder_many_version():
    versions = ["1.0", "2.0"]
    assert multiversion_regex_builder(versions) == r"\b(^1.0$|^2.0$)\b"

def test_fetch_multiversion_configuration_success():
    url = "https://example.com/success"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "tags": [],
        "branches": ["master", "branch-5.1", "branch-5.2"],
        "latest": "branch-5.2",
    }
    with patch("requests.get", return_value=mock_response):
        result = fetch_multiversion_configuration(url)
        assert result == {
            "tags": [],
            "branches": ["master", "branch-5.1", "branch-5.2"],
            "latest": "branch-5.2",
        }


def test_fetch_multiversion_configuration_http_error():
    url = "https://example.com/http_error"

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("HTTP Error")
    with patch("requests.get", return_value=mock_response):
        result = fetch_multiversion_configuration(url)
        assert result is None


def test_fetch_multiversion_configuration_invalid_json():
    url = "https://example.com/invalid_json"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Invalid JSON")
    with patch("requests.get", return_value=mock_response):
        result = fetch_multiversion_configuration(url)
        assert result is None


def test_fetch_multiversion_configuration_invalid_url():
    result = fetch_multiversion_configuration(None)
    assert result is None

    result = fetch_multiversion_configuration("")
    assert result is None


def test_resolve_link_external_url():
    """Test that external URLs are returned unchanged."""
    env = MagicMock()
    result = resolve_link("https://example.com", env)
    assert result == "https://example.com"


def test_resolve_link_empty():
    """Test that empty links are returned unchanged."""
    env = MagicMock()
    result = resolve_link("", env)
    assert result == ""
    
    result = resolve_link(None, env)
    assert result is None


def test_resolve_link_absolute_path():
    """Test absolute path resolution."""
    env = MagicMock()
    env.docname = "examples/topic-box"
    env.found_docs = {"getting-started/installation"}
    env.app.builder.get_relative_uri.return_value = "getting-started/installation.html"
    
    result = resolve_link("/getting-started/installation", env)
    assert result == "getting-started/installation.html"
    env.app.builder.get_relative_uri.assert_called_with("examples/topic-box", "getting-started/installation")


def test_resolve_link_relative_path():
    """Test relative path resolution."""
    env = MagicMock()
    env.docname = "examples/topic-box"
    env.found_docs = {"examples/code-blocks"}
    env.app.builder.get_relative_uri.return_value = "code-blocks.html"
    
    result = resolve_link("code-blocks", env)
    assert result == "code-blocks.html"
    env.app.builder.get_relative_uri.assert_called_with("examples/topic-box", "examples/code-blocks")


def test_resolve_link_parent_directory():
    """Test parent directory reference resolution."""
    env = MagicMock()
    env.docname = "examples/topic-box"
    env.found_docs = {"getting-started/installation"}
    env.app.builder.get_relative_uri.return_value = "getting-started/installation.html"
    
    result = resolve_link("../getting-started/installation", env)
    assert result == "getting-started/installation.html"
    env.app.builder.get_relative_uri.assert_called_with("examples/topic-box", "getting-started/installation")


def test_resolve_link_index_fallback():
    """Test fallback to index when document not found."""
    env = MagicMock()
    env.docname = "examples/topic-box"
    env.found_docs = {"getting-started/index"}
    env.app.builder.get_relative_uri.return_value = "getting-started/index.html"
    
    result = resolve_link("/getting-started", env)
    assert result == "getting-started/index.html"
    env.app.builder.get_relative_uri.assert_called_with("examples/topic-box", "getting-started/index")


def test_resolve_link_html_fallback():
    """Test fallback to .html extension when document not found."""
    env = MagicMock()
    env.docname = "examples/topic-box"
    env.found_docs = set()  # Empty set, no documents found
    
    result = resolve_link("/nonexistent", env)
    assert result == "nonexistent.html"


def test_resolve_link_anchor():
    """Test that anchor links are returned unchanged."""
    env = MagicMock()
    result = resolve_link("#section-name", env)
    assert result == "#section-name"
    
    result = resolve_link("#", env)
    assert result == "#"
