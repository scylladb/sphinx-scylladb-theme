from os import path
import sphinx_copybutton
from sphinx_tabs import tabs
from .extensions import panel_box, topic_box, redirects, not_found

def setup(app):
    """Setup theme and custom extensions."""
    app.add_html_theme('sphinx_scylladb_theme', path.abspath(path.dirname(__file__)))
    panel_box.setup(app)
    topic_box.setup(app)
    not_found.setup(app)
    redirects.setup(app)
    sphinx_copybutton.setup(app)
    tabs.setup(app)
