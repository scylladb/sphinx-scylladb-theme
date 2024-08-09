from unittest.mock import Mock

import pytest
from bs4 import BeautifulSoup as bs
from docutils import nodes

from sphinx_scylladb_theme.extensions.include_tooltip import (
    include_tooltip_role,
    include_tooltip_node,
)

tooltip_data = [
    # Test basic tooltip with text
    [
        "include_tooltip",
        "Test tooltip <This is a tooltip>",
        '<span data-tooltip tabindex="1" title="This is a tooltip" data-position="top">Test tooltip</span>',
        {},
        False,
    ],
    # Test tooltip with glossary term
    [
        "include_tooltip",
        "Glossary term <term1>",
        '<span data-tooltip tabindex="1" title="Glossary definition for term1" data-position="top">Glossary term</span>',
        {"term1": [nodes.Text("Glossary definition for term1")]},
        False,
    ],
]

mock_inliner = Mock()
mock_inliner.document.settings.env = Mock()
mock_inliner.document.reporter.error = Mock()

@pytest.mark.parametrize("role_name, input_text, expected_output, glossary, is_error", tooltip_data)
def test_include_tooltip_role(role_name, input_text, expected_output, glossary, is_error):
    glossary = glossary or {}
    mock_inliner.document.settings.env.domains = {"std": Mock(data={"terms": glossary})}

    # Directly call include_tooltip_role with required arguments
    name = role_name
    rawtext = input_text
    text = input_text
    lineno = 0
    inliner = mock_inliner
    result, messages = include_tooltip_role(name, rawtext, text, lineno, inliner)
    assert len(result) == 1
    node = result[0]
    assert isinstance(node, include_tooltip_node)

    # Check the output by converting the node to HTML and comparing it
    output_html = f'<span data-tooltip tabindex="1" title="{node["tooltip"]}">{node.astext()} <i class="scylla-icon scylla-icon--help"></i></span>'
    assert bs(output_html, "html.parser").prettify() == bs(expected_output, "html.parser").prettify()
