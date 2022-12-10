"""Common functions used by multiple functions."""
import shutil
import subprocess
from pathlib import Path
from typing import Optional

import typer
from rich import print


def load_blender(blender_exe: str, addons: list[str] = None) -> bytes:
    """Load Blender and automatically enable addons.

    Args:
        blender_exe: Path to blender.exe.
        addons: List of blender addon module names.

    Returns:
        The output of the blender subprocess.

    """

    def build_expression():
        """Build the expression needed to enable all addons from the command line."""

        expression = "import bpy; "

        if addons:
            for addon in addons:
                enable_addon = f"bpy.ops.preferences.addon_enable(module='{addon}')"
                expression = f"{expression}{enable_addon}"

        return expression

    cmd = f"{blender_exe} --python-expr '{build_expression()}'"
    blender = subprocess.Popen(cmd)
    blender = blender.communicate()

    return blender[0]


def clear_old_addon(addon_dir: Path, name: str) -> None:
    """

    Args:
        addon_dir: Path to the directory to search for the old addon
        name: Name of the addon to search for.

    """

    addon_path = Path(addon_dir / name)

    if not addon_path.exists():
        return

    if addon_path.is_dir():
        if addon_path.is_symlink():
            addon_path.rmdir()
        else:
            shutil.rmtree(addon_path)
    else:
        addon_path.unlink()


def clear_unused_files(addon: Path, rm_suffixes: set[str] = None) -> None:
    """Garbage cleaning source files. eg .pyc files.

    Args:
        addon: Addon path to garbage clean.
        rm_suffixes: Delete files using these suffixes.
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

    print(f"[green]Garbage Cleaning:[/green] {file_count} files removed.")


def get_addon_srcs(addons_src: Path, excluded_addons: Optional[list[str]] = None) -> list[Path]:
    """Get a list of addon source paths that need to be installed.

    Args:
        addons_src: Path of the directory where addon sources are located.
        excluded_addons: List of addon names to be excluded from the process.

    Returns:
        The paths of the addons to be installed.

    """

    def is_python(path: Path) -> bool:
        """Check the given path is either a python module or package.

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
