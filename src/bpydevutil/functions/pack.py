"""Pack addon into a ZIP file and automatically generate file information in the title."""
import ast
from pathlib import Path
from typing import Any, Union
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
    def get_addon_data(addon_path: Path) -> Union[dict[str, Any], None]:
        """Extract the bl_info from the addon.

        Args:
            addon_path: Path of the addon to process.

        Returns:
            bl_info dictionary (keys=name, version).
        """

        if addon_path.is_file():
            init = Path(addon_path)
        else:
            init = Path(addon_path / "__init__.py")
        text = init.read_text()

        mod = ast.parse(text)

        bl_info = {}
        nodes = []
        current_node = -1

        for node in ast.walk(mod):
            current_node += 1
            nodes.append(node)
            if isinstance(node, ast.Dict):
                previous_node = nodes[current_node - 1]
                if isinstance(previous_node, ast.Name) and previous_node.id == "bl_info":
                    pass
                else:
                    continue

                for key, value in zip(node.keys, node.values):
                    new_key = eval(compile(ast.Expression(key), "<ast expression>", "eval"))
                    new_value = eval(compile(ast.Expression(value), "<ast expression>", "eval"))
                    bl_info[new_key] = new_value

                return bl_info
        return None

    @staticmethod
    def generate_zip_name(bl_info: dict[str, Any]) -> str:
        """Generate the name of the addon package using the data inside the bl_info.

        Args:
            bl_info: bl_info dictionary extracted from the addon.

        Returns:
            An auto generated name based on the supplied information.
        """

        data_keys = ["name", "version"]
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

    def pack_addon(self, addon_path: Path, name: str, addons_src: Path) -> None:
        """Pack the addon source into a ZIP file ready for distribution.

        Args:
            addon_path: The path of the addon to pack.
            name: The name of the resulting ZIP file.
            addons_src: The path of the root directory where addon sources are located.
        """

        if not name.endswith(".zip"):
            name = f"{name}.zip"

        zip_path = self.release_dir / name
        if zip_path.exists():
            typer.confirm("This file already exists. Do you want to overwrite it?", default=True, abort=True)

        with ZipFile(zip_path, "w", ZIP_DEFLATED) as zip_file:
            if addon_path.is_dir():
                for entry in addon_path.rglob("*"):
                    zip_file.write(Path(entry), entry.relative_to(addons_src))
            else:
                zip_file.write(Path(addon_path), addon_path.relative_to(addons_src))
