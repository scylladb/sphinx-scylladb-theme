from sphinx_scylladb_theme.utils import multiversion_regex_builder


def test_multiversion_regex_builder_empty():
    versions = []
    assert multiversion_regex_builder(versions) == 'None'

def test_multiversion_regex_builder_all():
    versions = ['*']
    assert multiversion_regex_builder(versions) == '^.*'
    
def test_multiversion_regex_builder_one_version():
    versions = ['1.0']
    assert multiversion_regex_builder(versions) == r'^1.0$'

def test_multiversion_regex_builder_many_version():
    versions = ['1.0', '2.0']
    assert multiversion_regex_builder(versions) == r'\b(1.0|2.0)\b'

