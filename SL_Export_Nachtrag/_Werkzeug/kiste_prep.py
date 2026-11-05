import bpy, sys, os, glob, json, numpy as np
from mathutils import Matrix, Vector
d, breite = sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
objs = []
for f in sorted(glob.glob(os.path.join(d, '*.obj'))):
    if os.path.basename(f).startswith(('high_', 'LOD', 'K_')): continue
    b = set(bpy.data.objects); bpy.ops.wm.obj_import(filepath=f, forward_axis='Y', up_axis='Z')
    o = [x for x in bpy.data.objects if x not in b][0]; o.name = 'K_' + os.path.basename(f)[:-4]; o.data.name = o.name
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.remove_doubles(threshold=1e-7); bpy.ops.object.mode_set(mode='OBJECT')
    objs.append(o)
V = np.array([list(v.co) for o in objs for v in o.data.vertices]); mn, mx = V.min(0), V.max(0)
s = float(breite) / (mx[0] - mx[0] + (mx - mn)[np.argmax(mx - mn)])
c = (mn + mx) / 2
for o in objs: o.data.transform(Matrix.Scale(s, 4) @ Matrix.Translation(Vector(-c)))
V = np.array([list(v.co) for o in objs for v in o.data.vertices])
info = dict(skalierung=s, masse_m=(V.max(0) - V.min(0)).round(4).tolist(), teile={o.name: sum(len(p.vertices) - 2 for p in o.data.polygons) for o in objs})
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(d, 'roh.blend'))
json.dump(info, open(os.path.join(d, 'info.json'), 'w'), indent=1); print(info)
