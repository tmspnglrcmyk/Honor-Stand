# Nachtrags-Schild: Teile mit Smooth-by-Angle anwenden, zu einem Objekt vereinen, Buckel nach -Y, 0,85 m, zentriert
import bpy, sys, os, json, numpy as np
from mathutils import Matrix, Vector
src, out, ziel = sys.argv[sys.argv.index('--')+1:]
os.makedirs(out, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=src)
ms = [o for o in bpy.data.objects if o.type == 'MESH']
for o in ms:
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active = o
    for md in list(o.modifiers): bpy.ops.object.modifier_apply(modifier=md.name)
    o.data.transform(o.matrix_world); o.matrix_world = Matrix.Identity(4); o.parent = None
boss = np.array([v.co[:] for v in bpy.data.objects['shield_center_low'].data.vertices])
board = np.array([v.co[:] for v in bpy.data.objects['shield_wooden_base_low'].data.vertices])
info = dict(quelle=src)
# Dicke-Achse = kleinste Ausdehnung des Bretts
ax = int(np.argmin(board.max(0) - board.min(0))); info['dickenachse'] = ax
bpy.ops.object.select_all(action='DESELECT')
for o in ms: o.select_set(True)
bpy.context.view_layer.objects.active = ms[0]; bpy.ops.object.join(); o = bpy.context.view_layer.objects.active
for x in list(bpy.data.objects):
    if x != o: bpy.data.objects.remove(x, do_unlink=True)
R = Matrix.Identity(4)
if ax == 2: R = Matrix.Rotation(np.pi / 2, 4, 'X')
elif ax == 0: R = Matrix.Rotation(np.pi / 2, 4, 'Z')
o.data.transform(R)
V = np.array([v.co[:] for v in o.data.vertices]); c = (V.min(0) + V.max(0)) / 2
bc = (np.array(R.to_3x3()) @ boss.mean(0))
if bc[1] > c[1]: o.data.transform(Matrix.Rotation(np.pi, 4, 'Z')); info['drehung_z'] = 180
V = np.array([v.co[:] for v in o.data.vertices]); s = float(ziel) / (V[:, 0].max() - V[:, 0].min())
o.data.transform(Matrix.Scale(s, 4)); V = np.array([v.co[:] for v in o.data.vertices]); c = (V.min(0) + V.max(0)) / 2
o.data.transform(Matrix.Translation(Vector(-c))); V = np.array([v.co[:] for v in o.data.vertices])
info.update(skalierung=s, zielmass='Durchmesser %.2f m' % float(ziel), masse_m=(V.max(0) - V.min(0)).round(4).tolist(), dreiecke=sum(len(p.vertices) - 2 for p in o.data.polygons))
o.name = 'Schild_High'; o.data.name = 'Schild_High'; o.data.materials.clear()
uv = np.array([d.uv[:] for d in o.data.uv_layers.active.data]); info['uv_bereich'] = [uv.min(0).round(4).tolist(), uv.max(0).round(4).tolist()]
for im in list(bpy.data.images): bpy.data.images.remove(im)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, 'high.blend'))
bpy.ops.object.select_all(action='DESELECT'); o.select_set(True)
bpy.ops.wm.obj_export(filepath=os.path.join(out, 'high.obj'), export_selected_objects=True, export_materials=False, export_normals=False, export_uv=True, forward_axis='Y', up_axis='Z')
json.dump(info, open(os.path.join(out, 'info.json'), 'w'), indent=1, ensure_ascii=False); print(info)
