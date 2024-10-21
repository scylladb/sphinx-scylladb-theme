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
        '<span data-tooltip data-tooltip-height="0" tabindex="1" title="This is a tooltip" class="top">Test tooltip</span>',
        {},
        False,
    ],
]

mock_inliner = Mock()
mock_inliner.document.settings.env = Mock()
mock_inliner.document.reporter.error = Mock()

@pytest.mark.parametrize("role_name, input_text, expected_output, glossary, is_error", tooltip_data)
def test_include_tooltip_role(role_name, input_text, expected_output, glossary, is_error):
    glossary = glossary or {}
    mock_inliner.document.settings.env.get_domain = Mock(return_value=Mock(_terms=glossary))
    
    name = role_name
    rawtext = input_text
    text = input_text
    lineno = 0
    inliner = mock_inliner
    options = {}
    content = []

    result, messages = include_tooltip_role(name, rawtext, text, lineno, inliner, options, content)
    
    assert len(result) == 1
    node = result[0]
    assert isinstance(node, include_tooltip_node)

    output_html = f'<span data-tooltip data-tooltip-height="0" tabindex="1" title="{node["tooltip_source"]}" class="top">{node.astext()}</span>'
    assert bs(output_html, "html.parser").prettify() == bs(expected_output, "html.parser").prettify()
