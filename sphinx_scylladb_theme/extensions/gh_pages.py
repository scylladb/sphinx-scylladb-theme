"""
Sphinx extension that adds GitHub Pages support for sphinx-multiversion.
"""

import os
from .utils import copy

def add_gh_pages_support(app, exception):   
    """
    Copies CNAME and .nojekyll files in the root of the output directory.
    
    :param app: Sphinx Application
    :type app: sphinx.application.Sphinx

    :param exception: Sphinx Error
    :type exception: sphinx.error.SphinxError
    """ 
    is_multiversion = os.getenv("SPHINX_MULTIVERSION_NAME") is not None
    out_dir = app.builder.outdir
    head, tail = os.path.split(out_dir)

    if is_multiversion:
        copy(out_dir + '/CNAME', head + '/CNAME')
        copy(out_dir + '/.nojekyll', head + '/.nojekyll')

def setup(app):
    app.connect('build-finished', add_gh_pages_support)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
