from unittest.mock import Mock

import pytest
from bs4 import BeautifulSoup as bs

from sphinx_scylladb_theme.extensions.topic_box import TopicBox

test_data = [
    [
        [],
        {"title": "Lorem Ipsum", "class": "abc"},
        ["Content"],
        """
        <div class="topic-box abc">
            <div class="card">
                <div class="topic-box__head">
                <h3 class="topic-box__title">Lorem Ipsum</h3>
            </div>
            <div class="topic-box__body">
        """,
    ],
    [
        [],
        {
            "title": "Lorem Ipsum",
            "class": "abc",
            "icon": "scylla-icon",
            "icon_color": "#fff",
        },
        ["Content"],
        """
        <div class="topic-box abc">
            <div class="card">
                <div class="topic-box__head">
                    <div class="topic-box__icon">
                        <i class="scylla-icon" style="color:#fff !important;"></i>
                    </div>
                    <h3 class="topic-box__title">Lorem Ipsum</h3>
                </div>
            <div class="topic-box__body">
        """,
    ],
    [
        [],
        {
            "title": "Lorem Ipsum",
            "class": "abc",
            "image": "test.png",
        },
        ["Content"],
        """
        <div class="topic-box abc">
            <div class="card">
                <div class="topic-box__head">
                    <div class="topic-box__icon"">
                        <img src="test.png"/>
                    </div>
                    <h3 class="topic-box__title">Lorem Ipsum</h3>
                </div>
            <div class="topic-box__body">
        """,
    ],
    [
        [],
        {"title": "Lorem Ipsum", "link": "#"},
        ["Content"],
        """
        <div class="cell topic-box ">
            <a class="card" href="#">
                <div class="topic-box__head">
                    <h3 class="topic-box__title">Lorem Ipsum</h3>
                </div>
                <div class="topic-box__body">
        """,
    ],
    [
        [],
        {"title": "Lorem Ipsum", "link": "https://test.local"},
        ["Content"],
        """
        <div class="cell topic-box ">
            <a class="card" href="https://test.local" target="_blank">
                <div class="topic-box__head">
                    <h3 class="topic-box__title">Lorem Ipsum</h3>
                </div>
                <div class="topic-box__body">
        """,
    ],
]

mock_state_machine = Mock()
mock_state_machine.reporter = Mock()
mock_state = Mock()


@pytest.mark.parametrize("arguments, options, content, expected", test_data)
def test(arguments, options, content, expected):
    directive = TopicBox(
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
