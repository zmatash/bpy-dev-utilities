"""Pack addon into a ZIP file and automatically generate file information in the title."""
import ast
import importlib
import re
import sys
from pathlib import Path
from typing import Any, Optional, Union
from zipfile import ZIP_DEFLATED, ZipFile

import typer
from rich import print
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn


def render_settings(addons_src: Union[Path, str], release_dir: Union[Path, str], excluded_addons: list[str]) -> str:
    """Build a string represeting the tool settings in a printable format.

    Args:
        addons_src: Directory where addon sources are located.
        release_dir: Directory where addon should be moved after it is packed.
        excluded_addons: Names of addons in the source directory not to pack. (Include file extensions)

    Returns:
        The settings string to print to console.
    """

    src_string = f"Addon Sources Directory = {addons_src}"
    addon_release_string = f"Releases Directory = {release_dir}"
    excluded_addons_string = f"Excluded Addons = {excluded_addons}"

    return "\n".join([src_string, addon_release_string, excluded_addons_string])


def render_pack_report(file_count: int, file_path: Path) -> str:
    """Build a string represeting the packing report in a printable format.

    Args:
        file_count: The number of files archived.
        file_path: The final path of the generated archive.

    Returns:
        The report  string to print to console.
    """
    files_processed = f"Files Archived: {file_count}"
    zip_path = f"Archive Location: {file_path}"

    return "\n".join([files_processed, zip_path])


class PackAddonsFromSource:
    """Pack addons and generate data for release."""

    def __init__(self, addons_src: Path, release_dir: Path, excluded_addons: Optional[list[str]] = None) -> None:
        """

        Args:
            addons_src: Directory where addon sources are located.
            release_dir: Directory where addon should be moved after it is packed.
            excluded_addons: Names of addons in the source directory not to pack. (Include file extensions)
        """

        self.addons_src = addons_src
        self.release_dir = release_dir
        self.excluded_addons = excluded_addons

        print(
            Panel.fit(
                render_settings(addons_src, release_dir, excluded_addons),
                title="[orange3]Packer Settings[/orange3]",
                border_style="yellow",
                width=700,
            )
        )

    @staticmethod
    def get_addon_data(addon: Path) -> dict[str, Any]:
        """Extract the bl_info from the addon.

        Args:
            addon: Path of the addon to process.

        Returns:
            bl_info dictionary.
        """

        sys.path.append(str(addon.parent))
        try:
            imported_module = importlib.import_module(addon.stem)
            return imported_module.bl_info
        except ModuleNotFoundError:
            pass

        if addon.is_file():
            init = Path(addon)
        else:
            init = Path(addon / "__init__.py")

        text = init.read_text()
        bl_info = re.search(r"((?<=bl_info\s=\s)|(?<=bl_info=))(\s|){[\s\S]*?}", text)

        return ast.literal_eval(bl_info[0])

    @staticmethod
    def generate_zip_name(bl_info: dict[str, Any]) -> str:
        """Generate the name of the addon package using the data inside the bl_info.

        Args:
            bl_info: bl_info dictionary extracted from the addon.

        Returns:
            The final addon package name.
        """

        data_keys = ["name", "version", "blender"]
        for k in data_keys:
            if k not in bl_info.keys():
                print(
                    f"[red]<{k}> does not exist in the addon bl_info dictionary.[/red]"
                    "[red]\nThis data is required to generate the ZIP file name.[/red]"
                )
                raise typer.Abort()

        formatted_version = str(bl_info["version"])[1:-1].replace(",", ".").replace(" ", "")
        zip_name = f"{bl_info['name']} (v{formatted_version})"

        return zip_name

    def pack_addon(self, addon: Path, name: str) -> None:
        """Pack the addon source into a ZIP file ready for distribution.

        Args:
            addon: The path of the addon to pack.
            name: The name of the resulting ZIP file.
        """

        files_processed = 0

        if not name.endswith(".zip"):
            name = f"{name}.zip"

        zip_path = Path(self.release_dir / name)
        if zip_path.exists():
            typer.confirm("This file already exists. Do you want to overwrite it?", default=True, abort=True)

        with ZipFile(zip_path, "w", ZIP_DEFLATED) as zip_file:
            with Progress(
                SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True
            ) as progress:
                progress.add_task(description=f"Writing to archive...")
                if addon.is_dir():
                    for entry in addon.rglob("*"):
                        zip_file.write(Path(entry), entry.relative_to(self.addons_src))
                        files_processed += 1
                else:
                    zip_file.write(Path(addon), addon.relative_to(self.addons_src))

        print(
            Panel.fit(
                renderable=render_pack_report(files_processed, Path(self.release_dir / name)),
                title="Packer Report",
                border_style="green",
                width=700,
            )
        )
        print("[green]Done![/green]")
