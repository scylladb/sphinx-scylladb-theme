import os
from .utils import copy

def add_gh_pages_support(app, exception):   
    """
    Copies CNAME and .nojekyll files into the root output dir.
    """ 
    is_multiversion = os.getenv("SPHINX_MULTIVERSION_NAME") is not None
    out_dir = app.builder.outdir
    head, tail = os.path.split(out_dir)

    if is_multiversion:
        copy(out_dir + '/CNAME', head + '/CNAME')
        copy(out_dir + '/.nojekyll', head + '/.nojekyll')

def setup(app):
    """
    Add GitHub pages support for multiversion.
    """
    app.connect('build-finished', add_gh_pages_support)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
