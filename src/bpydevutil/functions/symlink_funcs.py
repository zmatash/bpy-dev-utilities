"""Create a symlink in the Blender addons directory rather than directly installing the addon source."""

from pathlib import Path


class SymlinkToAddonSource:
    """Symlink creator."""
    def __init__(self, addons_install_dir: Path) -> None:
        """
        Args:
            addons_install_dir: Directory to create symlinks in.
        """
        self.addons_install_dir = addons_install_dir

    def create_symlink(self, addon_path: Path) -> Path:
        """Create a symlink to the addon source inside the addons installation folder.

        Args:
            addon_path: Source directory of the addon to create a symlink to.

        Returns:
            The symlink directory.
        """

        symlink = Path(self.addons_install_dir / addon_path.name)
        symlink.symlink_to(addon_path)

        return symlink
