from pytest import raises
from sphinx.errors import SphinxWarning

from sphinx_scylladb_theme.extensions.validations import (
    raise_warning_if_document_has_underscores,
)


def test_raise_warning_if_document_has_underscores():
    with raises(SphinxWarning):
        raise_warning_if_document_has_underscores(None, "file_name.rst", None)
