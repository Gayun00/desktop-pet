import bpy
for o in bpy.data.objects:
    if o.type == 'MESH':
        print(f"{o.name:40s} dim=({o.dimensions.x:.2f},{o.dimensions.y:.2f},{o.dimensions.z:.2f}) loc=({o.location.x:.1f},{o.location.y:.1f},{o.location.z:.1f})")
print(f"\nTotal: {len([o for o in bpy.data.objects if o.type=='MESH'])}")
