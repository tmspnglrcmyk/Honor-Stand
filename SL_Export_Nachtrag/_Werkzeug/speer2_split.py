# trennt im Atlas-High die Wicklung (rope) vom Rest per Positionsabgleich mit dem Original-FBX,
# schreibt teil_rope.obj / teil_rest.obj (Atlas-UV) und eine Hülle für das Low
import bpy, sys, os, json, math, numpy as np
from mathutils import Matrix
from scipy.spatial import cKDTree
src, d = sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.fbx(filepath=src)
P = {}
for o in bpy.data.objects:
    if o.type == 'MESH': P[o.material_slots[0].material.name] = np.array([list(o.matrix_world @ v.co) for v in o.data.vertices])
A = np.vstack(list(P.values())); c = (A.min(0) + A.max(0)) / 2
rope = P['rope'] - c; tree = cKDTree(rope)
bpy.ops.wm.open_mainfile(filepath=os.path.join(d, 'high.blend'))
o = bpy.data.objects['Speer_High']; V = np.array([v.co[:] for v in o.data.vertices])
dist, _ = tree.query(V); isrope_v = dist < 1e-5
sel = [all(isrope_v[i] for i in p.vertices) for p in o.data.polygons]
print('Wicklung', sum(sel), 'von', len(sel), 'Flächen')
uv = o.data.uv_layers.active.data
def wobj(path, polys):
    vid = sorted({i for p in polys for i in p.vertices}); m = {v: k for k, v in enumerate(vid)}
    with open(path, 'w') as f:
        for v in vid: f.write('v %.6f %.6f %.6f\n' % tuple(V[v]))
        n = 0
        for p in polys:
            for li in p.loop_indices: f.write('vt %.6f %.6f\n' % tuple(uv[li].uv))
        k = 1
        for p in polys:
            idx = list(p.vertices); f.write('f ' + ' '.join('%d/%d' % (m[idx[j]] + 1, k + j) for j in range(len(idx))) + '\n'); k += len(idx)
wobj(os.path.join(d, 'teil_rope.obj'), [p for p, s in zip(o.data.polygons, sel) if s])
wobj(os.path.join(d, 'teil_rest.obj'), [p for p, s in zip(o.data.polygons, sel) if not s])
# Hülle: sechsseitiger Zylinder über die Wicklung, UV auf eine Lederstelle der Wicklung (2-px-Fläche wird im Zusammenbau gesetzt)
R = V[isrope_v]; z0, z1 = R[:, 2].min(), R[:, 2].max(); cx, cy = R[:, 0].mean(), R[:, 1].mean()
r = np.percentile(np.hypot(R[:, 0] - cx, R[:, 1] - cy), 90)
# UV-Mitte einer großen Wicklungsfläche
ropepolys = [p for p, s in zip(o.data.polygons, sel) if s]; big = max(ropepolys, key=lambda p: p.area)
u0 = np.mean([uv[li].uv[:] for li in big.loop_indices], 0)
N = 6; pts = [(cx + r * math.cos(2 * math.pi * i / N), cy + r * math.sin(2 * math.pi * i / N), z) for z in (z0, z1) for i in range(N)]
with open(os.path.join(d, 'huelle.obj'), 'w') as f:
    for p in pts: f.write('v %.6f %.6f %.6f\n' % p)
    F = []
    for i in range(N):
        j = (i + 1) % N; F += [(i, j, N + j), (i, N + j, N + i)]
    for _ in range(len(F) * 3): f.write('vt %.6f %.6f\n' % tuple(u0))
    for k, fc in enumerate(F): f.write('f %d/%d %d/%d %d/%d\n' % (fc[0] + 1, 3 * k + 1, fc[1] + 1, 3 * k + 2, fc[2] + 1, 3 * k + 3))
json.dump(dict(rope_uv=list(map(float, u0)), z0=float(z0), z1=float(z1), r=float(r)), open(os.path.join(d, 'huelle.json'), 'w'))
print('Hülle r=%.4f z %.3f..%.3f' % (r, z0, z1))
