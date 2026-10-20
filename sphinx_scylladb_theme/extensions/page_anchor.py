"""
Sphinx role to link to an arbitrary anchor of any page in the project.

Sphinx cross-reference roles (``:ref:``, ``:doc:``) can only target anchors
that exist in the doctree at build time. Anchors generated client-side by
JavaScript widgets (Redoc, Swagger UI, etc.) are invisible to Sphinx, so
pages like an OpenAPI reference cannot be deep-linked with standard roles.

This role resolves the page URL through the builder (so relative paths stay
correct at any nesting depth and in multiversion builds) and appends the
anchor verbatim, without validating it:

.. code-block:: rst

   :page-anchor:`Install Vector Search </api#tag/VectorSearch/operation/installVectorSearch>`
   :page-anchor:`/api#tag/VectorSearch/operation/installVectorSearch`
"""

from posixpath import dirname, join, normpath

from docutils import nodes
from sphinx.util import logging
from sphinx.util.docutils import SphinxRole
from sphinx.util.nodes import split_explicit_title

LOGGER = logging.getLogger(__name__)


class page_anchor_pending(nodes.Element):
    """Placeholder node resolved once the builder can compute URLs."""


class PageAnchorRole(SphinxRole):
    def run(self):
        has_explicit_title, title, target = split_explicit_title(self.text)

        if "#" in target:
            docpath, anchor = target.split("#", 1)
        else:
            docpath, anchor = target, ""

        if docpath.startswith("/"):
            docname = docpath.lstrip("/")
        else:
            docname = normpath(join(dirname(self.env.docname), docpath))

        if not has_explicit_title:
            title = target

        node = page_anchor_pending(
            self.rawtext,
            docname=docname,
            anchor=anchor,
            title=title,
        )
        self.set_source_info(node)
        return [node], []


def resolve_page_anchors(app, doctree, fromdocname):
    additional_pages = getattr(app.config, "html_additional_pages", None) or {}

    for node in list(doctree.findall(page_anchor_pending)):
        docname = node["docname"]
        anchor = node["anchor"]
        title = node["title"]

        if docname not in app.env.found_docs and docname not in additional_pages:
            LOGGER.warning(
                "page-anchor: unknown document %r (not a source document "
                "or an html_additional_pages entry)",
                docname,
                location=node,
            )

        try:
            uri = app.builder.get_relative_uri(fromdocname, docname)
        except Exception:
            uri = docname
        if anchor:
            uri += "#" + anchor

        reference = nodes.reference("", "", internal=True, refuri=uri)
        reference += nodes.inline(title, title, classes=["page-anchor"])
        node.replace_self(reference)


def setup(app):
    app.add_role("page-anchor", PageAnchorRole())
    app.connect("doctree-resolved", resolve_page_anchors)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
