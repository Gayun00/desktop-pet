"""
Blender: KayKit Restaurant — 정확한 크기 기반 레스토랑 조립.
바닥 4x4, 벽 4 wide, 카운터 2 wide. Y=depth, Z=up.
Run: blender --background --python scripts/build_restaurant.py
"""
import bpy
import os
import math

bpy.ops.wm.read_factory_settings(use_empty=True)

ASSET_DIR = "/Users/gygygygy/Documents/ai/3d-character/KayKit_Restaurant_Bits_1.0_FREE/Assets/gltf"
OUTPUT = "/Users/gygygygy/Documents/code/ai/desktop-pet/assets/restaurant_level.glb"

def load(name, loc=(0,0,0), rot=(0,0,0)):
    fp = os.path.join(ASSET_DIR, name)
    if not os.path.exists(fp):
        print(f"SKIP: {fp}")
        return
    bpy.ops.import_scene.gltf(filepath=fp)
    imported = bpy.context.selected_objects
    if not imported:
        return
    empty = bpy.data.objects.new("empty", None)
    bpy.context.collection.objects.link(empty)
    empty.location = loc
    empty.rotation_euler = rot
    for obj in imported:
        obj.parent = empty

# Grid: floor is 4x4 units
# Layout: 5 tiles wide (20 units) x 4 tiles deep (16 units)
# Kitchen left, dining right

# === FLOOR (5x4 = 20 tiles) ===
for col in range(5):
    for row in range(4):
        load("floor_kitchen.gltf", loc=(col * 4, row * 4, 0))

# === BACK WALL (z faces +Y direction in blender) ===
for col in range(5):
    load("wall.gltf", loc=(col * 4, 0, 0))

# === LEFT WALL ===
for row in range(4):
    load("wall.gltf", loc=(0, row * 4, 0), rot=(0, 0, math.pi/2))

# === DIVIDER (between kitchen & dining) x=10 ===
load("wall_half.gltf", loc=(10, 0, 0))
load("wall_orderwindow.gltf", loc=(10, 2, 0))
load("wall_half.gltf", loc=(10, 6, 0))

# === RIGHT WALL (dining side) ===
for row in range(4):
    load("wall.gltf", loc=(20, row * 4, 0), rot=(0, 0, math.pi/2))

# === FRONT WALL with door ===
load("wall.gltf", loc=(12, 16, 0))
load("wall_doorway.gltf", loc=(16, 16, 0))

# === KITCHEN (left, 0-10 x, 0-16 y) ===

# Counters along back wall
load("kitchencounter_straight_A_backsplash.gltf", loc=(2, 0.5, 0))
load("kitchencounter_sink_backsplash.gltf", loc=(4, 0.5, 0))
load("kitchencounter_straight_B_backsplash.gltf", loc=(6, 0.5, 0))

# Counters along left wall
load("kitchencounter_straight_A.gltf", loc=(0.5, 4, 0), rot=(0, 0, math.pi/2))
load("kitchencounter_straight_B.gltf", loc=(0.5, 6, 0), rot=(0, 0, math.pi/2))

# Stove on back counter
load("stove_multi_decorated.gltf", loc=(4, 0.8, 0))

# Oven next to stove
load("oven.gltf", loc=(2, 0.8, 0))

# Fridge in corner
load("fridge_A_decorated.gltf", loc=(0.5, 8, 0))

# Extractor hood above stove
load("extractorhood.gltf", loc=(4, 0.8, 2.5))

# Kitchen island
load("kitchentable_A_large.gltf", loc=(5, 6, 0))

# Cutting board + food on island
load("cuttingboard.gltf", loc=(5, 6, 1.0))
load("knife.gltf", loc=(5.4, 6, 1.0))

# Pots on stove
load("pot_A_stew.gltf", loc=(4, 0.8, 1.2))
load("pan_A.gltf", loc=(5, 0.8, 1.2))

# Crates
load("crate_tomatoes.gltf", loc=(8, 2, 0))
load("crate_lettuce.gltf", loc=(8, 4, 0))
load("crate_cheese.gltf", loc=(8, 6, 0))

# Jars on counter
load("jar_A_large.gltf", loc=(2, 0.5, 1.0))
load("jar_B_medium.gltf", loc=(6, 0.5, 1.0))

# Dish rack
load("dishrack_plates.gltf", loc=(6.5, 0.5, 1.0))

# Shelf
load("shelf_papertowel_decorated.gltf", loc=(8, 0.3, 1.5))

# === DINING AREA (right, 10-20 x, 0-16 y) ===

# Table 1 + chairs (center)
load("table_round_A_decorated.gltf", loc=(14, 5, 0))
load("chair_A.gltf", loc=(12.5, 5, 0), rot=(0, 0, math.pi/2))
load("chair_A.gltf", loc=(15.5, 5, 0), rot=(0, 0, -math.pi/2))

# Table 2 + chairs
load("table_round_A_small_decorated.gltf", loc=(14, 9, 0))
load("chair_B.gltf", loc=(12.5, 9, 0), rot=(0, 0, math.pi/2))
load("chair_B.gltf", loc=(15.5, 9, 0), rot=(0, 0, -math.pi/2))

# Table 3 (window seat)
load("table_round_B.gltf", loc=(18, 7, 0))
load("chair_stool.gltf", loc=(17, 7, 0))
load("chair_stool.gltf", loc=(19, 7, 0))

# Food on tables
load("food_burger.gltf", loc=(14, 5, 1.0))
load("food_dinner.gltf", loc=(14, 9, 0.7))
load("food_stew.gltf", loc=(18, 7, 0.7))

# Plates
load("plate.gltf", loc=(13.5, 5, 0.95))
load("bowl.gltf", loc=(14.5, 9, 0.65))

# Condiments
load("ketchup.gltf", loc=(14.5, 5.3, 1.0))
load("mustard.gltf", loc=(13.5, 5.3, 1.0))

# Menu
load("menu.gltf", loc=(15, 9.3, 0.7))

# Pillars
load("pillar_A.gltf", loc=(10, 0, 0))
load("pillar_B.gltf", loc=(10, 12, 0))

# ============================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(
    filepath=OUTPUT,
    export_format='GLB',
    use_selection=True,
    export_apply=True,
)
print(f"\n✅ Exported to: {OUTPUT}")
