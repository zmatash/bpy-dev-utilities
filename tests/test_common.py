"""Testing common shared functions."""

from collections import Counter

import bpydevutil.common as common
import bpydevutil.install as install


def test_get_addon_sources(fake_addon_dev_env, fake_addon_install_env):
    _, src_dir = fake_addon_dev_env
    install_tool = install.InstallAddonsFromSource(src_dir, fake_addon_install_env)

    assert Counter(
        [path.name for path in common.get_addon_srcs(install_tool.excluded_addons, install_tool.addons_src)]
    ) == Counter(["fake_addon_package", "fake_addon_module.py"])

    install_tool.excluded_addons = ["fake_addon_module.py"]
    assert Counter(
        [
            path.name
            for path in common.get_addon_srcs(install_tool.excluded_addons, install_tool.addons_src)
            if path.name not in install_tool.excluded_addons
        ]
    ) == Counter(["fake_addon_package"])
