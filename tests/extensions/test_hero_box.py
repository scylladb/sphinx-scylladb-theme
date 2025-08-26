from unittest.mock import Mock

import pytest
from bs4 import BeautifulSoup as bs

from sphinx_scylladb_theme.extensions.hero_box import HeroBox

pre_content_data = [
    [
        # Test hero header
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
        # Test hero with image
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
        # Test search box
        [],
        {"title": "Lorem Ipsum", "search_box": True},
        ["Content"],
        """
        </div>
        <div class="hero__search-wrapper">
            <div class="hero__search-box search-box search-box--hero">
                <ci-search></ci-search>
            </div>
        </div>
        </div></div></div>
        """,
    ],
    [
        # Test search box with AI chatbot
        [],
        {"title": "Lorem Ipsum", "search_box": True, "ai_chatbot_id": "test-chatbot-id"},
        ["Content"],
        """
        </div>
        <div class="hero__search-wrapper">
            <div class="hero__search-box search-box search-box--hero">
                <ci-search></ci-search>
            </div>
                <div class="hero__ask-ai">
                    <biel-button project="test-chatbot-id"
                        header-title="ScyllaDB chatbot (beta)"
                        button-position="default"
                        modal-position="bottom-right"
                        button-style="dark">Ask AI</biel-button>
                </div>
        </div>
        </div></div></div>
        """,
    ],
    [
        # Test button with icon
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
                <i class="icon icon--left fa" aria-hidden="true"></i>
                Test
            </button>
        </a>
        </div></div></div>
        """,
    ],
    [
        # Test button with icon on the right
        [],
        {
            "title": "Learn more",
            "button_icon": "fa",
            "button_text": "Discover",
            "button_url": "#",
            "button_icon_position": "right",
        },
        ["Content"],
        """
        </div>
        <a href="#">
            <button class="hero__button button">
                Discover<i class="icon icon--right fa" aria-hidden="true"></i>
            </button>
        </a>
        </div></div></div>
        """,
    ],
    [
        # Test button with CTA
        [],
        {
            "title": "Learn more",
            "button_icon": "fa",
            "button_text": "Discover",
            "button_url": "#",
            "cta": "More info",
            "button_icon_position": "right",
        },
        ["Content"],
        """
        </div>
        <a href="#">
            <button class="hero__button button">
                Discover <span class='hero__cta'>More info</span><i class="icon icon--right fa" aria-hidden="true"></i> 
            </button>
        </a>
        </div></div></div>
        """,
    ],
    [
        # Test button with bold style
        [],
        {
            "title": "Check Now",
            "button_icon": "icon-check",
            "button_text": "Submit",
            "button_url": "#",
            "button_style": "bold",
        },
        ["Content"],
        """
        </div>
        <a href="#">
            <button class="hero__button button hero__button--bold">
                <i class="icon icon--left icon-check" aria-hidden="true"></i>
                Submit
            </button>
        </a>
        </div></div></div>
        """,
    ],
    [
        # Test button with CTA & icon as link
        [],
        {
            "title": "Learn more",
            "button_icon": "fa",
            "button_text": "Discover",
            "button_url": "#",
            "cta": "More info",
            "button_icon_position": "right",
            "button_icon_link": True,
        },
        ["Content"],
        """
        </div>
        <a href="#">
            <button class="hero__button button">
                Discover <span class='hero__cta'>More info</span><i class="icon icon--right icon--link fa" aria-hidden="true"></i>
            </button>
        </a>
        </div></div></div>
        """,
    ],
]

mock_state_machine = Mock()
mock_state_machine.reporter = Mock()
mock_state = Mock()


@pytest.mark.parametrize("arguments, options, content, expected", pre_content_data)
def test_pre_content(arguments, options, content, expected):
    directive = HeroBox(
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
    assert bs(result[0].astext(), "html.parser") == bs(expected, "html.parser")


@pytest.mark.parametrize("arguments, options, content, expected", post_content_data)
def test_post_content(arguments, options, content, expected):
    directive = HeroBox(
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
        bs(result[2].astext(), "html.parser").prettify()
        == bs(expected, "html.parser").prettify()
    )
