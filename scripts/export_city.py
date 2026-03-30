"""
Blender script: Cartoon City에서 중심 영역의 도로/나무/소품만 추출.
빌딩 제외, 원본 변형 없이 그대로 export.
Run: blender --background Cartoon_City_Free.blend --python scripts/export_city.py
"""
import bpy

OUTPUT = "/Users/gygygygy/Documents/code/ai/desktop-pet/assets/city_level.glb"

# 제외할 오브젝트 (큰 빌딩, 빌보드 등)
EXCLUDE_PREFIXES = [
    "Billboard",
    "Eco_Building",
    "Regular_Building",
    "Signboard",
    "Graffiti",
    "Spotlight",
]

# 포함할 오브젝트 (도로, 나무, 소품 등)
INCLUDE_PREFIXES = [
    "road",
    "Bush",
    "Palm",
    "Car_",
    "Van",
    "Futuristic_Car",
    "Bus_Stop",
    "Fountain",
    "traffic_light",
    "Trash_Can",
    "Trash_0",
    "Set_B_Tiles",
]

# 영역 제한 (중심 근처만)
BOUNDS = 35  # -35 ~ 35 범위

# 모두 선택 해제
bpy.ops.object.select_all(action='DESELECT')

selected_count = 0
skipped_building = 0
skipped_bounds = 0

for obj in bpy.data.objects:
    name = obj.name

    # 제외 대상 체크
    excluded = False
    for prefix in EXCLUDE_PREFIXES:
        if name.startswith(prefix):
            excluded = True
            skipped_building += 1
            break

    if excluded:
        obj.select_set(False)
        continue

    # 포함 대상 체크
    included = False
    for prefix in INCLUDE_PREFIXES:
        if name.startswith(prefix):
            included = True
            break

    if not included:
        obj.select_set(False)
        continue

    # 영역 체크
    x, y, z = obj.location
    if abs(x) > BOUNDS or abs(y) > BOUNDS:
        skipped_bounds += 1
        obj.select_set(False)
        continue

    # 선택!
    obj.select_set(True)
    selected_count += 1

print(f"\n=== Export Summary ===")
print(f"Selected: {selected_count}")
print(f"Skipped (building): {skipped_building}")
print(f"Skipped (out of bounds): {skipped_bounds}")

# Export
bpy.ops.export_scene.gltf(
    filepath=OUTPUT,
    export_format='GLB',
    use_selection=True,
    export_apply=True,
)

print(f"\n✅ Exported to: {OUTPUT}")
