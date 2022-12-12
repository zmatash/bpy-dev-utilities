"""Test clearing of old addon files."""

from pathlib import Path

from bpydevutil.functions import common_funcs


def test_clear_old_addon(temp_addons_dir):
    root_dir, modules, packages = temp_addons_dir

    for module in modules.keys():
        assert Path(root_dir / f"{module}.py").exists()
        common_funcs.clear_old_addon(root_dir, module)
        assert not Path(root_dir / f"{module}.py").exists()

    for package in packages.keys():
        assert Path(root_dir / package).exists()
        common_funcs.clear_old_addon(root_dir, package)
        assert not Path(root_dir / package).exists()
