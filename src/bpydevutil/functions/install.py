"""Install Blender addons directly from source files into the Blender addons directory."""

import shutil
from pathlib import Path
from subprocess import Popen


class InstallAddonsFromSource:
    """Install addons directly from source to Blender."""

    def __init__(self, addons_install_dir: Path) -> None:
        """
        Args:
            addons_install_dir: Directory to install addons to.
        """
        self.addons_install_dir = addons_install_dir

    def install_addon(self, addon_path: Path) -> None:
        """Install addon sources to the addon directory.

        Args:
            addon_path: The addon source path.
        """

        if addon_path.is_file():
            shutil.copyfile(addon_path, Path(self.addons_install_dir / addon_path.name))
        else:
            shutil.copytree(addon_path, Path(self.addons_install_dir / addon_path.name))

    def run_blender(self, addon_names: list[str] = None):

        """Run Blender and activate addons.

        Args:
            addon_names: List of addon modules to activate.

        """

        Popen(f"{self.blender_exe} --addons {','.join(addon_names)}")
