"""Test installation of addon files."""

import pytest

from bpydevutil.functions import symlink_funcs


class TestSymlinkToAddonSource:
    """Testing SymlinkToAddonSource."""

    @pytest.fixture(scope="class")
    def _setup(self, temp_addons_dir):
        """Class fixture."""

        addons_dir, _, _ = temp_addons_dir
        symlinks_dir = addons_dir / "symlinks"
        return symlink_funcs.SymlinkToAddonSource(symlinks_dir), symlinks_dir

    def test_create_symlink(self, _setup, temp_projects_dir):
        instance, symlinks_dir = _setup
        root_dir, modules, packages = temp_projects_dir
        src_dir = root_dir / "src"

        symlinks = [path.stem for path in symlinks_dir.glob("*")]
        for module, is_valid in modules.items():
            assert module not in symlinks
            if is_valid:
                instance.create_symlink(src_dir / f"{module}.py")

        for package, is_valid in packages.items():
            assert package not in symlinks
            if is_valid:
                instance.create_symlink(src_dir / package)

        symlinks = [path.stem for path in symlinks_dir.glob("*")]
        for module, is_valid in modules.items():
            if is_valid:
                assert module in symlinks

        for package, is_valid in packages.items():
            if is_valid:
                assert package in symlinks
