"""Test finding addon sources."""

from bpydevutil.functions import common


def test_get_addon_srcs(temp_projects_dir):
    root_dir, modules, packages = temp_projects_dir

    addon_paths = common.get_addon_srcs(root_dir / "src")
    addon_names = [path.stem for path in addon_paths]

    for module, is_valid in modules.items():
        if is_valid:
            assert module in addon_names
        else:
            assert module not in addon_names

    for package, is_valid in packages.items():
        if is_valid:
            assert package in addon_names
        else:
            assert package not in addon_names
