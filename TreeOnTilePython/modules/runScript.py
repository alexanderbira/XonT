# import function_chest
from shutil import copy
from os.path import abspath
from os import system
import subprocess

function_chest_path_absolute = '/Users/lawanfathullah/Documents/TreeOnTilePython/modules/function_chest.py'
tile_path_absolute = '/Users/lawanfathullah/Documents/TreeOnTilePython/blender_files/baseTile.blend'
copy_path_absolute = '/Users/lawanfathullah/Documents/TreeOnTilePython/blender_files/baseTileCopy.blend'
source_path_absolute = ''
destination_path_absolute = ''

# This runs the script that places the 3D object on the tile.
# For now only configured to return a hexagonal tile as a .obj file.
# source_path is assumed to be a path to a .obj file for now, might be changed later.
# destionation_path MUST be a path to a .obj file.
def runScript(source_path, destination_path):
    copy(tile_path_absolute, copy_path_absolute)
    source_path_absolute = abspath(source_path)
    destination_path = abspath(destination_path)
    # subprocess.call(["blender", tile_path_absolute])
    subprocess.call(["blender", copy_path_absolute, "--python", function_chest_path_absolute])

runScript('./blender_files/Modular Village/Prop_Cart_1.obj', './blender_files/resultThingie.obj')