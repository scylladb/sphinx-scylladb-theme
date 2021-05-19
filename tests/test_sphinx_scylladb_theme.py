import os
from sphinx_scylladb_theme import version, override_smv_latest_version, override_rst_prolog

class ConfigStub:

    def __init__(self):
        self.smv_latest_version = ''
        self.rst_prolog = ''

def test_override_smv_latest_version_default():
    config = ConfigStub()
    assert override_smv_latest_version(config) == 'master'

def test_override_smv_latest_version_env():
    config = ConfigStub()
    os.environ["LATEST_VERSION"] = "abc"
    assert override_smv_latest_version(config) == 'abc'

def test_override_rst_prolog():
    config = ConfigStub()
    config.rst_prolog = '|a| raw:: html'
    assert '|v| raw:: html' in override_rst_prolog(config)
    assert '|a| raw:: html' in override_rst_prolog(config)
