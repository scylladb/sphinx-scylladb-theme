from os import path, getenv
import sphinx_copybutton
from sphinx_tabs import tabs
from sphinx_scylladb_theme.extensions import panel_box, topic_box, redirects, not_found, gh_pages
from sphinx_scylladb_theme._version import version

def update_context(app, pagename, templatename, context, doctree):
    context["scylladb_theme_version"] = version

def override_smv_latest_version(config):
    default = 'master'
    if hasattr(config, 'smv_latest_version') and config.smv_latest_version:
        default = config.smv_latest_version
    config.smv_latest_version = getenv('LATEST_VERSION', default=default)
    return config.smv_latest_version

def override_rst_prolog(config):
    substitutions = """
    .. |v| raw:: html
        
        <i class="inline-icon fa fa-check" aria-hidden="true"></i>

    .. |x| raw:: html
        
        <i class="inline-icon fa fa-times" aria-hidden="true"></i>
    """
    rst_prolog = config.rst_prolog or ''
    config.rst_prolog = substitutions + rst_prolog
    return config.rst_prolog

def update_config(app, config):
    override_smv_latest_version(config)
    override_rst_prolog(config)

def setup(app):
    """Setup theme"""
    app.add_html_theme('sphinx_scylladb_theme', path.abspath(path.dirname(__file__)))
    app.connect("html-page-context", update_context)
    app.connect('config-inited', update_config)

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
