from unittest.mock import MagicMock

from sphinx_scylladb_theme.extensions.validations import (
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
