from pathlib import Path

import pytest


def create_fake_module(root_path: Path, module_name: str, write: bool) -> None:
    module = Path(root_path / f"{module_name}.py")

    if write:
        module.write_text('bl_info = {"name": "Fake Addon File", "version": (0, 5, 0), "blender": (2, 93, 0)}')
    else:
        module.touch()


def create_fake_package(root_path: Path, package_name: str, write: bool) -> None:

    package = Path(root_path / package_name)
    package.mkdir()

    init = Path(package / "__init__.py")

    sub_folder = Path(package / "sub_folder")
    sub_folder.mkdir()

    if write:
        init.write_text('bl_info = {"name": "Fake Addon", "version": (0, 2, 5), "blender": (2, 93, 0)}')
    else:
        init.touch()


@pytest.fixture(scope="module")
def fake_addon_install_env(tmp_path_factory) -> Path:
    addons_dir = tmp_path_factory.mktemp("addons_dir")
    create_fake_module(addons_dir, "example_addon", False)
    create_fake_module(addons_dir, "fake_addon_module", True)
    create_fake_package(addons_dir, "fake_addon_package", True)

    return addons_dir


@pytest.fixture(scope="module")
def fake_addon_dev_env(tmp_path_factory) -> tuple[Path, Path]:
    root = tmp_path_factory.mktemp("project_root")
    src_dir = root / "src"
    src_dir.mkdir()

    create_fake_module(src_dir, "fake_addon_module", True)
    create_fake_package(src_dir, "fake_addon_package", True)
    create_fake_package(src_dir, "fake_addon_package_no_write", False)

    return root, src_dir
