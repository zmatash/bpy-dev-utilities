"""Common functions used by multiple functions."""
import shutil
import subprocess
from pathlib import Path
from typing import Any, Optional, Union

import tomli
import typer
from rich import print


def load_blender(blender_exe: str, addons: list[str] = None) -> None:
    """Load Blender and automatically enable addons.

    Args:
        blender_exe: Path to blender.exe.
        addons: List of blender addon module names.
    """

    def build_expression():
        """Build the expression needed to enable all addons from the command line."""

        expression = "import bpy; "

        if addons:
            for addon in addons:
                expression += f"bpy.ops.preferences.addon_enable(module='{addon}'); "

        return expression

    cmd = f'{blender_exe} --background --python-expr "{build_expression()}"'
    blender = subprocess.Popen(cmd)
    blender.communicate()


def clear_old_addon(addon_dir: Path, name: str) -> None:
    """Clear old files from the addon directory.

    Args:
        addon_dir: Path to the directory to search for the old addon
        name: Name of the addon to search for.
    """

    addon_path = addon_dir / name

    if not addon_path.exists():
        if Path(addon_path).with_suffix(".py").exists():
            addon_path = addon_path.with_suffix(".py")

    if addon_path.is_dir():
        if addon_path.is_symlink():
            addon_path.rmdir()
        else:
            shutil.rmtree(addon_path)
    else:
        addon_path.unlink()


def clear_unused_files(addon: Path, rm_suffixes: set[str] = None) -> int:
    """
    Garbage cleaning source files.
    Removes the __pycache__ folder
    and any other user configured file types.

    Args:
        addon: Addon path to garbage clean.
        rm_suffixes: suffixes to search for (include '.').

    Returns
        Number of files deleted.
    """
    if rm_suffixes is None:
        rm_suffixes = {".pyc"}

    file_count = 0
    for path in addon.rglob("*"):
        if path.is_dir() and path.name == "__pycache__":
            shutil.rmtree(path)
            file_count += 1
        elif path.suffix in rm_suffixes:
            path.unlink()
            file_count += 1

    return file_count


def get_addon_srcs(addons_src: Path, excluded_addons: Optional[list[str]] = None) -> list[Path]:
    """Get a list of addon source paths that need to be installed.

    Args:
        addons_src: Path of the directory where addon sources are located.
        excluded_addons: List of addon names to be excluded from the process.

    Returns:
        The paths of the addons to be installed.
    """

    def is_python(path: Path) -> bool:
        """
        Check the given path is either a python module or package.
        Check that it contains bl_info.

        Args:
            path: The path to check.

        Returns:
            True if "path" is a python module or package.
        """
        if path.is_dir() and Path(path / "__init__.py").exists():
            if "bl_info" in Path(path / "__init__.py").read_text():
                return True

        if path.is_file() and path.suffix == ".py":
            if "bl_info" in path.read_text():
                return True

        print(f"[italic]Skipping <{path.name}>, no [yellow]bl_info[/yellow] found.[/italic]")

    if excluded_addons:
        addon_srcs = [path for path in addons_src.iterdir() if path.name not in excluded_addons and is_python(path)]
    else:
        addon_srcs = [path for path in addons_src.iterdir() if is_python(path)]

    if not addon_srcs:
        print(f"[red]There are no addon sources inside the directory [{addons_src}][/red]")
        raise typer.Abort()

    return addon_srcs


def check_directories(directory_params: dict[str, str]) -> bool:
    """Check that user specified directories exist.

    Args:
        directory_params: Dictionary of parameters and corresponding values.

    Returns
        True if all tests are passed.
    """
    for param in directory_params.keys():
        if not directory_params[param]:
            raise typer.BadParameter(f"<{param}> cannot be empty.")

        if not Path(directory_params[param]).is_dir():
            raise typer.BadParameter(f"<{param}> <{directory_params[param]}> is not an existing directory.")

    return True


def parse_toml(toml_path: Path, param_key: str) -> Any:
    """Get value from toml file using a key.

    Args:
        toml_path: Path to the toml file.
        param_key: The key to the parameter value.

    Returns:
        Parameter value or none if key does not exist.
    """
    with open(toml_path, "rb") as f:
        toml_dict = tomli.load(f)
        try:
            return toml_dict["tool"]["bpydevutil"][param_key]
        except KeyError:
            return None


def get_toml() -> Union[Path, None]:
    """Search for the project toml file in the working directory.

    Returns:
        Path to the toml file if it exists, None if not.
    """
    pyproject = Path.cwd() / "pyproject.toml"
    if pyproject.exists():
        return pyproject
    else:
        return None
