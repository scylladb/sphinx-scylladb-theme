from os import path, getenv
import sphinx_copybutton
from sphinx_tabs import tabs
from .extensions import panel_box, topic_box, redirects, not_found, substitutions

def setup(app):
    """Setup theme"""
    app.add_html_theme('sphinx_scylladb_theme', path.abspath(path.dirname(__file__)))
    app.config.smv_latest_version = getenv('LATEST_VERSION', default='master')
    """Setup custom extensions"""
    panel_box.setup(app)
    topic_box.setup(app)
    substitutions.setup(app)
    not_found.setup(app)
    redirects.setup(app)
    sphinx_copybutton.setup(app)
    tabs.setup(app)
