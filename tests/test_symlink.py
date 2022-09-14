"""Testing the symlink tool."""

import pytest

from bpydevutil.functions.symlink import SymlinkToAddonSource


@pytest.mark.order(7)
class TestSymlinkClass:
    def test_create_symlink(self, fake_addon_install_env, fake_addon_dev_env):
        root, src = fake_addon_dev_env
        symlink_tool = SymlinkToAddonSource(fake_addon_install_env)

        symlink = symlink_tool.create_sympath(src)
        assert src == symlink.resolve()
