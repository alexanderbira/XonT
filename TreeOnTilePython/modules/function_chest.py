import bpy
import sys
import os
# from runScript import tile_path_absolute, source_path_absolute, destination_path_absolute
from shutil import copy
from math import radians
from random import uniform

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

# Takes an obj and rotates it and its children in a random angle in the Z axis.
def randomZRotate(obj):
    obj.rotation_euler.z = uniform(0, radians(360))

# Takes an obj and finds it minimum and maximum coordinates
# in the world space. (Accounts for children as well).
# Returns a tuple of two lists. Minimum and maximum coordinates respectively.
def getMinMaxWorldCoords(obj):
    # Get children of obj and put them into a list together.
    family_members = [obj] + list(obj.children)
    # Get all coordinate vectors.
    family_coords = [(member.matrix_world @ v.co)
                     for member in family_members
                     for v in member.data.vertices]

    minCoords = []
    maxCoords = []
    for i in range(3):
        vals = [co[i] for co in family_coords]
        minCoords.append(min(vals))
        maxCoords.append(max(vals))

    return (minCoords, maxCoords)

# Helper function to scale obj down and up.
def scalingHelper(obj, scaling_factor):
    for index in range(3):
         obj.scale[index] *= scaling_factor
    bpy.context.view_layer.update()

# Bind X, Y dimension to the ones of binding_obj with a margin.
# Also centers the obj onto the coordinates of binding_obj in the X, Y plane.
# Burrow parameter decides how deep into the binding_obj the object is placed.???
def placeObjectOn(obj, binding_obj, margin = 0, scaleUp = False):
    binding_min_coords, binding_max_coords = getMinMaxWorldCoords(binding_obj)
    binding_dimensions = [binding_max_coords[i] - binding_min_coords[i] - (2 * margin)
                         for i in range(2)] # Excluding Z coordinate.

    binding_center_coords = [(binding_min_coords[i] + binding_max_coords[i]) / 2
                             for i in range(3)]
    # Add Z coordinate without margins.
    
    
    obj_min_coords, obj_max_coords = getMinMaxWorldCoords(obj)
    obj_dimensions = [obj_max_coords[i] - obj_min_coords[i] for i in range(2)]
    
    scaling_factor = min([binding_dimensions[i] / obj_dimensions[i] for i in range(2)])
    if scaling_factor < 1 or scaleUp:
        scalingHelper(obj, scaling_factor)
        # Update matrix after scaling.
        

    obj_min_coords, obj_max_coords = getMinMaxWorldCoords(obj)
    obj_dimensions = [obj_max_coords[i] - obj_min_coords[i] for i in range(3)]
    obj_center_coords = [(obj_min_coords[i] + obj_max_coords[i]) / 2 for i in range(3)]
    for i in range(2):
        obj.location[i] -= obj_center_coords[i] - binding_center_coords[i]

    # Adjust Z coordinate without margin.
    obj.location[2] -= (obj_min_coords[2] - binding_center_coords[2])
    obj_min_coords, obj_max_coords = getMinMaxWorldCoords(obj)

# Imports the model in source to the copied tile file.
# Places the model on the square tile, then removes it,
# leaving only the hexagonal tile and the source object.
# Exports a .obj file at destination.
def runPlaceObject(src_file, dest_file):
    # Then import the tiles.
    # bpy.ops.import_scene.obj(filepath=tile_path_absolute)
    squareTile = bpy.data.objects['squareTile']

    # Import the 3D model and make them a family.
    bpy.ops.wm.obj_import(filepath=src_file)
    family = bpy.context.selected_objects
    if len(family) > 0:
        parent_obj = create_family(family)
        parent_obj.rotation_euler.x -= radians(90)

        # Place the object on the square tile
        placeObjectOn(parent_obj, squareTile, 0.2, True)


    # Remove the square tile, leaving only the hexagon tile.
    bpy.data.objects.remove(squareTile)

    # Export file as obj.
    bpy.ops.wm.obj_export(filepath=dest_file)

    # sys.exit()

def generate_objs(src_files, dest_files):
    abs_src_files = [os.path.abspath(file_path) for file_path in src_files]
    abs_dest_files = [os.path.abspath(file_path) for file_path in dest_files]

    for i in range(len(abs_src_files)):
        for obj in bpy.data.objects:
            bpy.data.objects.remove(obj)
        bpy.ops.wm.obj_import(filepath=tile_path_relative)
    
        runPlaceObject(abs_src_files[i], abs_dest_files[i])

generate_objs([anyaSrcPath, gigaSrcPath], [anyaDestPath, gigaDestPath])
# generate_objs(src_files, dest_files)