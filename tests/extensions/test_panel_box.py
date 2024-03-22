from unittest.mock import Mock
import pytest
from bs4 import BeautifulSoup as bs

from sphinx_scylladb_theme.extensions.panel_box import PanelBox

test_data = [
    [
        [],
        {"title": "Lorem Ipsum", "class": "abc"},
        ["Content"],
        """
        <div class="cell abc">
            <div class="panel">
            <h5 class="panel__title">Lorem Ipsum</h5>
        """,
    ],
]

mock_state_machine = Mock()
mock_state_machine.reporter = Mock()
mock_state = Mock()


@pytest.mark.parametrize("arguments, options, content, expected", test_data)
def test(arguments, options, content, expected):
    directive = PanelBox("component", arguments, options, content, 0, 0, "", mock_state_machine, mock_state)
    result = directive.run()
    assert (
        bs(result[0].astext(), "html.parser").prettify()
        == bs(expected, "html.parser").prettify()
    )
