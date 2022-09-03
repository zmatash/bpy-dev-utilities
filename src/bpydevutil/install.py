"""Install Blender addons directly from source files into the Blender addons directory."""

import shutil
from pathlib import Path
from typing import Optional

import typer
from rich import print
from rich.panel import Panel
from rich.progress import track


def render_settings(addons_src, addons_install_dir, excluded_addons):
    src_string = f"Addon Sources = {addons_src}"
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

    def get_addon_srcs(self) -> list[Path]:
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

        if self.excluded_addons:
            addon_srcs = [
                path for path in self.addons_src.iterdir() if path.name not in self.excluded_addons and is_python(path)
            ]
        else:
            addon_srcs = [path for path in self.addons_src.iterdir() if is_python(path)]

        if not addon_srcs:
            print(f"[red]There are no addon sources inside the directory [{self.addons_src}][/red]")
            raise typer.Abort()

        return addon_srcs

    def clear_old_addons(self, addon_names: list[str]) -> None:
        """Clear old addon version from the installion directory.

        Args:
            addon_names: List of addon names to delete.


        """

        delete_paths = [
            path for path in self.addons_install_dir.iterdir() if path.exists() and path.name in addon_names
        ]

        if not delete_paths:
            return

        for _ in track(delete_paths, show_speed=False, description="Removing old versions..."):
            for path in delete_paths:
                if path.is_file():
                    path.unlink()
                else:
                    shutil.rmtree(path)

    def install_addons(self, addons: list[Path]) -> None:
        """Install addon sources to the addon directory.

        Args:
            addons: List of addon source paths.

        """

        for _ in track(addons, description="Installing addons..."):
            for path in addons:
                if path.is_file():
                    shutil.copyfile(path, Path(self.addons_install_dir / path.name))
                else:
                    shutil.copytree(path, Path(self.addons_install_dir / path.name))

        print("[green]Done![/green]")
