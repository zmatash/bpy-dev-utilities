"""Test the parsing of the ini config file."""

import iniconfig
import pytest

import bpydevutil.main as main


@pytest.mark.order(5)
class TestConfigParsing:
    def test_get_cfg_arg(self, example_config):
        _, config_path = example_config
        config = iniconfig.IniConfig(str(config_path))

        assert main.get_cfg_arg(config, "src_dir") == "ExamplePath"
        assert main.get_cfg_arg(config, "blender_addons_dir") == "ExamplePath2"

        assert main.get_cfg_arg(config, "no_arg") is None

    def test_parse_cfg_list(self, example_config):
        _, config_path = example_config
        config = iniconfig.IniConfig(str(config_path))

        assert main.parse_cfg_list(main.get_cfg_arg(config, "excluded_addons")) == ["addon1", "addon2", "addon3"]
