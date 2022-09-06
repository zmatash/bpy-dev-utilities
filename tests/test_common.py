"""Testing common shared functions."""

from collections import Counter
from pathlib import Path

import pytest

import bpydevutil.common as common
import bpydevutil.install as install


@pytest.mark.order(1)
def test_get_addon_sources(fake_addon_dev_env, fake_addon_install_env):
    _, src_dir = fake_addon_dev_env
    install_tool = install.InstallAddonsFromSource(src_dir, fake_addon_install_env)

    assert Counter(
        [path.name for path in common.get_addon_srcs(install_tool.addons_src, install_tool.excluded_addons)]
    ) == Counter(["fake_addon_package", "fake_addon_module.py"])

    install_tool.excluded_addons = ["fake_addon_module.py"]
    assert Counter(
        [
            path.name
            for path in common.get_addon_srcs(install_tool.addons_src, install_tool.excluded_addons)
            if path.name not in install_tool.excluded_addons
        ]
    ) == Counter(["fake_addon_package"])


def test_clear_unused_files(fake_addon_dev_env):
    _, src_dir = fake_addon_dev_env

    assert (
        Path(src_dir / "fake_addon_package" / "dummy_file.dummy").exists()
        and Path(src_dir / "fake_addon_package" / "__pycache__").exists()
    )

    common.clear_unused_files(Path(src_dir / "fake_addon_package"), {".dummy"})

    assert (
        not Path(src_dir / "fake_addon_package" / "dummy_file.dummy").exists()
        and not Path(src_dir / "fake_addon_package" / "__pycache__").exists()
    )
