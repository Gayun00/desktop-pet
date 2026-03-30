"""
Blender: Furniture_FREE.blend 가구를 사무실/거실 스타일로 배치.
벽 없이 바닥만 깔고, 구역별로 가구 배치. 미리보기 렌더링 포함.
"""
import bpy
import math

OUTPUT_GLB = "/Users/gygygygy/Documents/code/ai/desktop-pet/assets/office_level.glb"
OUTPUT_IMG = "/Users/gygygygy/Documents/code/ai/desktop-pet/assets/preview_office.png"

# === 가구 재배치 ===
# 원본 변형 없이 위치만 변경
# 공간: 대략 10x8 유닛, 중앙 통로 확보
#
# 레이아웃:
#   뒤쪽(y=3~4): TV벽 + 소파 (거실 구역)
#   왼쪽(x=-4): 주방 (싱크, 냉장고)
#   오른쪽(x=3~4): 사무 구역 (책상, 의자)
#   중앙: 커피테이블 + 열린 공간

layout = {
    # === 거실 (뒤쪽 중앙) ===
    'tv_wall_001':        {'loc': (0, 3.8, 0), 'rot': (0, 0, math.pi)},
    'sofa_001':           {'loc': (0, 2, 0), 'rot': (0, 0, 0)},
    'coffee_table_001':   {'loc': (0, 1, 0), 'rot': (0, 0, 0)},
    'lamp_001':           {'loc': (-1.8, 2.5, 0), 'rot': (0, 0, 0)},
    'lounge_chair_001':   {'loc': (-2.2, 1.5, 0), 'rot': (0, 0, math.pi/4)},

    # === 사무 구역 (오른쪽) ===
    'office_table_001':   {'loc': (3.5, 2.5, 0), 'rot': (0, 0, -math.pi/2)},
    'lamp_002':           {'loc': (4.5, 2.5, 0), 'rot': (0, 0, 0)},
    'musical_instrument_001': {'loc': (4, 0, 0), 'rot': (0, 0, -math.pi/4)},

    # === 주방 (왼쪽) ===
    'kitchen_sink_001':   {'loc': (-4, 3, 0), 'rot': (0, 0, math.pi/2)},
    'fridge_001':         {'loc': (-4, 1, 0), 'rot': (0, 0, math.pi/2)},
    'kitchen_table_001':  {'loc': (-3, -1.5, 0), 'rot': (0, 0, 0)},
    'kitchen_chair_001':  {'loc': (-2.2, -1.5, 0), 'rot': (0, 0, math.pi/3)},
    'microwave_oven_001': {'loc': (-4, 2, 0.9), 'rot': (0, 0, math.pi/2)},

    # === 침실 (뒤쪽 오른쪽) ===
    'bed_001':            {'loc': (4, -2, 0), 'rot': (0, 0, 0)},
    'dresser_001':        {'loc': (3, -3, 0), 'rot': (0, 0, 0)},
    'closet_001':         {'loc': (4.5, 3.8, 0), 'rot': (0, 0, math.pi)},

    # === 소품 (중앙/여기저기) ===
    'flower_001':         {'loc': (0.5, 1, 0.3), 'rot': (0, 0, 0)},
    'toy_001':            {'loc': (-1, -1, 0), 'rot': (0, 0, 0)},
    'drink_001':          {'loc': (0.2, 1, 0.3), 'rot': (0, 0, 0)},
    'drink_002':          {'loc': (-2.8, -1.5, 0.5), 'rot': (0, 0, 0)},
    'dish_001':           {'loc': (-2.5, -1.5, 0.5), 'rot': (0, 0, 0)},
    'coffee_machine_001': {'loc': (-4, 2.3, 0.9), 'rot': (0, 0, math.pi/2)},
    'ketchup_001':        {'loc': (-3.3, -1.5, 0.5), 'rot': (0, 0, 0)},
    'dish_002':           {'loc': (-3, -1.5, 0.5), 'rot': (0, 0, 0)},
    'box_001':            {'loc': (3.5, -3, 0), 'rot': (0, 0, 0)},
    'scratching_post_001':{'loc': (2, 3.5, 0), 'rot': (0, 0, 0)},

    # === 현관 ===
    'door_001':           {'loc': (0, -3.5, 0), 'rot': (0, 0, 0)},
    'door_frame_001':     {'loc': (0, -3.5, 0), 'rot': (0, 0, 0)},
    'clothes_001':        {'loc': (-1.5, -3, 1), 'rot': (0, 0, 0)},

    # === 운동 ===
    'dumbbell_001':       {'loc': (2, -2, 0.1), 'rot': (0, 0, 0)},
    'dumbbell_002':       {'loc': (2, -2.3, 0.1), 'rot': (0, 0, 0)},
}

# 사용하지 않는 오브젝트 (너무 큰 것들)
HIDE = ['air_hockey_001', 'training_item_001', 'training_item_002',
        'toy_002', 'washing_machine_001', 'camera_001', 'clothes_002',
        'bathroom_item_001', 'closet_002']

for obj in bpy.data.objects:
    if obj.name in layout:
        cfg = layout[obj.name]
        obj.location = cfg['loc']
        obj.rotation_euler = cfg['rot']
    elif obj.name in HIDE:
        obj.location = (100, 100, 100)
    elif obj.type == 'MESH' and obj.name not in layout and obj.name not in HIDE:
        # 정의 안 된 오브젝트는 숨김
        found = False
        for k in layout:
            if obj.name == k:
                found = True
                break
        if not found:
            obj.location = (100, 100, 100)

# === 바닥 추가 (단순 평면) ===
bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, -0.01))
floor = bpy.context.active_object
floor.name = "Floor"
mat = bpy.data.materials.new("FloorMat")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.76, 0.68, 0.55, 1)  # 밝은 나무색
bsdf.inputs["Roughness"].default_value = 0.8
floor.data.materials.append(mat)

# === CAMERA ===
cam_data = bpy.data.cameras.new("Camera")
cam_data.type = 'PERSP'
cam_data.lens = 30
cam = bpy.data.objects.new("Camera", cam_data)
bpy.context.collection.objects.link(cam)
bpy.context.scene.camera = cam
cam.location = (0, -10, 10)
cam.rotation_euler = (math.radians(50), 0, 0)

# === LIGHTING ===
sun = bpy.data.lights.new("Sun", type='SUN')
sun.energy = 3
sun_obj = bpy.data.objects.new("Sun", sun)
bpy.context.collection.objects.link(sun_obj)
sun_obj.location = (3, -3, 8)
sun_obj.rotation_euler = (math.radians(40), math.radians(15), 0)

# Ambient fill
fill = bpy.data.lights.new("Fill", type='AREA')
fill.energy = 50
fill.size = 10
fill_obj = bpy.data.objects.new("Fill", fill)
bpy.context.collection.objects.link(fill_obj)
fill_obj.location = (0, 0, 6)

# === RENDER ===
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 800
scene.render.resolution_y = 600
scene.render.filepath = OUTPUT_IMG
scene.world = bpy.data.worlds.new("World")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.85, 0.9, 0.95, 1)
bpy.ops.render.render(write_still=True)
print(f"✅ Preview: {OUTPUT_IMG}")

# === EXPORT (floor 포함) ===
bpy.ops.object.select_all(action='SELECT')
# 숨긴 오브젝트 제외
for obj in bpy.data.objects:
    if obj.location.x > 50:
        obj.select_set(False)

bpy.ops.export_scene.gltf(
    filepath=OUTPUT_GLB,
    export_format='GLB',
    use_selection=True,
    export_apply=True,
)
print(f"✅ GLB: {OUTPUT_GLB}")
