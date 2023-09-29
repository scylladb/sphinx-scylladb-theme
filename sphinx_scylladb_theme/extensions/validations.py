from sphinx.util import logging

logger = logging.getLogger(__name__)


def warn_on_underscores(app, docname, source):
    if not docname:
        return False

    excluded_strings = ["rst_include", "_common"]

    theme_options = app.config.html_theme_options
    skip_warnings = theme_options.get("skip_warnings", [])

    if "document_has_underscores" in skip_warnings:
        return False

    if "_" in docname and not any(excluded in docname for excluded in excluded_strings):
        logger.warning(f"Document name contains underscores: {docname}")
        return True
    return False


def setup(app):
    app.connect("source-read", warn_on_underscores)
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
