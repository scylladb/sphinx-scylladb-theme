from os import getenv, path

import sphinx_collapse
import sphinx_copybutton
import sphinx_substitution_extensions
from notfound import extension as not_found
from sphinx_tabs import tabs
from sphinxcontrib import mermaid

from sphinx.environment.adapters.toctree import global_toctree_for_doc
from sphinx_scylladb_theme._version import version
from sphinx_scylladb_theme.extensions import (
    alerts,
    diagram,
    grid,
    hero_box,
    include_tooltip,
    labels,
    last_updated,
    multiversion,
    navigation,
    page_anchor,
    panel_box,
    topic_box,
    validations,
)
from sphinx_scylladb_theme.extensions.utils import base_url
from sphinx_scylladb_theme.lexers import cql, ditaa


def compute_toc_tree(toctree, maxdepth, collapse):
    if toctree:
        toctree_html = toctree(
            collapse=collapse,
            titles_only=True,
            maxdepth=maxdepth,
            includehidden=True,
        )
    else:
        toctree_html = ""
    toctree_html = navigation.get_navigation_tree(toctree_html, collapse)
    return toctree_html


_BASE_TOCTREE_CACHE: dict = {}

# Sphinx has no "no limit" value for toctree depth: 0 means "use the toctree's
# own :maxdepth:". Render the cached base tree with this large depth so every
# level is present, then apply the caller's real depth per page via
# navigation._prune_to_depth.
_UNPRUNED_MAXDEPTH = 10_000


def _get_root_toctree(builder, maxdepth, collapse):
    """Render the global toctree once, relative to the root document.

    Rendering it per page is O(pages x tree) and dominates build time on large
    sites: Sphinx resolves and deep-copies the whole tree on every call. The
    per-page differences are only the relative links and the "current" marker,
    which ``navigation.relativize_and_mark_current`` applies to this cached
    HTML instead.
    """
    key = (builder, collapse)
    cached = _BASE_TOCTREE_CACHE.get(key)
    if cached is None:
        root_doc = getattr(builder.config, "root_doc", None) or builder.config.master_doc
        node = global_toctree_for_doc(
            builder.env,
            root_doc,
            builder,
            tags=builder.tags,
            collapse=collapse,
            maxdepth=_UNPRUNED_MAXDEPTH,
            titles_only=True,
            includehidden=True,
        )
        cached = builder.render_partial(node)["fragment"] if node is not None else ""
        _BASE_TOCTREE_CACHE[key] = cached
    return cached


def make_navigation_tree(app, pagename):
    """Return the ``navigation_tree`` callable for one page.

    Keeps the signature the templates call, but serves the cached,
    per-page-adjusted tree instead of re-rendering the global toctree.
    """

    def navigation_tree(toctree, maxdepth, collapse):
        if collapse:
            return compute_toc_tree(toctree, maxdepth, collapse)
        base = _get_root_toctree(app.builder, maxdepth, collapse)
        if not base:
            return compute_toc_tree(toctree, maxdepth, collapse)
        return navigation.get_navigation_tree(
            base, collapse, pagename, app.builder, maxdepth
        )

    return navigation_tree


def compute_hide_toc(context):
    if "toc" not in context:
        return True

    return navigation.side_nav_has_one_item(context["toc"])


