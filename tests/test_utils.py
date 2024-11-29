from sphinx_scylladb_theme.utils import multiversion_regex_builder, fetch_multiversion_configuration
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
