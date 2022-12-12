"""Command line functionality."""

from pathlib import Path
from typing import Optional

import typer
from rich import panel, print, progress

from bpydevutil.functions import common_funcs, install_funcs, pack_funcs, symlink_funcs

app = typer.Typer()
config = common_funcs.get_toml()


@app.command()
def symlink(
    src_dir: str = typer.Argument(
        common_funcs.parse_toml(config, "src-dir"), help="Directory where addon sources are located."
    ),
    blender_addons_dir: str = typer.Argument(
        common_funcs.parse_toml(config, "blender-addons-dir"), help="Blender addon installation directory."
    ),
    excluded_addons: Optional[list[str]] = typer.Argument(
        common_funcs.parse_toml(config, "excluded-addons"), help="List of addons to ignore."
    ),
    blender_exe: Optional[str] = typer.Argument(
        common_funcs.parse_toml(config, "blender-exe"), help="Path to blender.exe."
    ),
    reload_blender: Optional[bool] = typer.Argument(
        common_funcs.parse_toml(config, "reload-blender"), help="Restart Blender and enable addons."
    ),
) -> None:
    """Create symlinks between addon sources and addon installation directory.

    Args:
        src_dir: Directory where addon sources are located.
        blender_addons_dir: Blender addon installation directory.
        excluded_addons: List of addon names to ignore.
        blender_exe: Path to blender.exe.
        reload_blender: Restart Blender and enable addons.
    """

    def format_parameters() -> str:
        """Format parameters for printing in the console."""
        src_string = f"Addon Sources Directory = {src_dir}"
        addons_install_string = f"Addon Install Directory = {blender_addons_dir}"
        excluded_addons_string = f"Excluded Addons = {excluded_addons}"
        blender_exe_string = f"Blender Executable = {blender_exe}"
        reload_blender_string = f"Reload Blender = {reload_blender}"

        return "\n".join(
            [src_string, addons_install_string, excluded_addons_string, blender_exe_string, reload_blender_string]
        )

    print(panel.Panel.fit(format_parameters(), title="[orange3]Symlink Tool Settings[/orange3]", border_style="yellow"))

    directory_params = {"src-dir": src_dir, "blender-addons-dir": blender_addons_dir}
    common_funcs.check_directories(directory_params)

    symlink_tool = symlink_funcs.SymlinkToAddonSource(Path(blender_addons_dir))
    addon_srcs = common_funcs.get_addon_srcs(Path(src_dir), excluded_addons)

    for addon in progress.track(addon_srcs, description="Removing old files..."):
        common_funcs.clear_old_addon(Path(blender_addons_dir), addon.name)

    for addon in progress.track(addon_srcs, description="Creating symlinks..."):
        try:
            symlink_tool.create_symlink(addon)
        except PermissionError:
            print("[red]You do not have permission to create symlinks.[/red]")
            typer.Abort()

    if reload_blender:
        common_funcs.load_blender(blender_exe, [path.stem for path in addon_srcs])

        if not blender_exe:
            print("[red]<reload-blender> option is enabled, <blender-exe> path should also be supplied.[/red]")
            print("[dark_orange]Done! Blender will not be loaded.[/dark_orange]")
            return

    print("[green]Done![/green]")


