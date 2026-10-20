from unittest.mock import Mock

import pytest
from docutils import nodes

from sphinx_scylladb_theme.extensions.page_anchor import (
    PageAnchorRole,
    page_anchor_pending,
    resolve_page_anchors,
)

role_data = [
    # input_text, current_docname, expected_docname, expected_anchor, expected_title
    [
        "Link text </api#tag/Tag/operation/opId>",
        "examples/links",
        "api",
        "tag/Tag/operation/opId",
        "Link text",
    ],
    [
        "/api#tag/Tag/operation/opId",
        "examples/links",
        "api",
        "tag/Tag/operation/opId",
        "/api#tag/Tag/operation/opId",
    ],
    # Relative path resolves against the current document, like :doc:
    [
        "Sibling <sibling#section>",
        "examples/links",
        "examples/sibling",
        "section",
        "Sibling",
    ],
    [
        "Parent <../index#section>",
        "examples/links",
        "index",
        "section",
        "Parent",
    ],
    # No anchor at all
    [
        "Plain </api>",
        "examples/links",
        "api",
        "",
        "Plain",
    ],
]


def run_role(input_text, current_docname):
    role = PageAnchorRole()
    inliner = Mock()
    inliner.document.settings.env.docname = current_docname
    inliner.reporter.get_source_and_line = Mock(return_value=("links.rst", 1))
    result, messages = role("page-anchor", input_text, input_text, 1, inliner)
    return result, messages


@pytest.mark.parametrize(
    "input_text, current_docname, expected_docname, expected_anchor, expected_title",
    role_data,
)
def test_page_anchor_role(
    input_text, current_docname, expected_docname, expected_anchor, expected_title
):
    result, messages = run_role(input_text, current_docname)

    assert messages == []
    assert len(result) == 1
    node = result[0]
    assert isinstance(node, page_anchor_pending)
    assert node["docname"] == expected_docname
    assert node["anchor"] == expected_anchor
    assert node["title"] == expected_title


def make_app(found_docs, additional_pages=None, relative_uri="../api.html"):
    app = Mock()
    app.config.html_additional_pages = additional_pages or {}
    app.env.found_docs = found_docs
    app.builder.get_relative_uri = Mock(return_value=relative_uri)
    return app


def make_doctree(pending):
    paragraph = nodes.paragraph()
    paragraph += pending
    return paragraph


def test_resolve_page_anchors_builds_relative_uri():
    pending = page_anchor_pending(
        "", docname="api", anchor="tag/Tag/operation/opId", title="Link text"
    )
    doctree = make_doctree(pending)
    app = make_app(found_docs={"api"}, relative_uri="../api.html")

    resolve_page_anchors(app, doctree, "examples/links")

    # The URI must come from the builder relative to the current page, so
    # links stay inside the version subdirectory in multiversion builds.
    app.builder.get_relative_uri.assert_called_once_with("examples/links", "api")
    reference = doctree.children[0]
    assert isinstance(reference, nodes.reference)
    assert reference["refuri"] == "../api.html#tag/Tag/operation/opId"
    assert reference["internal"] is True
    assert reference.astext() == "Link text"


def test_resolve_page_anchors_without_anchor():
    pending = page_anchor_pending("", docname="api", anchor="", title="Plain")
    doctree = make_doctree(pending)
    app = make_app(found_docs={"api"}, relative_uri="api.html")

    resolve_page_anchors(app, doctree, "index")

    reference = doctree.children[0]
    assert reference["refuri"] == "api.html"


def test_resolve_page_anchors_accepts_additional_pages():
    pending = page_anchor_pending("", docname="api", anchor="x", title="API")
    doctree = make_doctree(pending)
    app = make_app(
        found_docs=set(),
        additional_pages={"api": "redoc.html"},
        relative_uri="api.html",
    )

    resolve_page_anchors(app, doctree, "index")

    reference = doctree.children[0]
    assert reference["refuri"] == "api.html#x"


def test_resolve_page_anchors_warns_on_unknown_document(monkeypatch):
    pending = page_anchor_pending("", docname="missing", anchor="x", title="Broken")
    doctree = make_doctree(pending)
    app = make_app(found_docs={"index"}, relative_uri="missing.html")

    logger = Mock()
    monkeypatch.setattr(
        "sphinx_scylladb_theme.extensions.page_anchor.LOGGER", logger
    )
    resolve_page_anchors(app, doctree, "index")

    assert logger.warning.called
    # The link is still emitted so the build output stays navigable.
    reference = doctree.children[0]
    assert reference["refuri"] == "missing.html#x"
