from sphinx.util import logging

logger = logging.getLogger(__name__)

from sphinx_scylladb_theme.extensions.validations import (
    raise_warning_if_document_has_underscores,
)


def test_raise_warning_if_document_has_underscores():
    raise_warning_if_document_has_underscores(None, "file_name.rst", None)
    assert logger.warning.called