@app.command()
def install(
    src_dir: str = typer.Argument(
        common_funcs.parse_toml(config, "src-dir"), help="Directory where addon sources are located."
    ),
    blender_addons_dir: str = typer.Argument(
        common_funcs.parse_toml(config, "blender-addons-dir"), help="Blender addon installation directory."
    ),
    excluded_addons: Optional[list[str]] = typer.Argument(
        common_funcs.parse_toml(config, "excluded-addons"), help="List of addons to ignore."
    ),
    blender_exe: Optional[str] = typer.Argument(
        common_funcs.parse_toml(config, "blender-exe"), help="Path to blender.exe."
    ),
    reload_blender: Optional[bool] = typer.Argument(
        common_funcs.parse_toml(config, "reload-blender"), help="Restart Blender and enable addons."
    ),
) -> None:
    """Install addons directly from sources to addon installation directory.

    Args:
        src_dir: Directory where addon sources are located.
        blender_addons_dir: Blender addon installation directory.
        excluded_addons: List of addon names to ignore.
        blender_exe: Path to blender.exe.
        reload_blender: Restart Blender and enable addons.
    """

    def format_parameters() -> str:
        """Format parameters for printing in the console."""
        src_string = f"Addon Sources Directory = {src_dir}"
        addons_install_string = f"Addon Install Directory = {blender_addons_dir}"
        excluded_addons_string = f"Excluded Addons = {excluded_addons}"
        blender_exe_string = f"Blender Executable = {blender_exe}"
        reload_blender_string = f"Reload Blender = {reload_blender}"

        return "\n".join(
            [src_string, addons_install_string, excluded_addons_string, blender_exe_string, reload_blender_string]
        )

    print(
        panel.Panel.fit(format_parameters(), title="[orange3]Installer Tool Settings[/orange3]", border_style="yellow")
    )

    directory_params = {"src-dir": src_dir, "blender-addons-dir": blender_addons_dir}
    common_funcs.check_directories(directory_params)

    install_tool = install_funcs.InstallAddonsFromSource(Path(blender_addons_dir))
    addon_srcs = common_funcs.get_addon_srcs(Path(src_dir), excluded_addons)

    for addon in progress.track(addon_srcs, description="Removing old files..."):
        common_funcs.clear_old_addon(Path(blender_addons_dir), addon.name)

    for addon in progress.track(addon_srcs, description="Installing addons..."):
        try:
            install_tool.install_addon(addon)
        except PermissionError:
            print("[red]You do not have permission to install files in this directory.[/red]")
            typer.Abort()

    if reload_blender:
        common_funcs.load_blender(blender_exe, [path.stem for path in addon_srcs])

        if not blender_exe:
            print("[red]<reload-blender> option is enabled, <blender-exe> path should also be supplied.[/red]")
            print("[dark_orange]Done! Blender will not be loaded.[/dark_orange]")
            return

    print("[green]Done![/green]")


@app.command()
def pack(
    src_dir: str = typer.Argument(
        common_funcs.parse_toml(config, "src-dir"), help="Directory where addon sources are located."
    ),
    output_dir: str = typer.Argument(common_funcs.parse_toml(config, "output-dir"), help="ZIP file output directory."),
    excluded_addons: Optional[list[str]] = typer.Argument(
        common_funcs.parse_toml(config, "excluded-addons"), help="List of addons to ignore."
    ),
    remove_suffixes: Optional[list[str]] = typer.Option(
        default=common_funcs.parse_toml(config, "remove-suffixes"),
        help="Remove files with these suffixes from the addon source before running the operation.",
    ),
) -> None:
    """Pack addons into zip files and automatically generate names using bl_info.

    Args:
        src_dir: Directory where addon sources are located.
        output_dir: ZIP file output directory.
        excluded_addons: List of addon names to ignore.
        remove_suffixes: Remove any files with these suffixes before packing.
    """

    def format_parameters() -> str:
        """Format parameters for printing in the console."""
        src_string = f"Addon Sources Directory = {src_dir}"
        output_dir_string = f"Output Directory = {output_dir}"
        excluded_addons_string = f"Excluded Addons = {excluded_addons}"
        remove_suffixes_string = f"Remove Suffixes = {remove_suffixes}"

        return "\n".join([src_string, output_dir_string, excluded_addons_string, remove_suffixes_string])

    print(panel.Panel.fit(format_parameters(), title="[orange3]Packing Tool Settings[/orange3]", border_style="yellow"))

    directory_params = {"src-dir": src_dir, "output-dir": output_dir}
    common_funcs.check_directories(directory_params)

    packing_tool = pack_funcs.PackAddonsFromSource(Path(output_dir))
    addon_srcs = common_funcs.get_addon_srcs(Path(src_dir), excluded_addons)

    total_files_cleared = 0
    for addon in progress.track(addon_srcs, description="Packing addons..."):
        bl_info = packing_tool.get_addon_data(addon)
        name = packing_tool.generate_zip_name(bl_info)
        files_cleared = common_funcs.clear_unused_files(addon, remove_suffixes)
        total_files_cleared += files_cleared
        packing_tool.pack_addon(addon, name, Path(src_dir))

    if total_files_cleared > 0:
        print(f"[green]Garbage Cleaning:[/green] {total_files_cleared} files removed.")
    print("[green]Done![/green]")