def update_context(app, pagename, templatename, context, doctree):
    file_meta = context.get("meta", None) or {}
    context["scylladb_theme_version"] = version
    context["navigation_tree"] = make_navigation_tree(app, pagename)
    context["full_width"] = "full-width" in file_meta
    context["hide_toc"] = compute_hide_toc(context)
    context["hide_pre_content"] = "hide-pre-content" in file_meta
    context["hide_post_content"] = "hide-post-content" in file_meta
    context["hide_version_warning"] = "hide-version-warning" in file_meta
    context["hide_alert"] = "hide-alert" in file_meta
    context["hide_sidebar"] = "hide-sidebar" in file_meta
    context["hide_secondary_sidebar"] = "hide-secondary-sidebar" in file_meta
    context["exclude_doctools"] = "exclude-doctools" in file_meta
    context["landing"] = "landing" in file_meta
    context["llms_txt_enabled"] = getattr(app.config, "llms_txt_enabled", True)

    # TOC depth configuration (min: 2, max: 4)
    default_toc_depth = getattr(app.config, "html_theme_options", {}).get(
        "secondary_sidebar_toc_depth", 2
    )
    page_toc_depth = file_meta.get("toc-depth", default_toc_depth)
    # Clamp between 2 and 4
    context["toc_depth"] = max(2, min(4, int(page_toc_depth)))

    if (
        hasattr(app.config, "smv_rename_latest_version")
        and app.config.smv_rename_latest_version
    ):
        context["rename_latest_version"] = app.config.smv_rename_latest_version


def override_smv_latest_version(config):
    default = "master"
    if hasattr(config, "smv_latest_version") and config.smv_latest_version:
        default = config.smv_latest_version
    config.smv_latest_version = getenv("LATEST_VERSION", default=default)
    return config.smv_latest_version


def override_llms_txt_defaults(config):
    # Use "replace" mode (foo.md) instead of the default "auto" (foo.html.md).
    if getattr(config, "llms_txt_suffix_mode", "auto") == "auto":
        config.llms_txt_suffix_mode = "replace"

    # Default the llms.txt header description to the theme's site_description
    # option so projects don't have to maintain two copies of the same text.
    if not getattr(config, "llms_txt_description", ""):
        theme_options = getattr(config, "html_theme_options", {}) or {}
        site_description = theme_options.get("site_description", "")
        if site_description:
            config.llms_txt_description = site_description

    # Emit absolute URLs in llms.txt sitemaps, including the per-version
    # prefix when sphinx-multiversion is driving the build.
    site_base = base_url(config)
    if site_base and not getattr(config, "markdown_http_base", ""):
        config.markdown_http_base = site_base


def override_rst_epilog(config):
    substitutions = """
.. role:: raw-html(raw)
   :format: html

.. |v| replace:: :raw-html:`<i class="inline-icon icon-check" aria-hidden="true"></i>`
.. |x| replace:: :raw-html:`<i class="inline-icon icon-cancel" aria-hidden="true"></i>`
"""

    epilog = config.rst_epilog or ""
    config.rst_epilog = substitutions + epilog
    return config.rst_epilog


def update_config(app, config):
    override_smv_latest_version(config)
    override_rst_epilog(config)
    override_llms_txt_defaults(config)
    config.sphinx_tabs_disable_css_loading = True


def setup(app):
    """Setup theme"""
    app.add_html_theme("sphinx_scylladb_theme", path.abspath(path.dirname(__file__)))
    app.connect("builder-inited", lambda app: _BASE_TOCTREE_CACHE.clear())
    app.connect("html-page-context", update_context)
    app.connect("config-inited", update_config)

    """Setup lexers"""
    app.add_lexer("cql", cql.CQLLexer)
    app.add_lexer("ditaa", ditaa.DitaaLexer)

    """Setup thid-party extensions"""
    not_found.setup(app)
    mermaid.setup(app)
    sphinx_collapse.setup(app)
    sphinx_copybutton.setup(app)
    sphinx_substitution_extensions.setup(app)
    tabs.setup(app)
    app.setup_extension("sphinx_llm.txt")

    """Setup custom extensions"""
    alerts.setup(app)
    diagram.setup(app)
    hero_box.setup(app)
    grid.setup(app)
    include_tooltip.setup(app)
    labels.setup(app)
    last_updated.setup(app)
    multiversion.setup(app)
    page_anchor.setup(app)
    panel_box.setup(app)
    topic_box.setup(app)
    validations.setup(app)

    return {"version": version, "parallel_read_safe": True}
