import os

from sphinx_scylladb_theme import (
    LLMS_TXT_HUB_URL,
    add_llms_txt_hub_link,
    override_rst_epilog,
    override_smv_latest_version,
)


class ConfigStub:
    def __init__(self):
        self.smv_latest_version = ""
        self.rst_epilog = ""
        self.project = "ScyllaDB Manager"
        self.llms_txt_description = ""
        self.html_theme_options = {}


def test_override_smv_latest_version_default():
    config = ConfigStub()
    assert override_smv_latest_version(config) == "master"


def test_override_smv_latest_version_env():
    config = ConfigStub()
    os.environ["LATEST_VERSION"] = "abc"
    assert override_smv_latest_version(config) == "abc"


def test_override_rst_epilog():
    config = ConfigStub()
    config.rst_epilog = "|a| raw:: html"
    assert "|v| replace:: :raw-html:" in override_rst_epilog(config)
    assert "|x| replace:: :raw-html:" in override_rst_epilog(config)


def test_add_llms_txt_hub_link_appends_to_description():
    config = ConfigStub()
    config.llms_txt_description = "Automate repair and backup."
    description = add_llms_txt_hub_link(config)
    assert description.startswith("Automate repair and backup.\n")
    assert description.endswith(LLMS_TXT_HUB_URL)


def test_add_llms_txt_hub_link_without_description():
    config = ConfigStub()
    description = add_llms_txt_hub_link(config)
    assert description.startswith("ScyllaDB Manager documentation\n")
    assert description.endswith(LLMS_TXT_HUB_URL)


def test_add_llms_txt_hub_link_custom_url():
    config = ConfigStub()
    config.html_theme_options = {"llms_txt_hub_url": "https://example.com/llms.txt"}
    assert add_llms_txt_hub_link(config).endswith("https://example.com/llms.txt")


def test_add_llms_txt_hub_link_disabled():
    config = ConfigStub()
    config.llms_txt_description = "Automate repair and backup."
    config.html_theme_options = {"llms_txt_hub_url": ""}
    assert add_llms_txt_hub_link(config) == "Automate repair and backup."
    assert config.llms_txt_description == "Automate repair and backup."
