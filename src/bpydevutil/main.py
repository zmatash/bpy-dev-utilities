from pathlib import Path
from typing import Any, Optional

import tomli
import typer

from bpydevutil.functions import common
from bpydevutil.functions.install import InstallAddonsFromSource
from bpydevutil.functions.pack import PackAddonsFromSource

app = typer.Typer()


def check_directories(directory_params: dict[str, str]) -> None:
    """Check given directory arguments exist and are valid.

    Args:
        directory_params: Dictionary of arguments and corresponding values..

    """
    for param in directory_params.keys():
        if not directory_params[param]:
            raise typer.BadParameter(f"<{param}> cannot be empty.")

        if not Path(directory_params[param]).is_dir():
            raise typer.BadParameter(f"<{param}> <{directory_params[param]}> is not an existing directory.")


def parse_toml(toml: Path, param_key: str) -> Any:
    with open(toml, "rb") as f:
        toml_dict = tomli.load(f)
        try:
            return toml_dict["tool"]["bpydevutil"][param_key]
        except KeyError:
            return None


def get_toml():
    pyproject = Path.cwd() / "pyproject.toml"
    if pyproject.exists():
        return pyproject
    else:
        return None


@app.command()
def install(
    src_dir: str = typer.Argument(
        default=parse_toml(get_toml(), "src_dir"), help="Directory where addon sources are located."
    ),
    blender_addons_dir: str = typer.Argument(
        default=parse_toml(get_toml(), "blender_addons_dir"), help="Blender addon installation directory."
    ),
    excluded_addons: Optional[list[str]] = typer.Option(
        default=parse_toml(get_toml(), "excluded-addons"),
        help="Addon names to be excluded from installation, separate names with commas.",
    ),
    remove_suffixes: Optional[list[str]] = typer.Option(
        default=parse_toml(get_toml(), "remove-suffixes"),
        help="Remove files with these suffixes from the addon source before running the operation.",
    ),
) -> None:
    """
    Directly install addon sources to Blender, clearing old versions beforehand.
    """

    directory_params = {"src_dir": src_dir, "blender_addons_dir": blender_addons_dir}

    check_directories(directory_params)

    install_tool = InstallAddonsFromSource(Path(src_dir), Path(blender_addons_dir), excluded_addons)

    addon_srcs = common.get_addon_srcs(install_tool.addons_src, install_tool.excluded_addons)
    install_tool.clear_old_addons([path.name for path in addon_srcs])
    for addon in addon_srcs:
        common.clear_unused_files(addon, remove_suffixes)
    install_tool.install_addons(addon_srcs)


@app.command()
def pack(
    src_dir: str = typer.Argument(
        default=parse_toml(get_toml(), "src_dir"), help="Directory where addon sources are located."
    ),
    release_dir: str = typer.Argument(
        default=parse_toml(get_toml(), "release_dir"), help="Directory where addons should be moved after packing."
    ),
    excluded_addons: Optional[list[str]] = typer.Option(
        default=parse_toml(get_toml(), "exluded-addons"),
        help="Addon names to be excluded from installation, separate names with commas.",
    ),
    remove_suffixes: Optional[list[str]] = typer.Option(
        default=parse_toml(get_toml(), "remove-suffixes"),
        help="Remove files with these suffixes from the addon source before running the operation.",
    ),
):
    """
    Pack addons sources into ZIP files, autogenerating the name from extracted bl_info data.
    """
    directory_params = {"src_dir": src_dir, "release_dir": release_dir}

    check_directories(directory_params)

    packing_tool = PackAddonsFromSource(Path(src_dir), Path(release_dir), excluded_addons)
    addon_srcs = common.get_addon_srcs(packing_tool.addons_src, packing_tool.excluded_addons)

    for addon in addon_srcs:
        bl_info = packing_tool.get_addon_data(addon)
        name = packing_tool.generate_zip_name(bl_info)
        common.clear_unused_files(addon, remove_suffixes)
        packing_tool.pack_addon(addon, name)
