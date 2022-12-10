from pathlib import Path
from typing import Any, Optional

import tomli
import typer
from rich import print
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, track

from bpydevutil.functions import common
from bpydevutil.functions.install import InstallAddonsFromSource
from bpydevutil.functions.pack import PackAddonsFromSource
from bpydevutil.functions.symlink import SymlinkToAddonSource

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
def symlink(
    src_dir: str = typer.Argument(
        default=parse_toml(get_toml(), "src_dir"), help="Directory where addon sources are located."
    ),
    blender_addons_dir: str = typer.Argument(
        default=parse_toml(get_toml(), "blender_addons_dir"), help="Blender addon installation directory."
    ),
    excluded_addons: Optional[list[str]] = typer.Option(
        default=parse_toml(get_toml(), "excluded-addons"), help="Names of addons to ignore."
    ),
    blender_exe: Optional[str] = typer.Option(
        default=parse_toml(get_toml(), "blender-exe"), help="Path to blender.exe."
    ),
    reload_blender: Optional[bool] = typer.Option(
        default=parse_toml(get_toml(), "reload-blender"), help="Restart Blender and enable addons."
    ),
) -> None:
    """
    Create symlinks to the addon source in the addon installation directory.
    """

    def renderable(addons_src, addons_install_dir, excluded_addon_names, blender_exe_path, load_blender):
        src_string = f"Addon Sources Directory = {addons_src}"
        addons_install_string = f"Addon Install Directory = {addons_install_dir}"
        excluded_addons_string = f"Excluded Addons = {excluded_addon_names}"
        blender_exe_string = f"Blender Executable = {blender_exe_path}"
        reload_blender_string = f"Reload Blender = {load_blender}"

        return "\n".join(
            [src_string, addons_install_string, excluded_addons_string, blender_exe_string, reload_blender_string]
        )

    print(
        Panel.fit(
            renderable(src_dir, blender_addons_dir, excluded_addons, blender_exe, reload_blender),
            title="[orange3]Symlinker Settings[/orange3]",
            border_style="yellow",
        )
    )

    directory_params = {"src_dir": src_dir, "blender_addons_dir": blender_addons_dir}

    check_directories(directory_params)

    symlink_tool = SymlinkToAddonSource(Path(blender_addons_dir))

    addon_srcs = common.get_addon_srcs(Path(src_dir), excluded_addons)

    for addon in track(addon_srcs, description="Removing existing files..."):
        common.clear_old_addon(Path(blender_addons_dir), addon.name)

    for addon in track(addon_srcs, description="Creating symlinks..."):
        try:
            symlink_tool.create_sympath(addon)
        except PermissionError:
            print("[red]User does not have permission to create symlinks.[/red]")
            typer.Abort()

    if reload_blender:
        if not blender_exe:
            print("[red]<reload-blender> option is enabled, <blender-exe> path should also be supplied.[/red]")
            print("[dark_orange]Done! Blender will not be loaded.[/dark_orange]")
            return
        common.load_blender(blender_exe, [path.stem for path in addon_srcs])

    print("[green]Done![/green]")


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
    blender_exe: Optional[str] = typer.Option(
        default=parse_toml(get_toml(), "blender-exe"), help="Path to blender.exe."
    ),
    reload_blender: Optional[bool] = typer.Option(
        default=parse_toml(get_toml(), "reload-blender"), help="Restart Blender and enable addons."
    ),
) -> None:
    """
    Directly install addon sources to Blender, clearing old versions beforehand.
    """

    def renderable(addons_src, addons_install_dir, excluded_addon_names, blender_exe_path, load_blender):
        src_string = f"Addon Sources Directory = {addons_src}"
        addons_install_string = f"Addon Install Directory = {addons_install_dir}"
        excluded_addons_string = f"Excluded Addons = {excluded_addon_names}"
        blender_exe_string = f"Blender Executable = {blender_exe_path}"
        reload_blender_string = f"Reload Blender = {load_blender}"

        return "\n".join(
            [src_string, addons_install_string, excluded_addons_string, blender_exe_string, reload_blender_string]
        )

    print(
        Panel.fit(
            renderable(src_dir, blender_addons_dir, excluded_addons, blender_exe, reload_blender),
            title="[orange3]Installer Settings[/orange3]",
            border_style="yellow",
        )
    )

    directory_params = {"src_dir": src_dir, "blender_addons_dir": blender_addons_dir}

    check_directories(directory_params)

    install_tool = InstallAddonsFromSource(Path(blender_addons_dir))
    addon_srcs = common.get_addon_srcs(Path(src_dir), excluded_addons)

    for addon in track(addon_srcs, description="Removing existing files..."):
        common.clear_old_addon(Path(blender_addons_dir), addon.name)

    for addon in track(addon_srcs, description="Installing addons..."):
        install_tool.install_addon(addon)

    if reload_blender:
        if not blender_exe:
            print("[red]<reload-blender> option is enabled, <blender-exe> path should also be supplied.[/red]")
            print("[dark_orange]Done! Blender will not be loaded.[/dark_orange]")
            return
        common.load_blender(blender_exe, [path.stem for path in addon_srcs])

    print("[green]Done![/green]")


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
        help="Addon names to be excluded from packing, separate names with commas.",
    ),
    remove_suffixes: Optional[list[str]] = typer.Option(
        default=parse_toml(get_toml(), "remove-suffixes"),
        help="Remove files with these suffixes from the addon source before running the operation.",
    ),
):
    """
    Pack addons sources into ZIP files, auto generating the name from extracted bl_info data.
    """

    def renderable(addons_src, excluded_addon_names):
        src_string = f"Addon Sources Directory = {addons_src}"
        excluded_addons_string = f"Excluded Addons = {excluded_addon_names}"

        return "\n".join([src_string, excluded_addons_string])

    print(
        Panel.fit(
            renderable(src_dir, excluded_addons),
            title="[orange3]Packer Settings[/orange3]",
            border_style="yellow",
        )
    )

    directory_params = {"src_dir": src_dir, "release_dir": release_dir}

    check_directories(directory_params)

    packing_tool = PackAddonsFromSource(Path(release_dir))
    addon_srcs = common.get_addon_srcs(Path(src_dir), excluded_addons)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description=f"Writing to archive...")
        for addon in addon_srcs:
            bl_info = packing_tool.get_addon_data(addon)
            name = packing_tool.generate_zip_name(bl_info)

            progress.add_task(description=f"Garbage cleaning...")
            common.clear_unused_files(addon, remove_suffixes)
            packing_tool.pack_addon(addon, name, Path(src_dir))

    print("[green]Done![/green]")
