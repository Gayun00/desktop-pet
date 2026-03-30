"""
Blender: 레스토랑 조립 + 미리보기 렌더링
"""
import bpy
import os
import math

bpy.ops.wm.read_factory_settings(use_empty=True)

ASSET_DIR = "/Users/gygygygy/Documents/ai/3d-character/KayKit_Restaurant_Bits_1.0_FREE/Assets/gltf"
OUTPUT_GLB = "/Users/gygygygy/Documents/code/ai/desktop-pet/assets/restaurant_level.glb"
OUTPUT_IMG = "/Users/gygygygy/Documents/code/ai/desktop-pet/assets/preview_restaurant.png"

def load(name, loc=(0,0,0), rot=(0,0,0)):
    fp = os.path.join(ASSET_DIR, name)
    if not os.path.exists(fp):
        print(f"SKIP: {name}")
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

# ============================================
# LAYOUT — 컴팩트한 레스토랑 (12x12 유닛)
# 바닥 4x4 타일 기준, 3x3 그리드 = 12x12
# 왼쪽=주방, 오른쪽=다이닝, 앞쪽=열림(캐릭터 진입)
# ============================================

# --- FLOOR 3x3 grid ---
for col in range(3):
    for row in range(3):
        load("floor_kitchen.gltf", loc=(col * 4, row * 4, 0))

# --- WALLS ---
# Back wall (y=0)
load("wall.gltf", loc=(0, -0.25, 0))
load("wall.gltf", loc=(4, -0.25, 0))
load("wall_window_closed.gltf", loc=(8, -0.25, 0))

# Left wall (x=0)
load("wall.gltf", loc=(-0.25, 0, 0), rot=(0, 0, math.pi/2))
load("wall.gltf", loc=(-0.25, 4, 0), rot=(0, 0, math.pi/2))
load("wall_window_open.gltf", loc=(-0.25, 8, 0), rot=(0, 0, math.pi/2))

# Right wall (x=12)
load("wall.gltf", loc=(12.25, 0, 0), rot=(0, 0, math.pi/2))
load("wall_doorway.gltf", loc=(12.25, 4, 0), rot=(0, 0, math.pi/2))
load("wall.gltf", loc=(12.25, 8, 0), rot=(0, 0, math.pi/2))

# Divider wall (x=5, partial)
load("wall_orderwindow.gltf", loc=(5, 4, 0))
load("wall_half.gltf", loc=(5, 2, 0))

# --- KITCHEN (left: x=0~5, y=0~12) ---
# Counters along back wall
load("kitchencounter_straight_A_backsplash.gltf", loc=(1, 0.8, 0))
load("kitchencounter_sink_backsplash.gltf", loc=(3, 0.8, 0))

# Counters along left wall
load("kitchencounter_straight_A.gltf", loc=(0.8, 3, 0), rot=(0, 0, math.pi/2))

# Stove
load("stove_multi_decorated.gltf", loc=(1, 1, 0))

# Fridge
load("fridge_A_decorated.gltf", loc=(0.8, 6, 0))

# Kitchen island
load("kitchentable_A_large.gltf", loc=(2.5, 5, 0))

# Pots on stove
load("pot_A_stew.gltf", loc=(1, 1, 1.2))
load("pan_A.gltf", loc=(2, 1, 1.2))

# Crates along left
load("crate_tomatoes.gltf", loc=(0.8, 8, 0))
load("crate_lettuce.gltf", loc=(0.8, 9.5, 0))

# Extractor hood
load("extractorhood.gltf", loc=(1.5, 1, 2.5))

# Shelf
load("shelf_papertowel_decorated.gltf", loc=(3, 0.3, 1.8))

# Jars
load("jar_A_large.gltf", loc=(1, 0.8, 1.0))
load("jar_B_medium.gltf", loc=(3.5, 0.8, 1.0))

# Dish rack on counter
load("dishrack_plates.gltf", loc=(3, 0.8, 1.0))

# Cutting board on island
load("cuttingboard.gltf", loc=(2.5, 5, 1.0))
load("knife.gltf", loc=(2.8, 5, 1.0))

# --- DINING (right: x=6~12, y=0~12) ---
# Table 1 + chairs (near window)
load("table_round_A_decorated.gltf", loc=(9, 2, 0))
load("chair_A.gltf", loc=(7.8, 2, 0), rot=(0, 0, math.pi/2))
load("chair_A.gltf", loc=(10.2, 2, 0), rot=(0, 0, -math.pi/2))

# Table 2 + chairs (middle)
load("table_round_A_small_decorated.gltf", loc=(9, 6, 0))
load("chair_B.gltf", loc=(7.8, 6, 0), rot=(0, 0, math.pi/2))
load("chair_B.gltf", loc=(10.2, 6, 0), rot=(0, 0, -math.pi/2))

# Table 3 (bar stools, back)
load("table_round_B.gltf", loc=(9, 9.5, 0))
load("chair_stool.gltf", loc=(8, 9.5, 0))
load("chair_stool.gltf", loc=(10, 9.5, 0))

# Food on tables
load("food_burger.gltf", loc=(9, 2, 1.0))
load("food_dinner.gltf", loc=(9, 6, 0.7))
load("food_stew.gltf", loc=(9, 9.5, 0.7))

# Plates/condiments
load("plate.gltf", loc=(8.5, 2, 0.95))
load("bowl.gltf", loc=(9.5, 6, 0.65))
load("ketchup.gltf", loc=(9.5, 2, 1.0))
load("mustard.gltf", loc=(8.5, 2.3, 1.0))
load("menu.gltf", loc=(10, 6, 0.7))

# Pillars
load("pillar_A.gltf", loc=(5, 0, 0))
load("pillar_B.gltf", loc=(5, 8, 0))

# Door
load("door_A.gltf", loc=(12, 5, 0), rot=(0, 0, -math.pi/2))

# ============================================
# CAMERA + RENDER PREVIEW
# ============================================
cam_data = bpy.data.cameras.new("Camera")
cam_data.type = 'PERSP'
cam_data.lens = 35
cam = bpy.data.objects.new("Camera", cam_data)
bpy.context.collection.objects.link(cam)
bpy.context.scene.camera = cam
cam.location = (6, -8, 12)
cam.rotation_euler = (math.radians(50), 0, math.radians(10))

# Lighting
light_data = bpy.data.lights.new("Sun", type='SUN')
light_data.energy = 3
light = bpy.data.objects.new("Sun", light_data)
bpy.context.collection.objects.link(light)
light.location = (6, 6, 10)
light.rotation_euler = (math.radians(30), math.radians(10), 0)

# Render settings
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 800
scene.render.resolution_y = 600
scene.render.filepath = OUTPUT_IMG
bpy.ops.render.render(write_still=True)
print(f"✅ Preview: {OUTPUT_IMG}")

# Export GLB
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(
    filepath=OUTPUT_GLB,
    export_format='GLB',
    use_selection=True,
    export_apply=True,
)
print(f"✅ GLB: {OUTPUT_GLB}")
