"""
Blender: 플랫포머 레벨 — 바닥 넓게 + 조형물 90도 회전 복제.
"""
import bpy
import os
import math

bpy.ops.wm.read_factory_settings(use_empty=True)

SRC = "/Users/gygygygy/Documents/ai/3d-character/KayKit_Platformer_Pack_1.0_FREE/Assets/gltf"
OUTPUT_GLB = "/Users/gygygygy/Documents/code/ai/desktop-pet/assets/platformer_level.glb"
OUTPUT_IMG = "/Users/gygygygy/Documents/code/ai/desktop-pet/assets/preview_platformer.png"

def load(color, name, loc=(0,0,0), rot=(0,0,0)):
    fp = os.path.join(SRC, color, name)
    if not os.path.exists(fp):
        return
    bpy.ops.import_scene.gltf(filepath=fp)
    imported = bpy.context.selected_objects
    if not imported:
        return
    empty = bpy.data.objects.new("e", None)
    bpy.context.collection.objects.link(empty)
    empty.location = loc
    empty.rotation_euler = rot
    for obj in imported:
        obj.parent = empty

# ============================================
# BLUE FLOOR — 8x8 grid (32x32 units), 파란 타일로 전부 덮기
# ============================================
for col in range(8):
    for row in range(8):
        load("blue", "platform_4x4x1_blue.gltf", loc=(col*4, row*4, 0))

# ============================================
# ZONE A: 조형물 세트 (왼쪽 앞, 0~16 x, 0~16 y)
# 초록 섬 + 빨간 파이프 + 다리 + 장식
# ============================================

# Green cross island
load("green", "platform_2x2x1_green.gltf", loc=(4, 4, 1))
load("green", "platform_2x2x1_green.gltf", loc=(2, 4, 1))
load("green", "platform_2x2x1_green.gltf", loc=(6, 4, 1))
load("green", "platform_2x2x1_green.gltf", loc=(4, 2, 1))
load("green", "platform_2x2x1_green.gltf", loc=(4, 6, 1))

# Green bigger island
load("green", "platform_2x2x1_green.gltf", loc=(12, 10, 1))
load("green", "platform_2x2x1_green.gltf", loc=(10, 10, 1))
load("green", "platform_2x2x1_green.gltf", loc=(14, 10, 1))
load("green", "platform_2x2x1_green.gltf", loc=(12, 8, 1))
load("green", "platform_2x2x1_green.gltf", loc=(12, 12, 1))
load("green", "platform_2x2x1_green.gltf", loc=(10, 12, 1))
load("green", "platform_2x2x1_green.gltf", loc=(14, 8, 1))

# Red pipes
load("red", "pipe_180_A_red.gltf", loc=(6, 6, 1))
load("red", "pipe_180_B_red.gltf", loc=(8, 8, 1), rot=(0, 0, math.pi/2))
load("red", "pipe_180_A_red.gltf", loc=(10, 14, 1), rot=(0, 0, math.pi))
load("red", "pipe_90_A_red.gltf", loc=(6, 10, 1))

# Bridge + pillars
load("neutral", "pillar_1x1x4.gltf", loc=(2, 14, 0))
load("neutral", "pillar_1x1x4.gltf", loc=(14, 14, 0))
load("neutral", "floor_wood_2x6.gltf", loc=(4, 13.5, 4))
load("neutral", "floor_wood_2x6.gltf", loc=(10, 13.5, 4))

# Diamonds + stars floating
load("blue", "diamond_blue.gltf", loc=(6, 14, 5.5))
load("blue", "diamond_blue.gltf", loc=(10, 14, 5.5))
load("yellow", "star_yellow.gltf", loc=(4, 4, 2.5))
load("yellow", "flag_A_yellow.gltf", loc=(14, 14, 4))

# ============================================
# ZONE B: 조형물 세트 90도 회전 복제 (오른쪽 뒤, 16~32 x, 16~32 y)
# ============================================

# 같은 세트를 offset(20,20)에 90도 회전해서 배치
OX, OY = 20, 20
R = math.pi / 2

