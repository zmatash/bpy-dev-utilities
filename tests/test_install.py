"""Testing the addon install tool."""

from pathlib import Path

import pytest

import bpydevutil.functions.install as install


@pytest.mark.order(2)
class TestInstallClass:

    def test_clear_old_addons(self, fake_addon_dev_env, fake_addon_install_env):
        delete_addons = ["fake_addon_module.py", "fake_addon_package"]

        _, src_dir = fake_addon_dev_env
        install_tool = install.InstallAddonsFromSource(src_dir, fake_addon_install_env)

        install_tool.clear_old_addons(delete_addons)

        not_deleted = [path.name for path in fake_addon_install_env.iterdir()]

        assert not any(name in not_deleted for name in delete_addons)

    def test_install_addons(self, fake_addon_dev_env, fake_addon_install_env):
        install_addons = ["fake_addon_module.py", "fake_addon_package"]

        _, src_dir = fake_addon_dev_env
        install_tool = install.InstallAddonsFromSource(src_dir, fake_addon_install_env)

        install_tool.install_addons([Path(src_dir / name) for name in install_addons])

        assert all(name in [path.name for path in fake_addon_install_env.iterdir()] for name in install_addons)
