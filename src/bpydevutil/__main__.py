from pathlib import Path
from typing import Optional

import iniconfig
import typer
from iniconfig import IniConfig

from install import InstallAddonFromSource

app = typer.Typer()

cwd = Path.cwd()
config = Path(cwd / "bpydevutil.ini")

if config.is_file():
    ini_config = iniconfig.IniConfig(str(config))
else:
    ini_config = "NO_PARAM"


def get_cfg_arg(cfg: IniConfig, param: str):
    if cfg == "NO_PARAM":
        return cfg

    try:
        return cfg["bpydevutil"][param]
    except KeyError:
        return "NO_PARAM"


@app.command()
def install(
    src_dir: str = typer.Argument(default=get_cfg_arg(ini_config, "src_dir")),
    blender_addons_dir: str = typer.Argument(default=get_cfg_arg(ini_config, "blender_addons_dir")),
    excluded_addons: Optional[list[str]] = None,
):
    directory_params = {"src_dir": src_dir, "blender_addons_dir": blender_addons_dir}

    for param in directory_params.keys():
        if directory_params[param] == "NO_PARAM":
            raise typer.BadParameter(f"<{param}> cannot be empty.")

        if not Path(directory_params[param]).is_dir():
            raise typer.BadParameter(f"<{param}> <{directory_params[param]}> is not a valid directory.")

    InstallAddonFromSource(src_dir, blender_addons_dir).main(excluded_addons)


if __name__ == "__main__":
    app()
