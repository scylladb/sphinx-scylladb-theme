from os import path, getenv
import sphinx_copybutton
from sphinx_tabs import tabs
from sphinx_scylladb_theme.extensions import panel_box, topic_box, redirects, not_found, gh_pages
from sphinx_scylladb_theme._version import version

def update_context(app, pagename, templatename, context, doctree):
    context["scylladb_theme_version"] = version

def setup(app):
    """Setup theme"""
    app.add_html_theme('sphinx_scylladb_theme', path.abspath(path.dirname(__file__)))
    app.connect("html-page-context", update_context)
    app.config.smv_latest_version = getenv('LATEST_VERSION', default='master')
    """Setup custom extensions"""
    panel_box.setup(app)
    topic_box.setup(app)
    from .extensions import substitutions
    substitutions.setup(app)
    not_found.setup(app)
    redirects.setup(app)
    sphinx_copybutton.setup(app)
    tabs.setup(app)
    gh_pages.setup(app)
    return {"version": version, "parallel_read_safe": True}
