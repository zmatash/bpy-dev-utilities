"""Test toml find."""

import os

from bpydevutil.functions import common


def test_get_toml(temp_projects_dir):
    root_dir, _, _ = temp_projects_dir
    toml_path = root_dir / "pyproject.toml"

    os.chdir(root_dir)
    result_path = common.get_toml()
    assert result_path == toml_path
