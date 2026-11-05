import bpy, sys, os
from mathutils import Vector
p = sys.argv[-1]
if p.endswith('.blend'): bpy.ops.wm.open_mainfile(filepath=p)
else:
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.fbx(filepath=p)
print('Szene-Einheiten', bpy.context.scene.unit_settings.system, bpy.context.scene.unit_settings.scale_length)
for o in bpy.data.objects:
    ad = o.asset_data
    if o.type != 'MESH': print(' ', o.type, o.name); continue
    m = o.data; tris = sum(len(q.vertices) - 2 for q in m.polygons)
    cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    dims = [round(max(c[i] for c in cs) - min(c[i] for c in cs), 4) for i in range(3)]
    print(f'  {o.name}: tris={tris} v={len(m.vertices)} dims={dims} mats={[s.material.name if s.material else None for s in o.material_slots]} uv={[u.name for u in m.uv_layers]} mods={[md.type for md in o.modifiers]} parent={o.parent.name if o.parent else None}')
for coll in (bpy.data.objects, bpy.data.materials, bpy.data.meshes, bpy.data.collections):
    for x in coll:
        if x.asset_data: print('ASSET', x.name, 'author=', x.asset_data.author, 'license=', getattr(x.asset_data, 'license', ''), 'copyright=', getattr(x.asset_data, 'copyright', ''), 'desc=', x.asset_data.description)
for im in bpy.data.images:
    fp = bpy.path.abspath(im.filepath) if im.filepath else ''
    print('  IMG', im.name, repr(im.filepath), 'existiert' if fp and os.path.exists(fp) else 'FEHLT', 'packed' if im.packed_file else '')
for m in bpy.data.materials:
    if m.use_nodes: print('  MAT', m.name, [(n.type, n.image.name if getattr(n, 'image', None) else '') for n in m.node_tree.nodes if n.type in ('TEX_IMAGE', 'NORMAL_MAP', 'BSDF_PRINCIPLED', 'SEPARATE_COLOR', 'SEPRGB', 'SEPARATE_RGB')])
