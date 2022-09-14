"""Test the parsing of the ini config file."""

import pytest

import bpydevutil.main as main


@pytest.mark.order(4)
class TestConfigParsing:
    def test_get_cfg_arg(self, example_config):
        _, config_path = example_config

        assert main.parse_toml(config_path, "src_dir") == "ExamplePath"
        assert main.parse_toml(config_path, "excluded-addons") == ["addon1", "addon2", "addon3"]
