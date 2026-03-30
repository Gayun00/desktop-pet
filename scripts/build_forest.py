"""
Blender: LowPolyTreePack — vertex color를 material에 연결하여 export.
"""
import bpy
import math
import random

OUTPUT_GLB = "/Users/gygygygy/Documents/code/ai/desktop-pet/assets/forest_level.glb"
OUTPUT_IMG = "/Users/gygygygy/Documents/code/ai/desktop-pet/assets/preview_forest.png"

random.seed(42)

# 사용할 나무 + 위치
tree_layout = {
    'Tree Type1 05 Model': (0, 1, 0),
    'Tree Type1 04 Model': (-2.5, 2, 0),
    'Tree Type3 04 Model': (2, 2.5, 0),
    'Tree Type4 04 Model': (3.5, 1, 0),
    'Tree Type2 03 Model': (-3.5, 0, 0),
    'Tree Type3 03 Model': (-1, -0.5, 0),
    'Tree Type5 03 Model': (1.5, -0.5, 0),
    'Tree Type6 03 Model': (4, -0.5, 0),
    'Tree Type1 01 Model': (-2, -1.5, 0),
    'Tree Type2 01 Model': (0.5, -2, 0),
    'Tree Type4 01 Model': (3, -1.5, 0),
    'Tree Type6 01 Model': (-4, -1, 0),
    'Tree Type7 01 Model': (5, 0.5, 0),
    'Tree Type5 01 Model': (-1.5, 1.5, 0),
    'Tree Type0 05 Model': (1, 3, 0),
}

# 모든 오브젝트 숨기기
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.location = (100, 100, 100)

# 선택한 나무만 배치
for name, (x, y, z) in tree_layout.items():
    obj = bpy.data.objects.get(name)
    if obj:
        obj.location = (x, y, z)
        obj.rotation_euler = (0, 0, random.uniform(0, math.pi * 2))

# === Vertex color → Material 연결 ===
# 나무 모델들이 vertex color를 가지고 있으면 material에 연결
for obj in bpy.data.objects:
    if obj.type == 'MESH' and obj.location.x < 50:  # 숨기지 않은 것만
        mesh = obj.data
        if mesh.vertex_colors:
            # 기존 material이 있으면 vertex color 노드 연결
            if not obj.data.materials:
                mat = bpy.data.materials.new(f"VCol_{obj.name}")
                mat.use_nodes = True
                obj.data.materials.append(mat)

            for mat in obj.data.materials:
                if mat and mat.use_nodes:
                    nodes = mat.node_tree.nodes
                    links = mat.node_tree.links

                    # Check if already has vertex color node
                    has_vcol = any(n.type == 'VERTEX_COLOR' for n in nodes)
                    if has_vcol:
                        continue

                    # Find principled BSDF
                    bsdf = None
                    for n in nodes:
                        if n.type == 'BSDF_PRINCIPLED':
                            bsdf = n
                            break

                    if bsdf:
                        vcol = nodes.new('ShaderNodeVertexColor')
                        vcol.layer_name = mesh.vertex_colors[0].name
                        links.new(vcol.outputs['Color'], bsdf.inputs['Base Color'])
        elif obj.data.materials:
            # No vertex colors but has materials — keep as is
            pass

# === 바닥 ===
bpy.ops.mesh.primitive_cylinder_add(radius=6, depth=0.5, location=(0, 0.5, -0.25), vertices=32)
ground = bpy.context.active_object
ground.name = "Ground"
ground.scale = (1, 0.8, 1)
mat_ground = bpy.data.materials.new("Ground")
mat_ground.use_nodes = True
bsdf = mat_ground.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.45, 0.55, 0.3, 1)
bsdf.inputs["Roughness"].default_value = 0.9
ground.data.materials.append(mat_ground)

# 가장자리
bpy.ops.mesh.primitive_cylinder_add(radius=6.3, depth=0.3, location=(0, 0.5, -0.4), vertices=32)
edge = bpy.context.active_object
edge.name = "GroundEdge"
edge.scale = (1, 0.8, 1)
mat_edge = bpy.data.materials.new("GroundEdge")
mat_edge.use_nodes = True
bsdf2 = mat_edge.node_tree.nodes["Principled BSDF"]
bsdf2.inputs["Base Color"].default_value = (0.7, 0.6, 0.45, 1)
bsdf2.inputs["Roughness"].default_value = 0.95
edge.data.materials.append(mat_edge)

# 바위
for i in range(6):
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=1,
        radius=random.uniform(0.2, 0.5),
        location=(random.uniform(-4, 4), random.uniform(-1.5, 2.5), random.uniform(-0.1, 0.1))
    )
    rock = bpy.context.active_object
    rock.name = f"Rock_{i}"
    rock.scale = (random.uniform(0.8, 1.5), random.uniform(0.8, 1.5), random.uniform(0.5, 0.8))
    rock.rotation_euler = (random.uniform(0, 0.3), random.uniform(0, 0.3), random.uniform(0, math.pi * 2))
    mat_rock = bpy.data.materials.new(f"Rock_{i}")
    mat_rock.use_nodes = True
    bsdf_r = mat_rock.node_tree.nodes["Principled BSDF"]
    gray = random.uniform(0.5, 0.75)
    bsdf_r.inputs["Base Color"].default_value = (gray, gray, gray * 0.95, 1)
    bsdf_r.inputs["Roughness"].default_value = 0.9
    rock.data.materials.append(mat_rock)

# === CAMERA ===
cam_data = bpy.data.cameras.new("Camera")
cam_data.type = 'PERSP'
cam_data.lens = 50
cam = bpy.data.objects.new("Camera", cam_data)
bpy.context.collection.objects.link(cam)
bpy.context.scene.camera = cam
cam.location = (0, -10, 6)
cam.rotation_euler = (math.radians(60), 0, 0)

# === LIGHTING ===
sun = bpy.data.lights.new("Sun", type='SUN')
sun.energy = 4
sun_obj = bpy.data.objects.new("Sun", sun)
bpy.context.collection.objects.link(sun_obj)
sun_obj.location = (5, -5, 10)
sun_obj.rotation_euler = (math.radians(40), math.radians(15), 0)

scene = bpy.context.scene
scene.world = bpy.data.worlds.new("World")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.82, 0.88, 0.93, 1)

# === RENDER ===
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 800
scene.render.resolution_y = 600
scene.render.filepath = OUTPUT_IMG
bpy.ops.render.render(write_still=True)
print(f"✅ Preview: {OUTPUT_IMG}")

# === EXPORT ===
bpy.ops.object.select_all(action='SELECT')
for obj in bpy.data.objects:
    if obj.location.x > 50:
        obj.select_set(False)

bpy.ops.export_scene.gltf(
    filepath=OUTPUT_GLB,
    export_format='GLB',
    use_selection=True,
    export_apply=True,
    export_materials='EXPORT',
)
print(f"✅ GLB: {OUTPUT_GLB}")
