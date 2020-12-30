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
        return 'None'
    elif len(versions) == 1 and versions[0] == '*':
        return r'^.*'
    elif len(versions) == 1:
        return r'^' + versions[0] + r'$'
    else:
        return r'\b(' + '|'.join(versions) + r')\b'
