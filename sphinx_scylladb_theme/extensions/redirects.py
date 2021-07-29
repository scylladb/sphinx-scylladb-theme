"""
Sphinx extension for generating JavaScript-driven redirects for moved pages.
"""

import os

import yaml

from .utils import build_redirect_body, is_url


def create_redirects(app, exception):
    """
    Creates redirections for all the paths listed in the ``redirects_file`` defined in ``conf.py``.

    The file should contain a dictionary of redirections formatted as:

    >>> old path: new path

    :param app: Sphinx Application
    :type app: sphinx.application.Sphinx

    :param exception: Sphinx Error
    :type exception: sphinx.error.SphinxError
    """
    redirects_file = app.config.redirects_file
    is_multiversion = os.getenv("SPHINX_MULTIVERSION_NAME")
    if not redirects_file:
        return
    if os.path.exists("docs"):
        redirects_file = "docs/" + redirects_file
    if not os.path.exists(redirects_file):
        return

    with open(redirects_file, "r") as yaml_file:
        full_load = yaml.full_load(yaml_file)
        if full_load:
            for from_path, redirect_to in full_load.items():
                target_path = app.outdir + "/" + from_path

                # Handles sphinx-multiversion redirects
                if is_multiversion and not is_url(redirect_to):
                    redirect_to = (
                        app.config.html_baseurl
                        + "/"
                        + os.environ["SPHINX_MULTIVERSION_NAME"]
                        + redirect_to
                    )

                if app.builder.name == "dirhtml":
                    target_path = target_path + "/index.html"
                else:
                    target_path = target_path + ".html"

                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                with open(os.path.join(target_path), "w+") as t_file:
                    t_file.write(build_redirect_body(redirect_to))


def setup(app):
    app.add_config_value("redirects_file", "", "html")
    app.connect("build-finished", create_redirects)

    return {
        "version": "0.3",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
