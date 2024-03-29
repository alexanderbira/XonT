import bpy
import os
<<<<<<<< HEAD:TreeOnTilePython/modules/function_chest.py
========
# from runScript import tile_path_absolute, source_path_absolute, destination_path_absolute
from shutil import copy
>>>>>>>> origin/main:compose_objects/modules/messy_function_chest.py
from math import radians

<<<<<<<< HEAD:TreeOnTilePython/modules/function_chest.py
# Loading source paths and destination paths.
src_model_dir = os.path.abspath('images/models')
dest_model_dir = os.path.abspath('images/tiles')
src_paths = ['images/models' + file_name for file_name in os.listdir(src_model_dir)]
dest_paths = ['images/tiles' + file_name for file_name in os.listdir(src_model_dir)]
# Path to base tile.
tile_path = os.path.abspath('TreeOnTilePython/baseTiles/baseTile.obj')

========
# src_model_dir = os.path.abspath('images/models')
# dest_model_dir = os.path.abspath('images/tiles')
# src_files = ['images/models' + file_name for file_name in os.listdir(src_model_dir)]
# dest_files = ['images/tiles' + file_name for file_name in os.listdir(src_model_dir)]

tile_path_relative = os.path.abspath('TreeOnTilePython/blender_files/baseTiles/baseTile.obj')
anyaSrcPath = 'TreeOnTilePython/blender_files/objFromAI/anya.obj'
anyaDestPath = 'TreeOnTilePython/blender_files/objFromAI/anyaOutput.obj'
gigaSrcPath = 'TreeOnTilePython/blender_files/objFromAI/gigaLawn.obj'
gigaDestPath = 'TreeOnTilePython/blender_files/objFromAI/gigaOutput.obj'


# test_source = str(input("Enter path to object source: "))
# test_dest = str(input("Enter path to destination: "))

# test_source = '/Users/lawanfathullah/Documents/TreeOnTilePython/blender_files/anya.obj'
# test_dest = './blender_files/resultThingie.obj'

>>>>>>>> origin/main:compose_objects/modules/messy_function_chest.py
#####################################
#####################################

# This function takes a collection of objs (e.g. bpy.data.objs)
# and sets the first objeect to be a parent of all others.
# Returns a reference to the parent obj.
def create_family(family_members):
    parent_obj = family_members[0]
    for child_obj in family_members[1:]:
        child_obj.parent = parent_obj
        # To prevent the children from moving in the world space.
        child_obj.matrix_parent_inverse = parent_obj.matrix_world.inverted()

    return parent_obj

# Takes an obj and finds it minimum and maximum coordinates
# in the world space. (Accounts for children as well).
# Returns a tuple of two lists. Minimum and maximum coordinates respectively,
# in the format of [X, Y, Z].
def get_min_max_world_coords(obj):
    # Get children of obj and put them into a list together.
    family_members = [obj] + list(obj.children)
    # Get all coordinate vectors.
    family_coords = [(member.matrix_world @ v.co)
                     for member in family_members
                     for v in member.data.vertices]

    min_coords = []
    max_coords = []

    # Append minimum and maximum coordinates to the arrays.
    for i in range(3):
        vals = [co[i] for co in family_coords]
        min_coords.append(min(vals))
        max_coords.append(max(vals))

    return (min_coords, max_coords)

<<<<<<<< HEAD:TreeOnTilePython/modules/function_chest.py
========

>>>>>>>> origin/main:compose_objects/modules/messy_function_chest.py
# Helper function to scale obj down and up.
def scaling_helper(obj, scaling_factor):
    for index in range(3):
         obj.scale[index] *= scaling_factor
<<<<<<<< HEAD:TreeOnTilePython/modules/function_chest.py
    # Update matrix.
========
>>>>>>>> origin/main:compose_objects/modules/messy_function_chest.py
    bpy.context.view_layer.update()


# Bind X, Y dimensions of obj to the ones of binding_obj with a margin.
# Also centers the obj onto the coordinates of binding_obj in the X, Y plane.
# Puts the bottom of the obj at the center of binding_obj
def place_obj_on(obj, binding_obj, margin = 0, scaleUp = False):
    binding_min_coords, binding_max_coords = get_min_max_world_coords(binding_obj)
    binding_dimensions = [binding_max_coords[i] - binding_min_coords[i] - (2 * margin)
                         for i in range(2)] # Excluding Z coordinate.
    binding_center_coords = [(binding_min_coords[i] + binding_max_coords[i]) / 2
                             for i in range(3)]
    
    obj_min_coords, obj_max_coords = get_min_max_world_coords(obj)
    obj_dimensions = [obj_max_coords[i] - obj_min_coords[i] for i in range(2)]
    
    scaling_factor = min([binding_dimensions[i] / obj_dimensions[i] for i in range(2)])
    if scaling_factor < 1 or scaleUp:
