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

def multiversion_regex_builder(versions):
    """Generates a regex string from a list of versions.
    
    Every documentation project `conf.py` file uses this function
    to define the different documentation versions supported.

    Args:
        versions (:obj:`list` of :obj:`str`): A list of versions.

    Returns:
        str: The equivalent regular expression.
    """

    if len(versions) == 0:
        return ''
    elif len(versions) == 1 and versions[0] == '*':
        return r'^.*'
    elif len(versions) == 1:
        return r'^' + versions[0] + r'$'
    else:
        return r'\b(' + '|'.join(versions) + r')\b'
