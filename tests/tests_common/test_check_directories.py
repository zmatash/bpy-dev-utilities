"""Test directory checks."""

import pytest
import typer

from bpydevutil.functions import common


def test_check_directories(temp_projects_dir):
    root_dir, _, _ = temp_projects_dir

    param_dict = {"test_dir": str(root_dir)}
    assert common.check_directories(param_dict)

    param_dict = {"test_dir": ""}
    with pytest.raises(typer.BadParameter):
        assert common.check_directories(param_dict)