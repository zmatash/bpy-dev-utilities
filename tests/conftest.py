from pathlib import Path

import pytest


def create_fake_module(root_path: Path, module_name: str, write: bool, extension: str = ".py") -> None:
    module = Path(root_path / f"{module_name}{extension}")

    if write:
        module.write_text('bl_info = {"name": "Fake Addon File", "version": (0, 5, 0), "blender": (2, 93, 0)}')
    else:
        module.touch()


def create_fake_package(root_path: Path, package_name: str, write: bool) -> Path:

    package = Path(root_path / package_name)
    package.mkdir()

    init = Path(package / "__init__.py")

    sub_folder = Path(package / "sub_folder")
    sub_folder.mkdir()

    if write:
        init.write_text('bl_info = {"name": "Fake Addon", "version": (0, 2, 5), "blender": (2, 93, 0)}')
    else:
        init.touch()

    return package


@pytest.fixture(scope="session")
def fake_addon_install_env(tmp_path_factory) -> Path:
    addons_dir = tmp_path_factory.mktemp("addons_dir")
    create_fake_module(addons_dir, "example_addon", False)
    create_fake_module(addons_dir, "fake_addon_module", True)
    create_fake_package(addons_dir, "fake_addon_package", True)

    return addons_dir


@pytest.fixture(scope="session")
def fake_addon_dev_env(tmp_path_factory) -> tuple[Path, Path]:
    root = tmp_path_factory.mktemp("project_root")
    src_dir = root / "src"
    src_dir.mkdir()

    create_fake_module(src_dir, "fake_addon_module", True)

    path = create_fake_package(src_dir, "fake_addon_package", True)
    create_fake_package(path, "__pycache__", False)
    create_fake_module(path, "dummy_file", False, ".dummy")

    create_fake_package(src_dir, "fake_addon_package_no_write", False)

    return root, src_dir


def config_strings():
    """Formatting the strings to write the test ini file.

    Returns:
        Formatting string to write to the config file.

    """

    header = "[tool.bpydevutil]"
    src_dir = f'src_dir = "ExamplePath"'
    excluded_addons = f'excluded-addons = ["addon1", "addon2", "addon3"]'

    return f"{header}\n{src_dir}\n{excluded_addons}"


@pytest.fixture(scope="session")
def example_config(tmp_path_factory):
    config_dir = tmp_path_factory.mktemp("test_config_root")
    config = Path(config_dir / "pryproject.toml")
    config.write_text(config_strings())

    return config_dir, config
