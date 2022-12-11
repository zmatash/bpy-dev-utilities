"""Test finding addon sources."""

from bpydevutil.functions import common

def test_get_addon_srcs(temp_projects_dir):
    root_dir, modules, packages = temp_projects_dir

    arbitrary_package1 = root_dir / list(packages.keys())[0]
    arbitrary_package2 = root_dir / list(packages.keys())[1]

    assert len(list(arbitrary_package1.rglob("*.pyc"))) != 0
    common.clear_unused_files(arbitrary_package1)
    assert len(list(arbitrary_package1.rglob("*.pyc"))) == 0

    waste_files = list(arbitrary_package2.rglob("*.txt"))
    waste_files.extend(list(arbitrary_package2.rglob("*.tmp")))

    assert len(waste_files) != 0
    common.clear_unused_files(arbitrary_package2, {".txt", ".tmp"})

    waste_files = list(arbitrary_package2.rglob("*.txt"))
    waste_files.extend(list(arbitrary_package2.rglob("*.tmp")))
    assert len(waste_files) == 0
