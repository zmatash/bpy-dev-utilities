"""Test packing of addon files."""

from pathlib import Path
from zipfile import ZipFile

import pytest
import typer

from bpydevutil.functions import pack_funcs


class TestPackAddons:
    """Testing PackAddons."""

    @pytest.fixture(scope="class")
    def _setup(self, temp_projects_dir):
        """Class fixture."""

        root_dir, modules, packages = temp_projects_dir
        src_dir = root_dir / "src"
        output_dir = root_dir / "output"

        return pack_funcs.PackAddonsFromSource(output_dir), output_dir, src_dir, modules, packages

    def test_get_addon_data(self, _setup):
        instance, _, src_dir, _, _ = _setup

        bl_info = instance.get_addon_data(src_dir / "valid_package")
        assert isinstance(bl_info, dict)

    def test_generate_zip_name(self, _setup):
        instance, _, _, _, _ = _setup

        good_bl_info = {"name": "TestName", "version": (1, 1, 3)}
        assert instance.generate_zip_name(good_bl_info) == "TestName (v1.1.3)"

        bad_bl_info = {"version": (1, 1, 3)}
        with pytest.raises(typer.Abort):
            instance.generate_zip_name(bad_bl_info)

    def test_pack_addon(self, _setup):
        instance, output_dir, src_dir, modules, packages = _setup

        for module, is_valid in modules.items():
            if is_valid:
                name = "PackTest_Module"
                instance.pack_addon(src_dir / f"{module}.py", name, src_dir)
                with ZipFile(output_dir / f"{name}.zip") as f:
                    assert Path(output_dir / name).with_suffix(".zip").is_file()
                    assert len(f.namelist()) == 1
                break

        for package, is_valid in packages.items():
            if is_valid:
                name = "PackTest_Package"
                file_count = len(list(Path(src_dir / package).rglob("*")))

                instance.pack_addon(src_dir / package, name, src_dir)
                with ZipFile(output_dir / f"{name}.zip") as f:
                    assert Path(output_dir / name).with_suffix(".zip").is_file()
                    assert len(f.namelist()) == file_count
                break
