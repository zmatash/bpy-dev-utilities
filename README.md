
## BPY Dev Utilities

This is a personal collection of simple CLI utilities that I made to help my development of Blender addons.

### Installation
```shell
pip install bpy-dev-utils
```
#### OR
```shell
poetry add bpy-dev-utils
```

## Install Tool
```sh
bpy install <src_dir> <blender_addons_dir>
```
Installs addons directly from their source files into the specified Blender addons installation directory.
#### Arguments:
- src_dir: Directory where addon sources are located. eg ```MyProject\src```
- blender_addons_dir: Blender addon installation directory. eg ```\Blender\3.2\scripts\addons```

#### Options:
- --excluded-addons: Addon names to be excluded from installation. eg ```["Addon1", "Addon2"]```
- --remove-suffixes: File types to be deleted before installation. eg ```[".pyc", ".txt"]```
- --blender-exe: Path to blender exe. eg ```\Blender\blender.exe```
- --reload-blender: Load blender and enable addons, requires --blender-exe to be set. eg ```True```
- --help: Show help.

## Symlink Tool
```sh
bpy symlink <src_dir> <blender_addons_dir>
```
Creates symlinks to the addon source in the specified Blender addons installation directory. Requires either symlink creation privileges, either through running as admin or security policy.
#### Arguments:
- src_dir: Directory where addon sources are located. eg ```MyProject\src```
- blender_addons_dir: Blender addon installation directory. eg ```\Blender\3.2\scripts\addons```

#### Options:
- --excluded-addons: Addon names to be excluded from symlink creation. eg ```["Addon1", "Addon2"]```
- --remove-suffixes: File types to be deleted before symlink creation. eg ```[".pyc", ".txt"]```
- --blender-exe: Path to blender exe. eg ```\Blender\blender.exe```
- --reload-blender: Load blender and enable addons, requires --blender-exe to be set. eg ```True```
- --help: Show help.

## Packing Tool

```sh
bpy pack <src_dir> <release_dir>
```
Packs addons into ZIP files and automatically names them based on data extracted from the addon bl_info dictionary.<br>
Example resulting name: `My Addon (v1.0.0).zip`
#### Arguments:
- src_dir: Directory where addon sources are located. eg ```MyProject\src```
- release_dir: Directory where archive should be built. eg ```MyProject\releases```

#### Options:
- --excluded-addons: Addon names to be excluded from packing. eg ```Addon1, Addon2```
- --remove-suffixes: File types to be deleted before packing. eg ```.pyc, .txt```
- --help: Show help.

## Config File

All arguments and options can be specified in a ```pyproject.toml``` file, the script looks for this file in the current working directory.

```toml
[tool.bpydevutil]
blender_addons_dir = "Blender\\3.2\\scripts\\addons"
src_dir = "blender-addons\\my-addon\\src"
release_dir = "blender-addons\\my-addon\\release"
remove-suffixes = [".pyc", ".txt"]
blender-exe = "Blender\\blender.exe"
reload-blender = true
```
