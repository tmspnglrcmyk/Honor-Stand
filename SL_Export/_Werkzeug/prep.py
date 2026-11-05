# Lädt Original, wählt Mesh, richtet aus, skaliert gleichmäßig, zentriert, speichert high.blend + high.obj
import bpy, sys, os, json, numpy as np, bmesh
from mathutils import Matrix, Vector
name, src, out = sys.argv[sys.argv.index('--')+1:]
os.makedirs(out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
ext = os.path.splitext(src)[1].lower()
if ext == '.fbx': bpy.ops.import_scene.fbx(filepath=src)
elif ext == '.blend':
    with bpy.data.libraries.load(src) as (a, b): b.objects = a.objects
    for o in b.objects:
        if o: bpy.context.scene.collection.objects.link(o)
meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
pick = {'Axt': 'axe_lp', 'Schild': 'Shield', 'Speer': 'Box.014'}[name]
o = bpy.data.objects[pick]
for x in list(bpy.context.scene.objects):
    if x != o: bpy.data.objects.remove(x, do_unlink=True)
o.parent = None
bpy.context.view_layer.objects.active = o; o.select_set(True)
# Welt-Transform in die Daten übernehmen (Normalen bleiben erhalten)
o.data.transform(o.matrix_world); o.matrix_world = Matrix.Identity(4)
info = {'quelle': src, 'objekt': pick}
v = np.array([list(x.co) for x in o.data.vertices])
if name == 'Speer':
    c = v - v.mean(0); _, _, vt = np.linalg.svd(c, full_matrices=False)
    a0, a1 = vt[0], vt[1]
    p = c @ a0; w = np.abs(c @ a1); L = p.max() - p.min()
    hi = w[p > p.max() - 0.12 * L].max(); lo = w[p < p.min() + 0.12 * L].max()
    if lo > hi: a0 = -a0          # Spitze nach +Z
    a2 = np.cross(a0, a1)
    R = Matrix([list(a1), list(a2), list(a0)])   # Zeilen: neue X,Y,Z
    if R.determinant() < 0: R[0] = -R[0]
    o.data.transform(R.to_4x4())
    v = np.array([list(x.co) for x in o.data.vertices])
    s = 2.2 / (v[:, 2].max() - v[:, 2].min()); info['zielmass'] = 'Länge 2,20 m'
elif name == 'Schild':
    s = 0.85 / (v[:, 0].max() - v[:, 0].min()); info['zielmass'] = 'Durchmesser 0,85 m'
    o.data.transform(Matrix.Rotation(np.pi, 4, 'Z')); info['drehung'] = '180° um Z, Buckel zeigt nach -Y'
else:
    s = 1.0; info['zielmass'] = 'Originalmaß'
o.data.transform(Matrix.Scale(s, 4))
v = np.array([list(x.co) for x in o.data.vertices])
c = (v.min(0) + v.max(0)) / 2
o.data.transform(Matrix.Translation(Vector(-c)))
v = np.array([list(x.co) for x in o.data.vertices])
info['skalierung'] = s; info['masse_m'] = (v.max(0) - v.min(0)).round(4).tolist()
info['dreiecke'] = sum(len(p.vertices) - 2 for p in o.data.polygons)
o.name = name + '_High'; o.data.name = name + '_High'
# UV-Statistik
uv = np.array([d.uv[:] for d in o.data.uv_layers.active.data])
info['uv_bereich'] = [uv.min(0).round(4).tolist(), uv.max(0).round(4).tolist()]
for m in list(o.data.materials): pass
o.data.materials.clear()
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, 'high.blend'))
bpy.ops.wm.obj_export(filepath=os.path.join(out, 'high.obj'), export_selected_objects=True, export_materials=False,
                      export_normals=False, export_uv=True, apply_modifiers=False, forward_axis='Y', up_axis='Z')
json.dump(info, open(os.path.join(out, 'info.json'), 'w'), indent=1, ensure_ascii=False)
print(json.dumps(info, ensure_ascii=False))
