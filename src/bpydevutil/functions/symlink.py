"""Create a symlink in the Blender addons directory rather than directly installing the addon source."""

from pathlib import Path


class SymlinkToAddonSource:
    def __init__(self, addons_install_dir: Path) -> None:
        """
        Args:
            addons_install_dir: Directory to create symlinks in.

        """
        self.addons_install_dir = addons_install_dir

    def create_sympath(self, addon: Path) -> Path:
        """Create a sympath to the addon source inside the addons installation folder.

        Args:
            addon: Source directory of the addon to create a symlink to.

        Returns:
            The sympath directory.
        """

        sympath = Path(self.addons_install_dir / addon.name)
        sympath.symlink_to(addon)

        return sympath
