"""
Blender: Furniture_FREE.blend의 가구들을 사무실 방 형태로 재배치 → GLB export.
원본 오브젝트는 변형하지 않고 위치만 변경.
"""
import bpy
import math

OUTPUT = "/Users/gygygygy/Documents/code/ai/desktop-pet/assets/office_level.glb"

# 방 크기: 10x8 유닛
# 벽쪽에 가구 배치, 중앙은 비워둠 (캐릭터 이동 공간)

# 재배치 계획:
# 뒷벽 (y=4): TV + 소파 영역 (거실)
# 왼쪽벽 (x=-5): 주방 (싱크, 냉장고, 테이블)
# 오른쪽벽 (x=5): 침실/옷장
# 앞쪽: 열린 공간 + 작은 소품들

layout = {
    # === 거실 (뒷벽) ===
    'tv_wall_001':        (0, 3.5, 0, 0),        # TV 벽 중앙
    'sofa_001':           (0, 1.5, 0, 0),         # 소파 TV 앞
    'coffee_table_001':   (0, 0.5, 0, 0),         # 커피테이블

    # === 주방 (왼쪽) ===
    'kitchen_sink_001':   (-4, 3, 0, math.pi/2),  # 싱크대
    'fridge_001':         (-4, 1.5, 0, math.pi/2),# 냉장고
    'kitchen_table_001':  (-3, -1, 0, 0),         # 주방 테이블
    'kitchen_chair_001':  (-3.8, -1, 0, math.pi/4),# 의자
    'microwave_oven_001': (-4, 2.3, 0.9, math.pi/2),# 전자레인지 (싱크대 위)

    # === 침실/옷장 (오른쪽) ===
    'closet_001':         (4, 3.5, 0, math.pi),   # 옷장
    'bed_001':            (3.5, 1, 0, -math.pi/2),# 침대
    'dresser_001':        (4, -0.5, 0, -math.pi/2),# 서랍장
    'lamp_002':           (4.2, 2.5, 0, 0),       # 스탠드 조명

    # === 사무 공간 (앞쪽 오른쪽) ===
    'office_table_001':   (2.5, -2, 0, 0),        # 사무 테이블
    'lounge_chair_001':   (2.5, -3, 0, 0),        # 의자

    # === 현관/문 ===
    'door_001':           (0, -3.8, 0, 0),        # 문
    'door_frame_001':     (0, -3.8, 0, 0),        # 문틀

    # === 소품 (중앙 근처) ===
    'lamp_001':           (-2, 0.5, 0, 0),        # 작은 조명
    'flower_001':         (1, 0.5, 0.3, 0),       # 꽃
    'musical_instrument_001': (-3, 2, 0, math.pi/6),# 악기
    'toy_001':            (1.5, -1, 0, 0),        # 장난감

    # === 음식/작은 소품 ===
    'drink_001':          (0.3, 0.5, 0.3, 0),     # 음료
    'drink_002':          (-3.2, -1, 0.5, 0),     # 음료2
    'dish_001':           (-2.8, -1, 0.5, 0),     # 접시
    'ketchup_001':        (-2.5, -1, 0.5, 0),     # 케첩
    'coffee_machine_001': (-4, 2.8, 0.9, math.pi/2),# 커피머신

    # === 운동/취미 ===
    'dumbbell_001':       (3, -3, 0.1, 0),        # 덤벨
    'scratching_post_001':(4.2, -2, 0, 0),        # 캣타워
}

# 재배치
for obj in bpy.data.objects:
    if obj.name in layout:
        x, y, z, r = layout[obj.name]
        obj.location = (x, y, z)
        obj.rotation_euler = (0, 0, r)
    elif obj.type == 'MESH' and obj.name not in layout:
        # 사용하지 않는 오브젝트는 숨기기
        # (air_hockey, training items 등은 제외)
        if obj.name not in [o for o in layout]:
            # 화면 밖으로
            obj.location = (100, 100, 0)

# Export
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(
    filepath=OUTPUT,
    export_format='GLB',
    use_selection=True,
    export_apply=True,
)
print(f"\n✅ Exported to: {OUTPUT}")
