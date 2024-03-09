import bpy
import sys
import os
from runScript import tile_path_absolute, source_path_absolute, destination_path_absolute
from math import radians
from random import uniform

print(os.getcwd())



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


### FUNCTIONS TO SCALE HEIGHTS.
"""
# Sets height of obj
def setHeight(obj, set_height):
    minCoords, maxCoords = getMinMaxWorldCoords(obj)
    height = maxCoords[2] - minCoords[2]
    scalingHelper(obj, set_height / height)

# Sets height randomly between given min and max height.
def randomHeight(obj, min_height, max_height):
    setHeight(obj, uniform(min_height, max_height))

# Decreases height to max_height given if the obj height is larger.
def bindHeightUpper(obj, max_height):
    minCoords, maxCoords = getMinMaxWorldCoords(obj)
    height = maxCoords[2] - minCoords[2]
    if height > max_height:
        scalingHelper(obj, max_height / height)

# Increases the height to min_height if the obj height is smaller.
def bindHeightLower(obj, min_height):
    minCoords, maxCoords = getMinMaxWorldCoords(obj)
    height = maxCoords[2] - minCoords[2]
    if height < min_height:
        scalingHelper(obj, min_height / height)
"""
# Helper function to scale obj down and up.
def scalingHelper(obj, scaling_factor):
    for index in range(3):
         obj.scale[index] *= scaling_factor

# General purpose dimension scaler. axis set to 0 for X, 1 for Y, 2 for Z.
def setDimension(obj, set_dimension, axis):
    minCoords, maxCoords = getMinMaxWorldCoords(obj)
    dimension = maxCoords[axis] - minCoords[axis]
    scalingHelper(obj,  set_dimension / dimension)

def randomDimension(obj, min_dimension, max_dimension, axis):
    setDimension(obj, uniform(min_dimension, max_dimension), axis)

# Binds dimension to a max_dimension. 
# I.e. decreases obj dimension to max_dimension if larger.
def bindDimensionUpper(obj, max_dimension, axis):
    minCoords, maxCoords = getMinMaxWorldCoords(obj)
    dimension = maxCoords[axis] - minCoords[axis]
    if dimension > max_dimension:
        scalingHelper(obj, max_dimension / dimension)

# Binds dimension to a min_dimension
# I.e. increases obj dimension to max_dimension if smaller.
def bindDimensionLower(obj, min_dimension, axis):
    minCoords, maxCoords = getMinMaxWorldCoords(obj)
    dimension = maxCoords[axis] - minCoords[axis]
    if dimension < min_dimension:
        scalingHelper(obj, min_dimension / dimension)

# Binds all dimensions to the most restrictice max dimension. 
# Not to confuse with the minMaxCoords.
def bindAllUpper(obj, max_x, max_y, max_z):
    minCoords, maxCoords = getMinMaxWorldCoords(obj)
    obj_dimensions = [maxCoords[i] - minCoords[i] for i in range(3)]
    max_dimensions = [max_x, max_y, max_z]
    scaling_factor = min([max_dimensions[i] / obj_dimensions[i] for i in range(3)])

    if scaling_factor < 1:
        scalingHelper(obj, scaling_factor)

def bindAllLower(obj, min_x, min_y, min_z):
    minCoords, maxCoords = getMinMaxWorldCoords(obj)
    obj_dimensions = [maxCoords[i] - minCoords[i] for i in range(3)]
    min_dimensions = [min_x, min_y, min_z]
    scaling_factor = min([min_dimensions[i] / obj_dimensions[i] for i in range(3)])

    if scaling_factor > 1:
        scalingHelper(obj, scaling_factor)

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

    obj_min_coords, obj_max_coords = getMinMaxWorldCoords(obj)
    obj_center_coords = [(obj_min_coords[i] + obj_max_coords[i]) / 2 for i in range(3)]

    for i in range(2):
        obj.location[i] -= obj_center_coords[i] - binding_center_coords[i]

    # Adjust Z coordinate without margin.
    obj.location[2] -= (obj_min_coords[2] - binding_center_coords[2])
    ### WHY DOES THIS (NOT) WORK?

# Imports the model in source to the copied tile file.
# Places the model on the square tile, then removes it,
# leaving only the hexagonal tile and the source object.
# Exports a .obj file at destination.
def runPlaceObject():
    # Then import the tiles.
    bpy.ops.import_scene.obj(filepath=tile_path_absolute)
    squareTile = bpy.data.objects['squareTile']

    # Import the 3D model and make them a family.
    bpy.ops.import_scene.obj(filepath=source_path_absolute)
    family = bpy.context.selected_objects
    parent_obj = create_family(family)

    # Place the object on the square tile
    placeObjectOn(parent_obj, squareTile, 0.2, True)
    placeObjectOn(parent_obj, squareTile, 0.2, True)

    # Remove the square tile, leaving only the hexagon tile.
    bpy.data.objects.remove(squareTile)

    # Export file as obj.
    bpy.ops.wm.obj_export(filepath=destination_path_absolute)


bpy.ops.wm.obj_export(filepath=destination_path_absolute)