"""Common functions used by multiple tools."""
from pathlib import Path

import typer
from rich import print


def get_addon_srcs(excluded_addons, addons_src) -> list[Path]:
    """Get a list of addon source paths that need to be installed.

    Returns:
        The paths of the addons to be installed.

    """

    def is_python(path: Path) -> bool:
        """Check the given path is either a python module or package.

        Args:
            path: The path to check.

        Returns:
            True if path is a python module or package.

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
