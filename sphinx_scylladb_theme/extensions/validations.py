from urllib.parse import urlparse

from docutils import nodes
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


def warn_on_internal_docs_as_external_links(app, doctree, docname):
    theme_options = app.config.html_theme_options
    skip_warnings = theme_options.get("skip_warnings", [])
    if "internal_docs_as_external_link" in skip_warnings:
        return False

    reported = False
    for ref in doctree.traverse(nodes.reference):
        if ref.get("internal"):
            continue
        refuri = ref.get("refuri", "")
        if not refuri or refuri.startswith("#") or urlparse(refuri).scheme:
            continue
        line = ref.line or (ref.parent.line if ref.parent is not None else 0) or 0
        logger.warning(
            'External link "%s" has no URL scheme. '
            "Use :doc:`%s` for internal docs or prefix with http/https/mailto/... .",
            refuri,
            refuri,
            location=(docname, line),
        )
        reported = True
    return reported


def setup(app):
    app.connect("source-read", warn_on_underscores)
    app.connect("doctree-resolved", warn_on_internal_docs_as_external_links)
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
