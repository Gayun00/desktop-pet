"""
Blender: 고대 유적 테마 — Package 에셋 배치.
에셋 크기: Temple 4x4x4, Portal 3x3, CrashSite 8x8, Treasure 3x2, Artifacts 11x1x2
"""
import bpy
import os
import math

bpy.ops.wm.read_factory_settings(use_empty=True)

BASE = "/Users/gygygygy/Documents/ai/3d-character"
OUTPUT_GLB = "/Users/gygygygy/Documents/code/ai/desktop-pet/assets/ancient_level.glb"
OUTPUT_IMG = "/Users/gygygygy/Documents/code/ai/desktop-pet/assets/preview_ancient.png"

def load_obj(folder, name, loc=(0,0,0), rot=(0,0,0), scale=1.0):
    fp = os.path.join(BASE, folder, f"{name}.obj")
    if not os.path.exists(fp):
        print(f"SKIP: {fp}")
        return
    bpy.ops.wm.obj_import(filepath=fp)
    imported = bpy.context.selected_objects
    if not imported:
        return
    empty = bpy.data.objects.new("e", None)
    bpy.context.collection.objects.link(empty)
    empty.location = loc
    empty.rotation_euler = rot
    empty.scale = (scale, scale, scale)
    for obj in imported:
        obj.parent = empty

# ============================================
# LAYOUT
# Temple 뒤쪽 중앙 (큼)
# Portal 왼쪽 (3파트 합체)
# CrashSite 오른쪽 (큼)
# Treasure 앞 중앙
# Artifacts 여기저기
# ============================================

# Temple (뒤쪽 중앙)
load_obj("Package", "AncientTemple", loc=(0, 6, 0), scale=1.0)

# Cosmic Portal (왼쪽) — 3파트 같은 위치에
load_obj("Package 2", "AncientCosmicPortal-0-Portal_Stairs", loc=(-6, 0, 0), scale=1.0)
load_obj("Package 2", "AncientCosmicPortal-1-Portal_Rings", loc=(-6, 0, 0), scale=1.0)
load_obj("Package 2", "AncientCosmicPortal-2-Portal_Arch", loc=(-6, 0, 0), scale=1.0)

# Crash Site (오른쪽)
load_obj("Package 4", "AncientCrashSite", loc=(6, 2, 0), scale=0.8)

# Treasure (앞 중앙)
load_obj("Package 3", "AncientTreasure", loc=(0, -3, 0), scale=1.0)

# Artifacts (흩어져)
load_obj("Package 5", "AncientArtifacts-0", loc=(-3, 4, 0), scale=0.5, rot=(0, 0, math.pi/6))
load_obj("Package 5", "AncientArtifacts-1", loc=(3, -1, 0), scale=0.6, rot=(0, 0, -math.pi/4))

# === 바닥 ===
bpy.ops.mesh.primitive_cylinder_add(radius=12, depth=0.4, location=(0, 1, -0.2), vertices=32)
ground = bpy.context.active_object
ground.name = "Ground"
ground.scale = (1, 0.85, 1)
mat_g = bpy.data.materials.new("GroundMat")
mat_g.use_nodes = True
bsdf = mat_g.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.32, 0.28, 0.22, 1)
bsdf.inputs["Roughness"].default_value = 0.95
ground.data.materials.append(mat_g)

# 가장자리
bpy.ops.mesh.primitive_cylinder_add(radius=12.5, depth=0.6, location=(0, 1, -0.4), vertices=16)
edge = bpy.context.active_object
edge.name = "GroundEdge"
edge.scale = (1, 0.85, 1)
mat_e = bpy.data.materials.new("EdgeMat")
mat_e.use_nodes = True
bsdf2 = mat_e.node_tree.nodes["Principled BSDF"]
bsdf2.inputs["Base Color"].default_value = (0.22, 0.18, 0.14, 1)
bsdf2.inputs["Roughness"].default_value = 0.95
edge.data.materials.append(mat_e)

# === CAMERA ===
cam_data = bpy.data.cameras.new("Camera")
cam_data.type = 'PERSP'
cam_data.lens = 30
cam = bpy.data.objects.new("Camera", cam_data)
bpy.context.collection.objects.link(cam)
bpy.context.scene.camera = cam
cam.location = (0, -18, 14)
cam.rotation_euler = (math.radians(50), 0, 0)

# === LIGHTING ===
sun = bpy.data.lights.new("Sun", type='SUN')
sun.energy = 2.5
sun.color = (1, 0.85, 0.65)
sun_obj = bpy.data.objects.new("Sun", sun)
bpy.context.collection.objects.link(sun_obj)
sun_obj.location = (5, -5, 12)
sun_obj.rotation_euler = (math.radians(50), math.radians(10), 0)

# Portal glow
pt = bpy.data.lights.new("PortalLight", type='POINT')
pt.energy = 200
pt.color = (0.2, 1, 0.3)
pt_obj = bpy.data.objects.new("PortalLight", pt)
bpy.context.collection.objects.link(pt_obj)
pt_obj.location = (-6, 0, 3)

# World
scene = bpy.context.scene
scene.world = bpy.data.worlds.new("World")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.12, 0.1, 0.08, 1)

# === RENDER ===
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 800
scene.render.resolution_y = 600
scene.render.filepath = OUTPUT_IMG
bpy.ops.render.render(write_still=True)
print(f"✅ Preview: {OUTPUT_IMG}")

# === EXPORT ===
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(
    filepath=OUTPUT_GLB,
    export_format='GLB',
    use_selection=True,
    export_apply=True,
)
print(f"✅ GLB: {OUTPUT_GLB}")
