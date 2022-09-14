"""Testing the addon install tool."""

from pathlib import Path

import pytest

import bpydevutil.functions.install as install


@pytest.mark.order(2)
class TestInstallClass:
    @pytest.mark.parametrize("addon_name", ["fake_addon_module.py", "fake_addon_package"])
    def test_install_addons(self, fake_addon_dev_env, fake_addon_install_env, addon_name):
        _, src_dir = fake_addon_dev_env
        install_tool = install.InstallAddonsFromSource(fake_addon_install_env)

        install_tool.install_addon(Path(src_dir / addon_name))

        assert Path(fake_addon_install_env / addon_name).exists()
