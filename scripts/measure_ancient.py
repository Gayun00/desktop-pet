import bpy, os, mathutils
BASE = "/Users/gygygygy/Documents/ai/3d-character"
files = [
    ("Package", "AncientTemple.obj"),
    ("Package 2", "AncientCosmicPortal-0-Portal_Stairs.obj"),
    ("Package 3", "AncientTreasure.obj"),
    ("Package 4", "AncientCrashSite.obj"),
    ("Package 5", "AncientArtifacts-0.obj"),
]
for folder, name in files:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    fp = os.path.join(BASE, folder, name)
    bpy.ops.wm.obj_import(filepath=fp)
    min_v = [float('inf')]*3
    max_v = [float('-inf')]*3
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            for v in obj.bound_box:
                wv = obj.matrix_world @ mathutils.Vector(v)
                for i in range(3):
                    min_v[i] = min(min_v[i], wv[i])
                    max_v[i] = max(max_v[i], wv[i])
    dx = max_v[0]-min_v[0]
    dy = max_v[1]-min_v[1]
    dz = max_v[2]-min_v[2]
    print(f"{name:50s} size=({dx:.1f}, {dy:.1f}, {dz:.1f})")
