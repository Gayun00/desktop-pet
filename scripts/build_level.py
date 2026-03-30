"""
Blender script to assemble KayKit Platformer assets into a level.
Run: blender --background --python scripts/build_level.py
"""
import bpy
import os
import math

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

ASSET_DIR = "/Users/gygygygy/Documents/ai/3d-character/KayKit_Platformer_Pack_1.0_FREE/Assets/gltf"
OUTPUT = "/Users/gygygygy/Documents/code/ai/desktop-pet/assets/platformer_level.glb"

def load_gltf(filepath, location=(0,0,0), rotation=(0,0,0), scale=1.0):
    """Import a GLTF file and place it."""
    if not os.path.exists(filepath):
        print(f"SKIP: {filepath}")
        return None

    # Import
    bpy.ops.import_scene.gltf(filepath=filepath)

    # Get imported objects
    imported = bpy.context.selected_objects
    if not imported:
        return None

    # Create empty parent
    empty = bpy.data.objects.new("empty", None)
    bpy.context.collection.objects.link(empty)
    empty.location = location
    empty.rotation_euler = rotation
    empty.scale = (scale, scale, scale)

    for obj in imported:
        obj.parent = empty

    return empty

def p(color, name):
    """Shortcut to build asset path."""
    return os.path.join(ASSET_DIR, color, name)

# ============================================
# LEVEL LAYOUT (sample2 inspired)
# ============================================

# --- Yellow floor base (8x6 tiles) ---
# platform_6x6x1 is roughly 6x6x1 units
tile_size = 6  # approximate gltf unit size
for row in range(-1, 2):     # 3 rows deep
    for col in range(-2, 3):  # 5 columns wide
        load_gltf(
            p("yellow", "platform_6x6x1_yellow.gltf"),
            location=(col * tile_size, 0, row * tile_size),
        )

# --- Blue raised structures (back area) ---
# Back wall - row of platforms and barriers
for col in range(-2, 3):
    load_gltf(
        p("blue", "platform_4x4x2_blue.gltf"),
        location=(col * 4, 0, -8),
    )

# Second level platforms
load_gltf(p("blue", "platform_6x6x1_blue.gltf"), location=(-6, 2, -8))
load_gltf(p("blue", "platform_6x6x1_blue.gltf"), location=(0, 2, -8))
load_gltf(p("blue", "platform_6x6x1_blue.gltf"), location=(6, 2, -8))

# Third level (highest, back center)
load_gltf(p("blue", "platform_4x4x1_blue.gltf"), location=(0, 4, -8))

# --- Side walls ---
for row in range(-1, 2):
    load_gltf(p("neutral", "barrier_1x1x4.gltf"), location=(-14, 0, row * 4))
    load_gltf(p("neutral", "barrier_1x1x4.gltf"), location=(14, 0, row * 4))

# --- Blue pipes (arching over center) ---
load_gltf(p("blue", "pipe_straight_A_blue.gltf"), location=(-4, 4, -4), rotation=(0, math.pi/2, 0))
load_gltf(p("blue", "pipe_90_A_blue.gltf"), location=(-6, 4, -2))
load_gltf(p("blue", "pipe_straight_A_blue.gltf"), location=(4, 4, -4), rotation=(0, math.pi/2, 0))
load_gltf(p("blue", "pipe_90_B_blue.gltf"), location=(6, 4, -2))
load_gltf(p("blue", "pipe_180_A_blue.gltf"), location=(0, 6, -6))

# Side pipes
load_gltf(p("blue", "pipe_straight_A_blue.gltf"), location=(-12, 2, 0))
load_gltf(p("blue", "pipe_straight_A_blue.gltf"), location=(12, 2, 0))

# --- Arches ---
load_gltf(p("blue", "arch_blue.gltf"), location=(0, 0, -2))
load_gltf(p("blue", "arch_blue.gltf"), location=(-8, 0, -2))
load_gltf(p("blue", "arch_blue.gltf"), location=(8, 0, -2))

# --- Mid-level platforms (sides) ---
load_gltf(p("blue", "platform_2x2x2_blue.gltf"), location=(-10, 0, -4))
load_gltf(p("blue", "platform_2x2x2_blue.gltf"), location=(10, 0, -4))
load_gltf(p("blue", "platform_4x4x1_blue.gltf"), location=(-10, 0, 2))
load_gltf(p("blue", "platform_4x4x1_blue.gltf"), location=(10, 0, 2))

# --- Railings (front edge) ---
for col in range(-3, 4):
    load_gltf(p("blue", "railing_straight_double_blue.gltf"), location=(col * 4, 0, 8))

# --- Cones (path markers in center walkway) ---
for col in range(-2, 3):
    load_gltf(p("blue", "cone_blue.gltf"), location=(col * 3, 0, 2))
    load_gltf(p("yellow", "cone_yellow.gltf"), location=(col * 3 + 1.5, 0, 2))

# --- Spring pads ---
load_gltf(p("blue", "spring_pad_blue.gltf"), location=(-4, 0, 0))
load_gltf(p("blue", "spring_pad_blue.gltf"), location=(4, 0, 0))
load_gltf(p("green", "spring_pad_green.gltf"), location=(0, 0, 4))

# --- Stars (floating) ---
load_gltf(p("yellow", "star_yellow.gltf"), location=(-6, 6, -6))
load_gltf(p("yellow", "star_yellow.gltf"), location=(6, 6, -6))
load_gltf(p("blue", "star_blue.gltf"), location=(0, 8, -8))
load_gltf(p("red", "star_red.gltf"), location=(0, 5, 0))

# --- Flags ---
load_gltf(p("blue", "flag_A_blue.gltf"), location=(-8, 4, -8))
load_gltf(p("blue", "flag_A_blue.gltf"), location=(8, 4, -8))
load_gltf(p("red", "flag_C_red.gltf"), location=(0, 6, -8))

# --- Hearts & Diamonds ---
load_gltf(p("red", "heart_red.gltf"), location=(-8, 4, 0))
load_gltf(p("blue", "diamond_blue.gltf"), location=(8, 4, 0))

# --- Ball ---
load_gltf(p("neutral", "ball.gltf"), location=(6, 1, 4))

# --- Signs ---
load_gltf(p("neutral", "sign.gltf"), location=(-12, 0, 4))
load_gltf(p("neutral", "signage_finish_wide.gltf"), location=(0, 0, -10))

# ============================================
# EXPORT
# ============================================

# Select all objects
bpy.ops.object.select_all(action='SELECT')

# Export as GLB
bpy.ops.export_scene.gltf(
    filepath=OUTPUT,
    export_format='GLB',
    use_selection=True,
    export_apply=True,
)

print(f"\n✅ Exported to: {OUTPUT}")
