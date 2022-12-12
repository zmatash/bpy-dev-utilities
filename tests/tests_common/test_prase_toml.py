"""Test toml parsing."""

from bpydevutil.functions import common

def test_parse_toml(temp_projects_dir):
    root_dir, _, _ = temp_projects_dir
    toml_path = root_dir / "pyproject.toml"

    string_result = common.parse_toml(toml_path, "root-dir")
    assert string_result == str(root_dir)