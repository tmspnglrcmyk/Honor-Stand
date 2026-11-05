# Nachtrags-Speer auf 2,20 m: High, Teil-OBJs und Hülle gleichmäßig skalieren (Mittelpunkt bleibt im Ursprung)
import bpy, sys, os, json, numpy as np
from mathutils import Matrix
a, b, L = sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.open_mainfile(filepath=os.path.join(a, 'high.blend'))
o = bpy.data.objects['Speer_High']; V = np.array([v.co[:] for v in o.data.vertices])
s = float(L) / (V[:, 2].max() - V[:, 2].min())
o.data.transform(Matrix.Scale(s, 4))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(b, 'high.blend'))
bpy.ops.object.select_all(action='DESELECT'); o.select_set(True)
bpy.ops.wm.obj_export(filepath=os.path.join(b, 'high.obj'), export_selected_objects=True, export_materials=False, export_normals=False, export_uv=True, forward_axis='Y', up_axis='Z')
for n in ('teil_rope.obj', 'teil_rest.obj'):
    with open(os.path.join(a, n)) as f, open(os.path.join(b, n), 'w') as g:
        for l in f:
            if l.startswith('v '): x = [float(t) * s for t in l.split()[1:4]]; g.write('v %.6f %.6f %.6f\n' % tuple(x))
            else: g.write(l)
h = json.load(open(os.path.join(a, 'huelle.json'))); h.update(z0=h['z0'] * s, z1=h['z1'] * s, r=h['r'] * s); json.dump(h, open(os.path.join(b, 'huelle.json'), 'w'))
info = json.load(open(os.path.join(a, 'info.json'))); V = np.array([v.co[:] for v in o.data.vertices])
info.update(skalierung=s, zielmass='Länge 2,20 m (gleichmäßig aus 1,44 m)', masse_m=(V.max(0) - V.min(0)).round(4).tolist())
json.dump(info, open(os.path.join(b, 'info.json'), 'w'), indent=1, ensure_ascii=False); print('Faktor %.4f Maße %s' % (s, info['masse_m']))
