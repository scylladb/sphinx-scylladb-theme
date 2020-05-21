from os import path
from .extensions import panel_box, topic_box

def setup(app):
    """Setup theme and custom extensions."""
    app.add_html_theme('sphinx_scylladb_theme', path.abspath(path.dirname(__file__)))

    panel_box.setup(app)
    topic_box.setup(app)