<<<<<<<< HEAD:TreeOnTilePython/modules/function_chest.py
        scaling_helper(obj, scaling_factor)
        
        # Update values of object.
        obj_min_coords, obj_max_coords = get_min_max_world_coords(obj)
        obj_center_coords = [(obj_min_coords[i] + obj_max_coords[i]) / 2 for i in range(3)]

    # Center obj on binding_obj with respect to XY plane.
    for i in range(2):
        obj.location[i] -= obj_center_coords[i] - binding_center_coords[i]

    # Adjust Z coordinate separately as obj is put ON TOP of binding_obj.
    obj.location[2] -= (obj_min_coords[2] - binding_center_coords[2])
    obj_min_coords, obj_max_coords = get_min_max_world_coords(obj)

    # Update matrix.
    bpy.context.view_layer.update()
========
        scalingHelper(obj, scaling_factor)

    obj_min_coords, obj_max_coords = getMinMaxWorldCoords(obj)
    obj_dimensions = [obj_max_coords[i] - obj_min_coords[i] for i in range(3)]
    obj_center_coords = [(obj_min_coords[i] + obj_max_coords[i]) / 2 for i in range(3)]
    for i in range(2):
        obj.location[i] -= obj_center_coords[i] - binding_center_coords[i]

    # Adjust Z coordinate without margin.
    
    obj.location[2] -= (obj_center_coords[2] - binding_center_coords[2])
    obj.location[2] += obj_dimensions[2] / 2
    obj_min_coords, obj_max_coords = getMinMaxWorldCoords(obj)
    bpy.context.view_layer.update()
    ### WHY DOES THIS (NOT) WORK?
>>>>>>>> origin/main:compose_objects/modules/messy_function_chest.py

# Imports the model in source to the copied tile file.
# Places the model on the square tile, then removes it,
# leaving only the hexagonal tile and the source object.
# Exports a .obj file at destination.
<<<<<<<< HEAD:TreeOnTilePython/modules/function_chest.py
def run_place_obj(src_file, dest_file):
========
def runPlaceObject(src_file, dest_file):
>>>>>>>> origin/main:compose_objects/modules/messy_function_chest.py
    # Then import the tiles.
    # bpy.ops.import_scene.obj(filepath=tile_path_absolute)
    square_tile = bpy.data.objects['squareTile']

    # Import the 3D model and make them a family.
    bpy.ops.wm.obj_import(filepath=src_file)
    family = bpy.context.selected_objects
    if len(family) > 0:
        parent_obj = create_family(family)
        parent_obj.rotation_euler.x -= radians(90)
        bpy.context.view_layer.update()

        # Place the object on the square tile
        place_obj_on(parent_obj, square_tile, 0.2, True)


    # Remove the square tile, leaving only the hexagon tile.
    bpy.data.objects.remove(square_tile)

    # Export file as obj.
    bpy.ops.wm.obj_export(filepath=dest_file)

    # sys.exit()

<<<<<<<< HEAD:TreeOnTilePython/modules/function_chest.py
# Takes a list of source file paths and destination file paths,
# then generates "X on Tile" at the destination file paths for each
# source file.
========
>>>>>>>> origin/main:compose_objects/modules/messy_function_chest.py
def generate_objs(src_files, dest_files):
    abs_src_files = [os.path.abspath(file_path) for file_path in src_files]
    abs_dest_files = [os.path.abspath(file_path) for file_path in dest_files]

    for i in range(len(abs_src_files)):
        for obj in bpy.data.objects:
            bpy.data.objects.remove(obj)
<<<<<<<< HEAD:TreeOnTilePython/modules/function_chest.py
        bpy.ops.wm.obj_import(filepath=tile_path)
    
        run_place_obj(abs_src_files[i], abs_dest_files[i])

generate_objs(src_paths, dest_paths)
========
        bpy.ops.wm.obj_import(filepath=tile_path_relative)
    
        runPlaceObject(abs_src_files[i], abs_dest_files[i])

# generate_objs([anyaSrcPath, gigaSrcPath], [anyaDestPath, gigaDestPath])
# generate_objs(src_files, dest_files)
>>>>>>>> origin/main:compose_objects/modules/messy_function_chest.py
