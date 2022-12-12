"""Test installation of addon files."""

import pytest

from bpydevutil.functions import install


class TestInstallAddonsFromSource:
    """Testing InstallAddonsFromSource."""

    @pytest.fixture(scope="class")
    def _setup(self, temp_addons_dir):
        """Class fixture."""

        addons_dir, _, _ = temp_addons_dir
        return install.InstallAddonsFromSource(addons_dir), addons_dir

    def test_install_addon(self, _setup, temp_projects_dir):
        instance, addons_dir = _setup
        root_dir, modules, packages = temp_projects_dir
        src_dir = root_dir / "src"

        installed_addons = [path.stem for path in addons_dir.glob("*")]
        for module, is_valid in modules.items():
            assert module not in installed_addons
            if is_valid:
                instance.install_addon(src_dir / f"{module}.py")

        for package, is_valid in packages.items():
            assert package not in installed_addons
            if is_valid:
                instance.install_addon(src_dir / package)

        installed_addons = [path.stem for path in addons_dir.glob("*")]
        for module, is_valid in modules.items():
            if is_valid:
                assert module in installed_addons

        for package, is_valid in packages.items():
            if is_valid:
                assert package in installed_addons
