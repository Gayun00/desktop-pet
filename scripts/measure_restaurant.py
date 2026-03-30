"""Measure actual dimensions of each restaurant asset."""
import bpy
import os

ASSET_DIR = "/Users/gygygygy/Documents/ai/3d-character/KayKit_Restaurant_Bits_1.0_FREE/Assets/gltf"

# Key assets to measure
assets = [
    "floor_kitchen.gltf",
    "floor_kitchen_small.gltf",
    "wall.gltf",
    "wall_half.gltf",
    "wall_orderwindow.gltf",
    "kitchencounter_straight_A.gltf",
    "table_round_A.gltf",
    "chair_A.gltf",
    "fridge_A.gltf",
    "stove_multi.gltf",
    "oven.gltf",
    "door_A.gltf",
    "crate.gltf",
    "pillar_A.gltf",
]

for name in assets:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    fp = os.path.join(ASSET_DIR, name)
    if not os.path.exists(fp):
        continue
    bpy.ops.import_scene.gltf(filepath=fp)

    # Get bounding box of all imported objects
    min_x = min_y = min_z = float('inf')
    max_x = max_y = max_z = float('-inf')

    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            for v in obj.bound_box:
                wx, wy, wz = obj.matrix_world @ __import__('mathutils').Vector(v)
                min_x = min(min_x, wx)
                max_x = max(max_x, wx)
                min_y = min(min_y, wy)
                max_y = max(max_y, wy)
                min_z = min(min_z, wz)
                max_z = max(max_z, wz)

    dx = max_x - min_x
    dy = max_y - min_y
    dz = max_z - min_z
    print(f"{name:50s} size=({dx:.2f}, {dy:.2f}, {dz:.2f})")
