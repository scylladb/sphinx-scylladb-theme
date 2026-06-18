from unittest.mock import Mock

import pytest
from bs4 import BeautifulSoup as bs

from sphinx_scylladb_theme.extensions.diagram import Diagram, _comma_list

test_data = [
    [
        # All metadata options.
        [],
        {
            "id": "auth-flow",
            "tags": "networking,security",
            "categories": "security",
            "deployment": "core",
            "last-reviewed": "2026-06-01",
        },
        ["placeholder"],
        '<div class="diagram" id="auth-flow"'
        ' data-tags="networking,security"'
        ' data-categories="security"'
        ' data-deployment="core"'
        ' data-last-reviewed="2026-06-01">',
        "</div>",
    ],
    [
        # No options: bare wrapper, no attributes beyond the class.
        [],
        {},
        ["placeholder"],
        '<div class="diagram">',
        "</div>",
    ],
    [
        # Only :id: set.
        [],
        {"id": "diagram-1"},
        ["placeholder"],
        '<div class="diagram" id="diagram-1">',
        "</div>",
    ],
    [
        # HTML-special characters in option values are escaped.
        [],
        {"id": 'a"b', "tags": "<x>"},
        ["placeholder"],
        '<div class="diagram" id="a&quot;b" data-tags="&lt;x&gt;">',
        "</div>",
    ],
]

mock_state_machine = Mock()
mock_state_machine.reporter = Mock()
mock_state = Mock()


@pytest.mark.parametrize(
    "arguments, options, content, expected_open, expected_close", test_data
)
def test_diagram_wrapper(arguments, options, content, expected_open, expected_close):
    directive = Diagram(
        "diagram",
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
    assert len(result) == 3
    assert bs(result[0].astext(), "html.parser") == bs(expected_open, "html.parser")
    assert bs(result[2].astext(), "html.parser") == bs(expected_close, "html.parser")


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("networking, security", "networking,security"),
        ("  a , b ,c  ", "a,b,c"),
        ("a,,b", "a,b"),
        ("", ""),
        (None, ""),
    ],
)
def test_comma_list_normalizes_values(raw, expected):
    assert _comma_list(raw) == expected
