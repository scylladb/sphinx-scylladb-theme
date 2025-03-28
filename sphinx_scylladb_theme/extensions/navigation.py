"""
Extension for Sphinx that generates a navigation tree with dropdowns
from Sphinx's toctree function's output.


Adapted from https://github.com/pradyunsg/furo
(Copyright (c) 2020 Pradyun Gedam, MIT License)
for sphinx-scylladb-theme.
"""

import functools

from bs4 import BeautifulSoup


@functools.lru_cache(maxsize=None)
def get_navigation_tree(toctree_html: str, collapse: bool) -> str:
    """Modify the given navigation tree, with furo-specific elements.
    Adds a checkbox + corresponding label to <li>s that contain a <ul> tag, to enable
    the I-spent-too-much-time-making-this-CSS-only collapsing sidebar tree.
    """
    if not toctree_html:
        return toctree_html

    soup = BeautifulSoup(toctree_html, "html.parser")

    toctree_checkbox_count = 0
    last_element_with_current = None
    for element in soup.find_all("li", recursive=True):
        # We check all "li" elements, to add a "current-page" to the correct li.
        classes = element.get("class", [])
        if "current" in classes:
            last_element_with_current = element

        # Nothing more to do, unless this has "children" or sidebar is collapsed
        if not element.find("ul") or collapse:
            continue

        # Add a class to indicate that this has children.
        element["class"] = classes + ["has-children"]

        # We're gonna add a checkbox.
        toctree_checkbox_count += 1
        checkbox_name = f"toctree-checkbox-{toctree_checkbox_count}"

        # Add the "label" for the checkbox which will get filled.
        label = soup.new_tag("label", attrs={"for": checkbox_name})
        label.append(
            soup.new_tag("i", attrs={"class": "icon-chevron-right"})
        )
        element.insert(1, label)
        space = soup.new_tag("div", attrs={"class": "break"})
        element.insert(2, space)

        # Add the checkbox that's used to store expanded/collapsed state.
        checkbox = soup.new_tag(
            "input",
            attrs={
                "type": "checkbox",
                "class": ["toctree-checkbox"],
                "id": checkbox_name,
                "name": checkbox_name,
            },
        )
        # if this has a "current" class,
        # be expanded by default (by checking the checkbox)
        if "current" in classes:
            checkbox.attrs["checked"] = ""

        element.insert(1, checkbox)

    if last_element_with_current is not None:
        last_element_with_current["class"].append("current-page")

    return str(soup)


@functools.lru_cache(maxsize=None)
def side_nav_has_one_item(toc: str) -> bool:
    """Check if the toc has exactly one list item."""

    soup = BeautifulSoup(toc, "html.parser")
    if len(soup.find_all("li")) == 1:
        return True

    return False
