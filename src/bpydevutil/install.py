"""Install Blender addons directly from source files into the Blender addons directory."""

import shutil
from pathlib import Path

from typing import Optional


class InstallAddonsFromSource:
    def __init__(
        self,
        addons_src: Path,
        addons_install_dir: Path,
        print_info: bool = True,
        excluded_addons: Optional[list[str]] = None,
    ):
        """
        Args:
            addons_src: Directory where addon sources are located.
            addons_install_dir: Directory to install addons to.
            print_info: Print information to terminal.
            excluded_addons: Names of addons in the source directory not to install. (Include file extensions)
        """
        self.addons_src = addons_src
        self.addons_install_dir = addons_install_dir
        self.print_info = print_info
        self.excluded_addons = excluded_addons

    def get_addon_srcs(self) -> list[Path]:
        """Get a list of addon source paths that need to be installed.

        Returns:
            The paths of the addons to be installed.

        """

        def is_python(path: Path) -> bool:
            """Check the given path is either a python module or package.

            Args:
                path: The path to check.

            Returns:
                True if path is a python module or package.

            """
            if path.is_dir() and Path(path / "__init__.py").exists():
                if "bl_info" in Path(path / "__init__.py").read_text():
                    return True

            if path.is_file() and path.suffix == ".py":
                if "bl_info" in path.read_text():
                    return True

            return False

        if self.excluded_addons:
            addon_srcs = [
                path for path in self.addons_src.iterdir() if path.name not in self.excluded_addons and is_python(path)
            ]
        else:
            addon_srcs = [path for path in self.addons_src.iterdir() if is_python(path)]

        return addon_srcs

    def clear_old_addons(self, addon_names: list[str]) -> None:
        """Clear old addon version from the installion directory.

        Args:
            addon_names: List of addon names to delete.


        """

        delete_paths = [
            path for path in self.addons_install_dir.iterdir() if path.exists() and path.name in addon_names
        ]

        for path in delete_paths:
            if path.is_file():
                path.unlink()
            else:
                shutil.rmtree(path)

    def install_addons(self, addons: list[Path]) -> None:

        for path in addons:
            if path.is_file():
                shutil.copyfile(path, Path(self.addons_install_dir / path.name))
            else:
                shutil.copytree(path, Path(self.addons_install_dir / path.name))

