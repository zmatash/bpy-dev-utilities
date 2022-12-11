"""Pytest resources."""

from pathlib import Path

import pytest


def example_module(root_path: Path, module_name: str, write: bool, extension: str = ".py") -> Path:
    """Create example python module to run tests on.

    Args:
        root_path: Path to create the module.
        module_name: Name of the module.
        write: Write information to module or leave blank.
        extension: File extension.

    Returns:
        Path to the module.
    """
    module = Path(root_path) / f"{module_name}{extension}"
    module.touch()

    if write:
        module.write_text(f'bl_info = {{"name": "{module.name}", "version": (0, 5, 0), "blender": (2, 93, 0)}}')
    else:
        module.touch()

    return module


def example_package(root_path: Path, package_name: str, write: bool) -> Path:
    """Create example python package to run tests on.

    Args:
        root_path: Path to create the package.
        package_name: Name of the package.
        write: Write information to init file or leave blank.

    Returns:
        Path to the package.
    """
    package = Path(root_path / package_name)
    package.mkdir()

    init = package / "__init__.py"
    sub_folder = package / "sub_folder"
    sub_folder.mkdir()

    for file_type in (".py", ".txt", ".tmp", ".pyc"):
        Path(sub_folder / f"dummy_file{file_type}").touch()

    if write:
        init.write_text(f'bl_info = {{"name": "{package.name}", "version": (0, 2, 5), "blender": (2, 93, 0)}}')
    else:
        init.touch()

    return package


@pytest.fixture(scope="session")
def temp_projects_dir(tmp_path_factory) -> tuple[Path, dict[str, bool], dict[str, bool]]:
    """Create temporary mock project folder structure.

    Returns:
        The root path of the project directory.
        The dictionaries used to populate it.
    """

    root_dir = tmp_path_factory.mktemp("test-projects")
    src_dir = root_dir / "src"
    src_dir.mkdir()

    output_dir = root_dir / "output"
    output_dir.mkdir()

    modules_dict = {"valid_module": True, "valid_module_2": True, "invalid_module": False}
    packages_dict = {"valid_package": True, "valid_package_2": True, "invalid_package": False}

    for k, v in modules_dict.items():
        example_module(root_dir / "src", k, v)

    for k, v in packages_dict.items():
        example_package(root_dir / "src", k, v)

    return root_dir, modules_dict, packages_dict


@pytest.fixture(scope="session")
def temp_addons_dir(tmp_path_factory) -> tuple[Path, dict[str, bool], dict[str, bool]]:
    """Create temporary mock installation folder structure.

    Returns:
        The root path of the installation directory.
        The dictionaries used to populate it.
    """

    root_dir = tmp_path_factory.mktemp("install-location")
    root_dir.mkdir(exist_ok=True)

    modules_dict = {"existing_module": True}
    packages_dict = {"existing_package": True}

    for k, v in modules_dict.items():
        example_module(root_dir, k, v)

    for k, v in packages_dict.items():
        example_package(root_dir, k, v)

    return root_dir, modules_dict, packages_dict
