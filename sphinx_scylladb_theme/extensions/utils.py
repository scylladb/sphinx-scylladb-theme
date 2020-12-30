import os
import shutil

def generate_template(template, **vars):
    return template.format(**vars)

def generate_styles(**styles):
    return ''.join(['{}:{};'.format(k, v) for k, v in styles.items() if v])

def generate_content(*lines, line_break='\n'):
    return line_break.join([line for line in lines])

def copy(src, dest):
    if os.path.isfile(dest) or os.path.islink(dest):
        os.remove(dest)
    elif os.path.isdir(dest):
        shutil.rmtree(dest)
    if os.path.exists(src):
        try:
            shutil.copytree(src, dest)
        except:
            shutil.copy(src, dest)
