"""
Sphinx directive that wraps a figure or image with metadata so external
tools can filter and extract diagrams.

Usage::

    .. diagram::
       :id: auth-flow
       :tags: networking, security
       :categories: security
       :deployment: core
       :last-reviewed: 2026-06-01

       .. figure:: images/auth-flow.png
          :alt: Authentication flow

          Authentication flow diagram.

The wrapped content is rendered inside a ``<div class="diagram">``. The
``id`` option becomes the element ``id`` attribute, and the remaining
options are exposed as ``data-*`` attributes.
Comma-separated values in ``tags`` and ``categories`` are normalized
(whitespace trimmed).
"""

import html

from docutils import nodes
from docutils.parsers.rst import Directive, directives


def _comma_list(argument):
    if not argument:
        return ""
    parts = [p.strip() for p in argument.split(",") if p.strip()]
    return ",".join(parts)


class Diagram(Directive):
    has_content = True
    option_spec = {
        "id": directives.unchanged,
        "tags": _comma_list,
        "categories": _comma_list,
        "deployment": directives.unchanged,
        "last-reviewed": directives.unchanged,
    }

    def run(self):
        attrs = []
        diagram_id = self.options.get("id", "").strip()
        if diagram_id:
            attrs.append(f'id="{html.escape(diagram_id, quote=True)}"')
        for key in ("tags", "categories", "deployment", "last-reviewed"):
            value = self.options.get(key, "").strip()
            if value:
                attrs.append(f'data-{key}="{html.escape(value, quote=True)}"')

        attr_str = (" " + " ".join(attrs)) if attrs else ""
        open_html = f'<div class="diagram"{attr_str}>'
        close_html = "</div>"

        content_node = nodes.container()
        if self.state and self.content:
            self.state.nested_parse(self.content, self.content_offset, content_node)

        return [
            nodes.raw(text=open_html, format="html"),
            content_node,
            nodes.raw(text=close_html, format="html"),
        ]


def setup(app):
    app.add_directive("diagram", Diagram)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
