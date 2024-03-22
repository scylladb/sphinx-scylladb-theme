import pytest
from bs4 import BeautifulSoup as bs
from unittest.mock import Mock

from sphinx_scylladb_theme.extensions.hero_box import HeroBox

pre_content_data = [
    [
        [],
        {"title": "Lorem Ipsum", "class": "hero_test"},
        ["Content"],
        """
        <div class="hero hero_test">
                <div class="hero-wrapper">
                    <div class="hero__img">
                    </div>
                    <div class="hero-header">
                        <h1 class="hero__title">Lorem Ipsum</h1>
                        <div class="hero__text">
        """,
    ],
    [
        [],
        {"title": "Lorem Ipsum", "class": "hero_test", "image": "image.png"},
        ["Content"],
        """
        <div class="hero hero_test">
                <div class="hero-wrapper">
                    <div class="hero__img">
                        <img src="image.png" />
                    </div>
                    <div class="hero-header">
                        <h1 class="hero__title">Lorem Ipsum</h1>
                        <div class="hero__text">
        """,
    ],
]

post_content_data = [
    [
        [],
        {
            "title": "Lorem Ipsum",
            "button_icon": "fa",
            "button_text": "Test",
            "button_url": "#",
        },
        ["Content"],
        """
        </div>
        <a href="#">
            <button class="hero__button button">
                <i class="icon fa" aria-hidden="true"></i>
                Test
            </button>
        </a>
        </div></div></div>
        """,
    ],
    [
        [],
        {"title": "Lorem Ipsum", "search_box": True},
        ["Content"],
        """
        </div>
        <div class="hero__search-box search-box search-box--hero">
            <ci-search></ci-search>
        </div>
        </div></div></div>
        """,
    ],
]

mock_state_machine = Mock()
mock_state_machine.reporter = Mock()
mock_state = Mock()


@pytest.mark.parametrize("arguments, options, content, expected", pre_content_data)
def test_pre_content(arguments, options, content, expected):
    directive = HeroBox("component", arguments, options, content, 0, 0, "", mock_state_machine, mock_state)
    result = directive.run()
    assert bs(result[0].astext(), "html.parser") == bs(expected, "html.parser")


@pytest.mark.parametrize("arguments, options, content, expected", post_content_data)
def test_post_content(arguments, options, content, expected):
    directive = HeroBox("component", arguments, options, content, 0, 0, "", mock_state_machine, mock_state)
    result = directive.run()
    assert (
        bs(result[2].astext(), "html.parser").prettify()
        == bs(expected, "html.parser").prettify()
    )
