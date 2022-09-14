"""Testing the addon packing tool."""

import zipfile
from pathlib import Path

import pytest

import bpydevutil.functions.common as common
import bpydevutil.functions.pack as pack


@pytest.mark.order(6)
class TestPackClass:
    def test_extract_data(self, fake_addon_dev_env, fake_addon_install_env):
        root, src_dir = fake_addon_dev_env
        pack_tool = pack.PackAddonsFromSource(fake_addon_install_env)

        addons = common.get_addon_srcs(src_dir)
        bl_info = pack_tool.get_addon_data(addons[0])

        bl_info_keys = ["name", "version", "blender"]
        assert all(k in bl_info.keys() for k in bl_info_keys)

    def test_generate_name(self, fake_addon_install_env):
        bl_info = {"name": "Fake Addon", "version": (0, 2, 0), "blender": (2, 93, 0)}

        pack_tool = pack.PackAddonsFromSource(fake_addon_install_env)
        generated_name = pack_tool.generate_zip_name(bl_info)
        assert generated_name == "Fake Addon (v0.2.0)"

    @pytest.mark.parametrize(
        "addon_name, zip_name", [("fake_addon_package", "TestPackageZip"), ("fake_addon_module.py", "TestModuleZip")]
    )
    def test_zip_addon(self, fake_addon_dev_env, addon_name, zip_name):
        root, src_dir = fake_addon_dev_env

        addon_path = Path(src_dir / addon_name)
        if addon_path.is_dir():
            addon_file_count = len([file for file in addon_path.rglob("*")])
        else:
            addon_file_count = 1

        pack_tool = pack.PackAddonsFromSource(root)

        pack_tool.pack_addon(Path(src_dir / addon_name), zip_name, src_dir)

        assert Path(root / f"{zip_name}.zip").is_file()

        with zipfile.ZipFile(Path(root / f"{zip_name}.zip"), "r") as zip_file:
            zip_file_count = len([file for file in zip_file.namelist()])
            assert zip_file_count == addon_file_count
