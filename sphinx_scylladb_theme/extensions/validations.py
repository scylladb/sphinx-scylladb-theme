from sphinx.util import logging

logger = logging.getLogger(__name__)


def raise_warning_if_document_has_underscores(app, docname, source):
    result = False
    
    theme_options = app.config.html_theme_options
    if 'skip_warnings' in theme_options and 'document_has_underscores' in theme_options['skip_warnings']:
        return result
    
    if "_" in docname:
        logger.warning("Document name contains underscores: %s" % docname)
        result = True
    return result


def setup(app):
    app.connect("source-read", raise_warning_if_document_has_underscores)
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
