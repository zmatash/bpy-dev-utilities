"""Testing the addon packing tool."""

import zipfile
from pathlib import Path

import pytest

import bpydevutil.functions.common as common
import bpydevutil.functions.pack as pack


@pytest.mark.order(3)
class TestPackClass:
    def test_extract_data(self, fake_addon_dev_env):
        root, src_dir = fake_addon_dev_env
        pack_tool = pack.PackAddonsFromSource(src_dir, root)

        addons = common.get_addon_srcs(src_dir)
        bl_info = pack_tool.get_addon_data(addons[0])

        bl_info_keys = ["name", "version", "blender"]
        assert all(k in bl_info.keys() for k in bl_info_keys)

    def test_generate_name(self, fake_addon_dev_env):
        root, src_dir = fake_addon_dev_env
        bl_info = {"name": "Fake Addon", "version": (0, 2, 0), "blender": (2, 93, 0)}

        pack_tool = pack.PackAddonsFromSource(src_dir, root)
        generated_name = pack_tool.generate_zip_name(bl_info)
        assert generated_name == "Fake Addon (v0.2.0)"

    def test_zip_addon(self, fake_addon_dev_env):
        root, src_dir = fake_addon_dev_env
        addon_file_count = len([file for file in Path(src_dir / "fake_addon_package").rglob("*")])

        pack_tool = pack.PackAddonsFromSource(src_dir, root)

        pack_tool.pack_addon(Path(src_dir / "fake_addon_package"), "TestPackageZip")
        pack_tool.pack_addon(Path(src_dir / "fake_addon_module.py"), "TestModuleZip")

        assert Path(root / "TestPackageZip.zip").is_file()
        assert Path(root / "TestModuleZip.zip").is_file()

        with zipfile.ZipFile(Path(root / "TestPackageZip.zip"), "r") as zip_file:
            zip_file_count = len([file for file in zip_file.namelist()])
            assert zip_file_count == addon_file_count

        with zipfile.ZipFile(Path(root / "TestModuleZip.zip"), "r") as zip_file:
            zip_file_count = len([file for file in zip_file.namelist()])
            assert zip_file_count == 1
