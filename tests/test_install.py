"""Unit testing the addon install tool."""

from collections import Counter

import bpydevutil.install as install


class TestInstallClass:
    def test_get_addon_sources(self, fake_addon_dev_env, fake_addon_install_env):

        _, src_dir = fake_addon_dev_env
        install_tool = install.InstallAddonsFromSource(src_dir, fake_addon_install_env)

        assert Counter([path.name for path in install_tool.get_addon_srcs()]) == Counter(
            ["fake_addon_package", "fake_addon_module.py"]
        )

        install_tool.excluded_addons = ["fake_addon_module.py"]
        assert Counter(
            [path.name for path in install_tool.get_addon_srcs() if path.name not in install_tool.excluded_addons]
        ) == Counter(["fake_addon_package"])

    def test_clear_old_addons(self, fake_addon_dev_env, fake_addon_install_env):
        delete_addons = ["fake_addon_module.py", "fake_addon_package"]

        _, src_dir = fake_addon_dev_env
        install_tool = install.InstallAddonsFromSource(src_dir, fake_addon_install_env)

        install_tool.clear_old_addons(delete_addons)

        not_deleted = [path.name for path in fake_addon_install_env.iterdir()]

        assert not any(name in delete_addons for name in not_deleted)

    def test_install_from_source(self):
        assert False
