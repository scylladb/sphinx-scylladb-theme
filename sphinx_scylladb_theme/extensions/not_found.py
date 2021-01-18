"""
Sphinx extension that adds sphinx-notfound-page support for sphinx-multiversion.
"""
import os
from notfound import extension
from .utils import copy


def create_not_found_page(app, exception):
    """
    Creates a 404.html in the root of the output directory.
    
    :param app: Sphinx Application
    :type app: sphinx.application.Sphinx

    :param exception: Sphinx Error
    :type exception: sphinx.error.SphinxError
    """
    is_dirhtml = app.builder.name == 'dirhtml'
    is_multiversion = os.getenv("SPHINX_MULTIVERSION_NAME") is not None
    out_dir = app.builder.outdir
    head, tail = os.path.split(out_dir)

    if is_dirhtml and os.path.exists(out_dir + '/404'):
        copy(out_dir + '/404/index.html', out_dir + '/404.html')
    elif is_multiversion:
        copy(out_dir + '/404.html', head + '/404.html')
        copy(out_dir + '/_static', head + '/_static')


def setup(app):
    extension.setup(app)
    app.connect('build-finished', create_not_found_page)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
