"""Forest: vertex color 안 되니까 material 색을 직접 지정."""
import bpy, math, random
random.seed(42)

OUTPUT_GLB = "/Users/gygygygy/Documents/code/ai/desktop-pet/assets/forest_level.glb"

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

# Hide all
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.location = (100, 100, 100)

# Place trees + force green/brown colors
for name, (x, y, z) in tree_layout.items():
    obj = bpy.data.objects.get(name)
    if not obj:
        continue
    obj.location = (x, y, z)
    obj.rotation_euler = (0, 0, random.uniform(0, math.pi * 2))

    # Replace all materials with simple green or brown
    for i, mat in enumerate(obj.data.materials):
        if not mat:
            continue
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        # Remove all nodes except output
        for n in list(nodes):
            if n.type != 'OUTPUT_MATERIAL':
                nodes.remove(n)

        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        output = [n for n in nodes if n.type == 'OUTPUT_MATERIAL'][0]
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

        # Guess color from material name or position
        mname = mat.name.lower()
        if 'trunk' in mname or 'bark' in mname or 'wood' in mname or 'branch' in mname:
            # Brown trunk
            brown = random.uniform(0.3, 0.5)
            bsdf.inputs['Base Color'].default_value = (brown, brown * 0.6, brown * 0.3, 1)
        else:
            # Green foliage (varied greens)
            g = random.uniform(0.3, 0.6)
            bsdf.inputs['Base Color'].default_value = (g * 0.5, g, g * 0.3, 1)
        bsdf.inputs['Roughness'].default_value = 0.85

# Ground
bpy.ops.mesh.primitive_cylinder_add(radius=6, depth=0.5, location=(0, 0.5, -0.25), vertices=32)
g = bpy.context.active_object
g.name = "Ground"
g.scale = (1, 0.8, 1)
mat = bpy.data.materials.new("GroundMat")
mat.use_nodes = True
mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.4, 0.5, 0.25, 1)
mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9
g.data.materials.append(mat)

# Edge
bpy.ops.mesh.primitive_cylinder_add(radius=6.3, depth=0.3, location=(0, 0.5, -0.4), vertices=32)
e = bpy.context.active_object
e.name = "Edge"
e.scale = (1, 0.8, 1)
mat2 = bpy.data.materials.new("EdgeMat")
mat2.use_nodes = True
mat2.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.65, 0.55, 0.4, 1)
mat2.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
e.data.materials.append(mat2)

# Rocks
for i in range(6):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=random.uniform(0.2, 0.5),
        location=(random.uniform(-4, 4), random.uniform(-1.5, 2.5), random.uniform(-0.1, 0.1)))
    r = bpy.context.active_object
    r.scale = (random.uniform(0.8, 1.5), random.uniform(0.8, 1.5), random.uniform(0.5, 0.8))
    r.rotation_euler = (random.uniform(0, 0.3), random.uniform(0, 0.3), random.uniform(0, math.pi * 2))
    mr = bpy.data.materials.new(f"Rock{i}")
    mr.use_nodes = True
    gray = random.uniform(0.5, 0.7)
    mr.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (gray, gray, gray*0.95, 1)
    r.data.materials.append(mr)

# Export
bpy.ops.object.select_all(action='SELECT')
for obj in bpy.data.objects:
    if obj.location.x > 50:
        obj.select_set(False)
bpy.ops.export_scene.gltf(filepath=OUTPUT_GLB, export_format='GLB', use_selection=True, export_apply=True)
print(f"✅ GLB: {OUTPUT_GLB}")
