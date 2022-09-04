"""Install Blender addons directly from source files into the Blender addons directory."""

import shutil
from pathlib import Path
from typing import Optional

import typer
from rich import print
from rich.panel import Panel
from rich.progress import track


def render_settings(addons_src, addons_install_dir, excluded_addons):
    src_string = f"Addon Sources Directory = {addons_src}"
    addons_install_string = f"Addon Install Directory = {addons_install_dir}"
    excluded_addons_string = f"Excluded Addons = {excluded_addons}"

    return "\n".join([src_string, addons_install_string, excluded_addons_string])


class InstallAddonsFromSource:
    def __init__(
        self,
        addons_src: Path,
        addons_install_dir: Path,
        excluded_addons: Optional[list[str]] = None,
    ):
        """
        Args:
            addons_src: Directory where addon sources are located.
            addons_install_dir: Directory to install addons to.
            excluded_addons: Names of addons in the source directory not to install. (Include file extensions)

        """
        self.addons_src = addons_src
        self.addons_install_dir = addons_install_dir
        self.excluded_addons = excluded_addons

        print(
            Panel.fit(
                render_settings(addons_src, addons_install_dir, excluded_addons),
                title="[orange3]Installer Settings[/orange3]",
                border_style="yellow",
            )
        )

    def clear_old_addons(self, addon_names: list[str]) -> None:
        """Clear old addon version from the installion directory.

        Args:
            addon_names: List of addon names to delete.

        """

        delete_paths = [
            path for path in self.addons_install_dir.iterdir() if path.exists() and path.name in addon_names
        ]

        if not delete_paths:
            raise typer.Abort()

        for path in track(delete_paths, description="Removing old versions..."):
            if path.is_file():
                path.unlink()
            else:
                shutil.rmtree(path)

    def install_addons(self, addons: list[Path]) -> None:
        """Install addon sources to the addon directory.

        Args:
            addons: List of addon source paths.

        """

        for path in track(addons, description="Installing addons..."):
            if path.is_file():
                shutil.copyfile(path, Path(self.addons_install_dir / path.name))
            else:
                shutil.copytree(path, Path(self.addons_install_dir / path.name))

        print("[green]Done![/green]")
