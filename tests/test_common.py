"""Testing common shared functions."""

from collections import Counter
from pathlib import Path

import pytest

import bpydevutil.functions.common as common


@pytest.mark.order(1)
def test_get_addon_sources(fake_addon_dev_env, fake_addon_install_env):
    _, src_dir = fake_addon_dev_env

    assert Counter([path.name for path in common.get_addon_srcs(src_dir)]) == Counter(
        ["fake_addon_package", "fake_addon_module.py"]
    )

    assert Counter(
        [
            path.name
            for path in common.get_addon_srcs(src_dir, ["fake_addon_module.py"])
            if path.name not in ["fake_addon_module.py"]
        ]
    ) == Counter(["fake_addon_package"])


@pytest.mark.parametrize("addon_name", ["fake_addon_module.py", "fake_addon_package"])
@pytest.mark.order(2)
def test_clear_old_addon(fake_addon_install_env, addon_name):

    common.clear_old_addon(fake_addon_install_env, addon_name)

    assert not Path(fake_addon_install_env / addon_name).exists()


@pytest.mark.order(3)
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
