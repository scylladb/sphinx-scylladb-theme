from sphinx.util import logging


def raise_warning_if_document_has_underscores(app, docname, source):
    if "_" in docname:
        logger = logging.getLogger(__name__)
        logger.warning("Document name contains underscores: %s" % docname)


def setup(app):
    app.connect("source-read", raise_warning_if_document_has_underscores)
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
