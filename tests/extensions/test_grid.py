from unittest.mock import Mock

import pytest
from bs4 import BeautifulSoup as bs

from sphinx_scylladb_theme.extensions.grid import Grid

test_data = [
    [
        # Test basic grid
        [],
        {"type": "default"},
        ["Content"],
        """
        <div class="topics-grid">
            <div class="grid-container full">
                <div class="grid-x grid-margin-x">
        """,
    ],
    [
        # Test grid with title and text
        [],
        {
            "type": "default",
            "title": "Test Title",
            "text": "Test Description",
        },
        ["Content"],
        """
        <div class="topics-grid">
            <h2 class="topics-grid__title">Test Title</h2>
            <p class="topics-grid__text">Test Description</p>
            <div class="grid-container full">
                <div class="grid-x grid-margin-x">
        """,
    ],
    [
        # Test scrollable grid
        [],
        {"type": "scrollable"},
        ["Content"],
        """
        <div class="topics-grid topics-grid--scrollable">
            <div class="grid-container full">
                <div class="grid-x grid-margin-x hs">
        """,
    ],
    [
        # Test products grid
        [],
        {"type": "products"},
        ["Content"],
        """
        <div class="topics-grid topics-grid--products">
            <div class="grid-container full">
                <div class="grid-x grid-margin-x">
        """,
    ],
    [
        # Test grid with custom class
        [],
        {"type": "default", "class": "custom-grid"},
        ["Content"],
        """
        <div class="topics-grid custom-grid">
            <div class="grid-container full">
                <div class="grid-x grid-margin-x">
        """,
    ],
    [
        # Test products grid with title and text
        [],
        {
            "type": "products",
            "title": "Products",
            "text": "Choose your product",
        },
        ["Content"],
        """
        <div class="topics-grid topics-grid--products">
            <h2 class="topics-grid__title">Products</h2>
            <p class="topics-grid__text">Choose your product</p>
            <div class="grid-container full">
                <div class="grid-x grid-margin-x">
        """,
    ],
]

mock_state_machine = Mock()
mock_state_machine.reporter = Mock()
mock_state = Mock()


@pytest.mark.parametrize("arguments, options, content, expected", test_data)
def test(arguments, options, content, expected):
    directive = Grid(
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