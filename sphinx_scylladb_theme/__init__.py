from os import getenv, path

import sphinx_copybutton
from sphinx_tabs import tabs

from sphinx_scylladb_theme._version import version
from sphinx_scylladb_theme.extensions import (
    gh_pages,
    navigation,
    not_found,
    panel_box,
    redirects,
    topic_box,
)
from sphinx_scylladb_theme.lexers import CQLLexer, DitaaLexer


def compute_toc_tree(context):
    if "toctree" in context:
        toctree = context["toctree"]
        toctree_html = toctree(
            collapse=False,
            titles_only=True,
            maxdepth=-1,
            includehidden=True,
        )
    else:
        toctree_html = ""

    toctree_html = navigation.get_navigation_tree(toctree_html)
    return toctree_html


def update_context(app, pagename, templatename, context, doctree):
    context["scylladb_theme_version"] = version
    context["navigation_tree"] = compute_toc_tree(context)


def override_smv_latest_version(config):
    default = "master"
    if hasattr(config, "smv_latest_version") and config.smv_latest_version:
        default = config.smv_latest_version
    config.smv_latest_version = getenv("LATEST_VERSION", default=default)
    return config.smv_latest_version


def override_rst_prolog(config):
    substitutions = """
    .. |v| raw:: html

        <i class="inline-icon fa fa-check" aria-hidden="true"></i>

    .. |x| raw:: html

        <i class="inline-icon fa fa-times" aria-hidden="true"></i>
    """
    rst_prolog = config.rst_prolog or ""
    config.rst_prolog = substitutions + rst_prolog
    return config.rst_prolog


def update_config(app, config):
    override_smv_latest_version(config)
    override_rst_prolog(config)
    config.sphinx_tabs_disable_css_loading = True


def setup(app):
    """Setup theme"""
    app.add_html_theme("sphinx_scylladb_theme", path.abspath(path.dirname(__file__)))
    app.connect("html-page-context", update_context)
    app.connect("config-inited", update_config)

    """Setup lexers"""
    app.add_lexer("cql", CQLLexer())
    app.add_lexer("ditaa", DitaaLexer())

    """Setup custom extensions"""
    gh_pages.setup(app)
    not_found.setup(app)
    panel_box.setup(app)
    redirects.setup(app)
    sphinx_copybutton.setup(app)
    from .extensions import substitutions

    substitutions.setup(app)
    tabs.setup(app)
    topic_box.setup(app)

    return {"version": version, "parallel_read_safe": True}
