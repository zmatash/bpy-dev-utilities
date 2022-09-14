"""Pack addon into a ZIP file and automatically generate file information in the title."""
import ast
import importlib
import re
import sys
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

import typer
from rich import print


class PackAddonsFromSource:
    """Pack addons and generate data for release."""

    def __init__(self, release_dir: Path) -> None:
        """

        Args:
            release_dir: Directory where addon should be moved after it is packed.

        """

        self.release_dir = release_dir

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

    def pack_addon(self, addon: Path, name: str, addons_src: Path) -> None:
        """Pack the addon source into a ZIP file ready for distribution.

        Args:
            addon: The path of the addon to pack.
            name: The name of the resulting ZIP file.
            addons_src: The path of the root directory where addon sources are located.

        """

        if not name.endswith(".zip"):
            name = f"{name}.zip"

        zip_path = Path(self.release_dir / name)
        if zip_path.exists():
            typer.confirm("This file already exists. Do you want to overwrite it?", default=True, abort=True)

        with ZipFile(zip_path, "w", ZIP_DEFLATED) as zip_file:
            if addon.is_dir():
                for entry in addon.rglob("*"):
                    zip_file.write(Path(entry), entry.relative_to(addons_src))
            else:
                zip_file.write(Path(addon), addon.relative_to(addons_src))
