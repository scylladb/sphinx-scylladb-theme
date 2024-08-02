from unittest.mock import Mock
import pytest
from docutils import nodes
from docutils.parsers.rst import roles
from bs4 import BeautifulSoup as bs
from sphinx.testing.util import SphinxTestApp
from sphinx.util.docutils import new_document

from sphinx_scylladb_theme.extensions.hero_box import (
    include_tooltip_role,
    include_tooltip_node,
    visit_include_tooltip_node_html,
    depart_include_tooltip_node_html,
)

# Setup mock environment
mock_inliner = Mock()
mock_inliner.document.settings.env = Mock()
mock_inliner.document.reporter.error = Mock()

tooltip_data = [
    # Test basic tooltip with text
    (
        "include_tooltip",
        "Test tooltip <This is a tooltip>",
        '<span data-tooltip tabindex="1" title="This is a tooltip" data-position="top">Test tooltip <i class="scylla-icon scylla-icon--help"></i></span>',
        {},
        False
    ),
    # Test tooltip with glossary term
    (
        "include_tooltip",
        "Glossary term <term1>",
        '<span data-tooltip tabindex="1" title="Glossary definition for term1" data-position="top">Glossary term <i class="scylla-icon scylla-icon--help"></i></span>',
        {'term1': [nodes.Text("Glossary definition for term1")]},
        False
    ),
    # Test invalid syntax
    (
        "include_tooltip",
        "Invalid syntax text",
        "Invalid syntax for include_tooltip role. Expected format: 'display text <tooltip text or term or file>'",
        None,
        True
    ),
]

@pytest.mark.parametrize("role_name, input_text, expected_output, glossary, is_error", tooltip_data)
def test_include_tooltip_role(role_name, input_text, expected_output, glossary, is_error):
    # Setup glossary if provided
    glossary = glossary or {}
    mock_inliner.document.settings.env.domains = {'std': Mock(data={'terms': glossary})}

    # Register and process the role
    roles.register_local_role(role_name, include_tooltip_role)
    result, messages = roles.role(role_name, input_text, 0, mock_inliner, options={}, content=[])

    # Verify results
    assert len(messages) == int(is_error)

    if is_error:
        assert expected_output in str(messages[0])
        return
    
    assert len(result) == 1
    node = result[0]
    assert isinstance(node, include_tooltip_node)

    output_html = node['tooltip']
    assert bs(output_html, "html.parser") == bs(expected_output, "html.parser")

    app = SphinxTestApp()
    app.add_node(include_tooltip_node, html=(visit_include_tooltip_node_html, depart_include_tooltip_node_html))
    document = new_document("test", app.env.settings)
    document += node
    app.build()

    writer = app.builder.create_writers()[0]
    writer.write(document, None)
    assert bs(writer.output, "html.parser").prettify() == bs(expected_output, "html.parser").prettify()