# Green cross island (rotated)
load("green", "platform_2x2x1_green.gltf", loc=(OX+4, OY+4, 1))
load("green", "platform_2x2x1_green.gltf", loc=(OX+2, OY+4, 1))
load("green", "platform_2x2x1_green.gltf", loc=(OX+6, OY+4, 1))
load("green", "platform_2x2x1_green.gltf", loc=(OX+4, OY+2, 1))
load("green", "platform_2x2x1_green.gltf", loc=(OX+4, OY+6, 1))

# Green island 2
load("green", "platform_2x2x1_green.gltf", loc=(OX-2, OY-2, 1))
load("green", "platform_2x2x1_green.gltf", loc=(OX-4, OY-2, 1))
load("green", "platform_2x2x1_green.gltf", loc=(OX, OY-2, 1))
load("green", "platform_2x2x1_green.gltf", loc=(OX-2, OY-4, 1))
load("green", "platform_2x2x1_green.gltf", loc=(OX-2, OY, 1))

# Red pipes (rotated layout)
load("red", "pipe_180_A_red.gltf", loc=(OX+6, OY+6, 1), rot=(0, 0, R))
load("red", "pipe_180_B_red.gltf", loc=(OX+2, OY+8, 1), rot=(0, 0, R + math.pi/2))
load("red", "pipe_180_A_red.gltf", loc=(OX-4, OY+2, 1), rot=(0, 0, R + math.pi))
load("red", "pipe_90_A_red.gltf", loc=(OX+2, OY-2, 1), rot=(0, 0, R))

# Bridge
load("neutral", "pillar_1x1x4.gltf", loc=(OX-2, OY+8, 0))
load("neutral", "pillar_1x1x4.gltf", loc=(OX+8, OY+8, 0))
load("neutral", "floor_wood_2x6.gltf", loc=(OX, OY+7.5, 4))
load("neutral", "floor_wood_2x6.gltf", loc=(OX+4, OY+7.5, 4))

# Collectibles
load("blue", "diamond_blue.gltf", loc=(OX+2, OY+8, 5.5))
load("red", "star_red.gltf", loc=(OX+4, OY+4, 2.5))
load("yellow", "flag_A_yellow.gltf", loc=(OX-2, OY+8, 4))

# ============================================
# Extra decorations in open areas
# ============================================
# Cones along paths
for i in range(4):
    load("blue", "cone_blue.gltf", loc=(16, i*4 + 2, 0))
    load("yellow", "cone_yellow.gltf", loc=(i*4 + 2, 16, 0))

# Spring pads
load("green", "spring_pad_green.gltf", loc=(8, 16, 0))
load("blue", "spring_pad_blue.gltf", loc=(16, 8, 0))

# Signs
load("neutral", "sign.gltf", loc=(0, 0, 0))
load("neutral", "sign.gltf", loc=(28, 28, 0), rot=(0, 0, math.pi))

# Stars in the open center area
load("yellow", "star_yellow.gltf", loc=(16, 16, 2))
load("blue", "star_blue.gltf", loc=(12, 20, 2))

# ============================================
# CAMERA + LIGHTING
# ============================================
cam_data = bpy.data.cameras.new("Camera")
cam_data.type = 'PERSP'
cam_data.lens = 35
cam = bpy.data.objects.new("Camera", cam_data)
bpy.context.collection.objects.link(cam)
bpy.context.scene.camera = cam
cam.location = (38, -10, 30)
cam.rotation_euler = (math.radians(55), 0, math.radians(30))

sun = bpy.data.lights.new("Sun", type='SUN')
sun.energy = 4
sun_obj = bpy.data.objects.new("Sun", sun)
bpy.context.collection.objects.link(sun_obj)
sun_obj.location = (16, 16, 20)
sun_obj.rotation_euler = (math.radians(35), math.radians(15), 0)

scene = bpy.context.scene
scene.world = bpy.data.worlds.new("World")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.7, 0.85, 1, 1)

# Render
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 800
scene.render.resolution_y = 600
scene.render.filepath = OUTPUT_IMG
bpy.ops.render.render(write_still=True)
print(f"✅ Preview: {OUTPUT_IMG}")

# Export
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=OUTPUT_GLB, export_format='GLB', use_selection=True, export_apply=True)
print(f"✅ GLB: {OUTPUT_GLB}")
