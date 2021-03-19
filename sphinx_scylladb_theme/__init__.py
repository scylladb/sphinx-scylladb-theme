from os import path, getenv

import sphinx_copybutton
import sphinx_last_updated_by_git
from sphinx_tabs import tabs
from navigation_icons import extension as navigation_icons

from sphinx_scylladb_theme._version import version
from sphinx_scylladb_theme.lexers import CQLLexer, DitaaLexer
from sphinx_scylladb_theme.extensions import panel_box, topic_box, redirects, not_found, gh_pages


def update_context(app, pagename, templatename, context, doctree):
    context["scylladb_theme_version"] = version

def update_config(app, config):
    default = 'master'
    if hasattr(config, 'smv_latest_version') and config.smv_latest_version:
        default = config.smv_latest_version
    config.smv_latest_version = getenv('LATEST_VERSION', default=default)

def setup(app):
    """Setup theme"""
    app.add_html_theme('sphinx_scylladb_theme', path.abspath(path.dirname(__file__)))
    app.connect("html-page-context", update_context)
    app.connect('config-inited', update_config)

    """Setup lexers"""
    app.add_lexer("cql", CQLLexer())
    app.add_lexer("ditaa", DitaaLexer())

    """Setup custom extensions"""
    gh_pages.setup(app)
    navigation_icons.setup(app)
    not_found.setup(app)
    panel_box.setup(app)
    redirects.setup(app)
    sphinx_copybutton.setup(app)
    sphinx_last_updated_by_git.setup(app)
    from .extensions import substitutions
    substitutions.setup(app)
    tabs.setup(app)
    topic_box.setup(app)

    return {"version": version, "parallel_read_safe": True}
