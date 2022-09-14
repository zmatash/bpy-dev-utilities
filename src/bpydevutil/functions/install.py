"""Install Blender addons directly from source files into the Blender addons directory."""

import shutil
from pathlib import Path
from subprocess import Popen


class InstallAddonsFromSource:
    def __init__(self, addons_install_dir: Path) -> None:
        """
        Args:
            addons_install_dir: Directory to install addons to.

        """
        self.addons_install_dir = addons_install_dir

    def install_addon(self, addon: Path) -> None:
        """Install addon sources to the addon directory.

        Args:
            addon: The addon source path.

        """

        if addon.is_file():
            shutil.copyfile(addon, Path(self.addons_install_dir / addon.name))
        else:
            shutil.copytree(addon, Path(self.addons_install_dir / addon.name))

    def run_blender(self, addons: list[str] = None):

        """Run Blender and activate addons.

        Args:
            addons: List of addon modules to activate.

        """

        Popen(f"{self.blender_exe} --addons {','.join(addons)}")
