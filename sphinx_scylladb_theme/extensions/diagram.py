"""
Sphinx directive that wraps a figure, image, or mermaid block with
metadata so external tools can filter and extract diagrams.

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

The extension also emits ``diagrams.json`` at the root of the build
output. Each entry contains the metadata plus either an absolute image
URL (``type: "image"``) or the raw mermaid source (``type: "mermaid"``).
"""

import html
import json
import os
from pathlib import Path

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from .utils import base_url

_DATA_KEYS = ("tags", "categories", "deployment", "last-reviewed")
_HTML_BUILDERS = {"html", "dirhtml"}


def _comma_list(argument):
    if not argument:
        return ""
    parts = [p.strip() for p in argument.split(",") if p.strip()]
    return ",".join(parts)


def _split(value):
    return [p for p in (value or "").split(",") if p]


class diagram_node(nodes.General, nodes.Element):
    """Doctree node carrying a wrapped diagram and its metadata."""


def visit_diagram_html(self, node):
    attrs = []
    diagram_id = node.get("diagram_id", "")
    if diagram_id:
        attrs.append(f'id="{html.escape(diagram_id, quote=True)}"')
    for key in _DATA_KEYS:
        value = node.get(key, "")
        if value:
            attrs.append(f'data-{key}="{html.escape(value, quote=True)}"')
    attr_str = (" " + " ".join(attrs)) if attrs else ""
    self.body.append(f'<div class="diagram"{attr_str}>')


def depart_diagram_html(self, node):
    self.body.append("</div>")


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
        node = diagram_node()
        node["diagram_id"] = self.options.get("id", "").strip()
        for key in _DATA_KEYS:
            node[key] = self.options.get(key, "").strip()

        if self.state and self.content:
            self.state.nested_parse(self.content, self.content_offset, node)

        return [node]


def _page_url(app, docname, anchor=""):
    base = base_url(app.config)
    builder = app.builder.name if app.builder is not None else ""
    suffix = "/" if builder == "dirhtml" else ".html"
    if docname == "index":
        path = ""
        suffix = ""
    elif docname.endswith("/index"):
        path = docname[: -len("index")]
        suffix = ""
    else:
        path = docname
    page = f"{base}/{path}{suffix}" if base else f"{path}{suffix}"
    if anchor:
        page = f"{page}#{anchor}"
    return page


def _image_url(app, uri):
    base = base_url(app.config)
    if not uri:
        return None
    if uri.startswith(("http://", "https://", "data:")):
        return uri
    if uri.startswith("_images/"):
        served = uri
    else:
        mapped = getattr(app.env, "images", {}).get(uri)
        if mapped:
            served = f"_images/{mapped[1]}"
        else:
            served = f"_images/{os.path.basename(uri)}"
    return f"{base}/{served}" if base else f"/{served}"


def _is_mermaid(node):
    return node.__class__.__name__ == "mermaid"


def _extract_entry(app, docname, node):
    diagram_id = node.get("diagram_id") or None
    entry = {
        "id": diagram_id,
        "page": docname,
        "page_url": _page_url(app, docname, anchor=diagram_id or ""),
        "tags": _split(node.get("tags", "")),
        "categories": _split(node.get("categories", "")),
        "deployment": node.get("deployment") or None,
        "last_reviewed": node.get("last-reviewed") or None,
    }

    for child in node.traverse():
        if _is_mermaid(child):
            entry["type"] = "mermaid"
            entry["content"] = child.get("code", "")
            return entry

    for img in node.traverse(nodes.image):
        entry["type"] = "image"
        entry["content"] = _image_url(app, img.get("uri", ""))
        return entry

    return None


def write_diagrams_json(app, exception):
    if exception is not None:
        return
    if app.builder is None or app.builder.name not in _HTML_BUILDERS:
        return

    all_entries = []
    env = app.env
    for docname in sorted(env.found_docs):
        try:
            doctree = env.get_doctree(docname)
        except Exception:
            continue
        for node in doctree.traverse(diagram_node):
            entry = _extract_entry(app, docname, node)
            if entry is not None:
                all_entries.append(entry)

    out_path = Path(app.builder.outdir) / "diagrams.json"
    out_path.write_text(
        json.dumps({"diagrams": all_entries}, indent=2, sort_keys=False),
        encoding="utf-8",
    )


def setup(app):
    app.add_node(diagram_node, html=(visit_diagram_html, depart_diagram_html))
    app.add_directive("diagram", Diagram)
    app.connect("build-finished", write_diagrams_json)

    return {
        "version": "0.2",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
