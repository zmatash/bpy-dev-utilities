from pathlib import Path
from typing import Optional, Union

import iniconfig
import typer
from iniconfig import IniConfig

from install import InstallAddonsFromSource

app = typer.Typer()

cwd = Path.cwd()
config = Path(cwd / "bpydevutil.ini")

if config.is_file():
    ini_config = iniconfig.IniConfig(str(config))
else:
    ini_config = None


def get_cfg_arg(cfg: IniConfig, param: str):
    if not cfg:
        return None

    try:
        return cfg["bpydevutil"][param]
    except KeyError:
        return None


def parse_cfg_list(value: str) -> Union[list[str], None]:
    """Split a string into a list.

    Args:
        value: The string to split by commas.

    Returns:
        The list of strings.

    """

    if not value:
        return None

    value = value.replace(", ", ",")
    return value.split(",")


@app.command()
def install(
    src_dir: str = typer.Argument(
        default=get_cfg_arg(ini_config, "src_dir"), help="Directory where addon sources are located."
    ),
    blender_addons_dir: str = typer.Argument(
        default=get_cfg_arg(ini_config, "blender_addons_dir"), help="Blender addon installion directory."
    ),
    excluded_addons: Optional[list[str]] = typer.Option(
        default=parse_cfg_list(get_cfg_arg(ini_config, "excluded_addons")),
        help="Addon names to be excluded from installion, separate names with commas.",
    ),
) -> None:
    """
    Directly install addon sources to Blender, clearing old versions beforehand.
    """

    directory_params = {"src_dir": src_dir, "blender_addons_dir": blender_addons_dir}

    for param in directory_params.keys():
        if not directory_params[param]:
            raise typer.BadParameter(f"<{param}> cannot be empty.")

        if not Path(directory_params[param]).is_dir():
            raise typer.BadParameter(f"<{param}> <{directory_params[param]}> is not a valid directory.")

    install_tool = InstallAddonsFromSource(Path(src_dir), Path(blender_addons_dir), excluded_addons)

    addon_srcs = install_tool.get_addon_srcs()
    install_tool.clear_old_addons([path.name for path in addon_srcs])
    install_tool.install_addons(addon_srcs)

    print(excluded_addons)


if __name__ == "__main__":
    app()
