import os
import shutil
from notfound import extension

def force_link(src, dest):
    if os.path.isfile(dest) or os.path.islink(dest):
        os.remove(dest)
    elif os.path.isdir(dest):
        shutil.rmtree(dest)
    try:
        shutil.copytree(src, dest)
    except:
        shutil.copy(src, dest)

def add_404_page(app, docname):    
    is_dirhtml = app.builder.name == 'dirhtml'
    is_multiversion = os.getenv("SPHINX_MULTIVERSION_NAME") is not None
    out_dir = app.builder.outdir
    head, tail = os.path.split(out_dir)

    if is_dirhtml and os.path.exists(out_dir + '/404'):
        force_link(out_dir + '/404/index.html', out_dir + '/404.html')
    elif is_multiversion:
        force_link(out_dir + '/404.html', head + '/404.html')
        force_link(out_dir + '/_static', head + '/_static')


def setup(app):
    extension.setup(app)
    app.connect('build-finished', add_404_page)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
