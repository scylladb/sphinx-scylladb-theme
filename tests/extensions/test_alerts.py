from unittest.mock import Mock
import pytest
from bs4 import BeautifulSoup as bs

from sphinx_scylladb_theme.extensions.alert import Alert

test_data = [
    [
        [],
        {"link": "https://scylladb.com", "link_text": "Learn more", "icon": "logs", "target": "_blank"},
        ["We’re updating our license & versioning policy."],
        """
        <div class="alert">
            <div><i class="icon-logs"></i> We’re updating our license & versioning policy.</div>
            <div><a href="https://scylladb.com" target="_blank">Learn more <i class="icon-arrow-right"></i></a></div>
        </div>
        """,
    ],
    [
        [],
        {"link": "https://scylladb.com", "link_text": "Learn more about the change", "icon": "logs"},
        ["We’re updating our license & versioning policy."],
        """
        <div class="alert">
            <div><i class="icon-logs"></i> We’re updating our license & versioning policy.</div>
            <div><a href="https://scylladb.com">Learn more about the change <i class="icon-arrow-right"></i></a></div>
        </div>
        """,
    ],
]

mock_state_machine = Mock()
mock_state_machine.reporter = Mock()
mock_state = Mock()


@pytest.mark.parametrize("arguments, options, content, expected", test_data)
def test_alert(arguments, options, content, expected):
    directive = Alert(
        "component",
        arguments,
        options,
        content,
        0,
        0,
        "",
        mock_state_machine,
        mock_state,
    )
    result = directive.run()
    assert (
        bs(result[0].astext(), "html.parser").prettify()
        == bs(expected, "html.parser").prettify()
    )
