"""
Extension for Sphinx that generates a navigation tree with dropdowns
from Sphinx's toctree function's output.


Adapted from https://github.com/pradyunsg/furo
(Copyright (c) 2020 Pradyun Gedam, MIT License)
for sphinx-scylladb-theme.
"""

import functools

from bs4 import BeautifulSoup, NavigableString


def get_navigation_tree(
    toctree_html: str,
    collapse: bool,
    docname: str | None = None,
    builder=None,
    maxdepth: int = 0,
) -> str:
    """Modify the given navigation tree, with furo-specific elements.
    Adds a checkbox + corresponding label to <li>s that contain a <ul> tag, to enable
    the I-spent-too-much-time-making-this-CSS-only collapsing sidebar tree.
    """
    if not toctree_html:
        return toctree_html

    soup = BeautifulSoup(toctree_html, "html.parser")

    if docname is not None:
        relativize_and_mark_current(soup, docname, builder)
        _prune_to_depth(soup, maxdepth)

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
        label.append(soup.new_tag("i", attrs={"class": "icon-chevron-right"}))
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


def _add_class(classes, value):
    return classes + [value] if value not in classes else classes


def _mark_current(element):
    parent = element.parent
    while parent is not None:
        if getattr(parent, "name", None) in ("li", "ul"):
            parent["class"] = _add_class(parent.get("class", []), "current")
        parent = parent.parent


def relativize_and_mark_current(soup, docname: str, builder) -> None:
    """Adapt a root-relative navigation tree to one page.

    The tree is rendered once relative to the root document. Each page needs
    the links relative to its own location and its node marked as current, so
    adjust the already-parsed soup instead of re-rendering the whole toctree.
    """
    current_uri = builder.get_target_uri(docname)
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        if href.startswith(("http://", "https://", "mailto:", "#", "/")):
            continue
        fragment = ""
        if "#" in href:
            href, fragment = href.split("#", 1)
            fragment = "#" + fragment
        trailing_slash = href.endswith("/")
        target = href.rstrip("/")

        if target == current_uri.rstrip("/") and not fragment:
            anchor["href"] = "#"
            anchor["class"] = ["current"] + [
                c for c in anchor.get("class", []) if c != "current"
            ]
            _mark_current(anchor)
            continue

        relative = builder.get_relative_uri(docname, target)
        if trailing_slash and not relative.endswith("/"):
            relative += "/"
        anchor["href"] = relative + fragment


def _decompose(el):
    """Remove ``el`` together with its adjacent whitespace-only text nodes."""
    if el.parent is None:
        return
    prev, nxt = el.previous_sibling, el.next_sibling
    el.decompose()
    for sibling in (prev, nxt):
        if (
            isinstance(sibling, NavigableString)
            and not sibling.strip()
            and sibling.parent is not None
        ):
            sibling.extract()


def _prune_to_depth(soup, maxdepth: int) -> None:
    """Drop navigation levels deeper than ``maxdepth``.

    Sphinx marks the whole branch leading to the current page before pruning,
    so the deepest *surviving* node keeps the current marker.
    """
    if not maxdepth or maxdepth < 0:
        return
    for li in soup.find_all("li"):
        if li.parent is None:
            continue
        for cls in li.get("class", []):
            if cls.startswith("toctree-l") and cls[len("toctree-l") :].isdigit():
                if int(cls[len("toctree-l") :]) > maxdepth:
                    _decompose(li)
                break
    while True:
        empties = [ul for ul in soup.find_all("ul") if not ul.find("li")]
        if not empties:
            break
        for ul in empties:
            _decompose(ul)
