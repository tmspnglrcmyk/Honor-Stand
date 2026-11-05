# Speer-Lowest von Hand: Fußring (4), Ring an der breitesten Stelle der Spitze (4, trifft die Box), Spitze (1)
import bpy, sys, os, numpy as np
from scipy.spatial import cKDTree
d = sys.argv[sys.argv.index('--')+1]
bpy.ops.wm.open_mainfile(filepath=os.path.join(d, 'high.blend'))
o = bpy.data.objects['Speer_High']; V = np.array([v.co[:] for v in o.data.vertices]); lo, hi = V.min(0), V.max(0)
top = V[V[:, 2] > hi[2] - 0.25]
zw = top[np.argmax(np.abs(top[:, 0] - (lo[0] + hi[0]) / 2)), 2]          # breiteste Stelle der Spitze
bot = V[V[:, 2] < lo[2] + 0.05]; cx, cy = bot[:, 0].mean(), bot[:, 1].mean(); rb = np.percentile(np.hypot(bot[:, 0] - cx, bot[:, 1] - cy), 95)
mx, my = (lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2
P = [(cx + rb, cy, lo[2]), (cx, cy + rb, lo[2]), (cx - rb, cy, lo[2]), (cx, cy - rb, lo[2]),
     (hi[0], my, zw), (mx, hi[1], zw), (lo[0], my, zw), (mx, lo[1], zw),
     (top[np.argmax(top[:, 2]), 0], top[np.argmax(top[:, 2]), 1], hi[2])]
F = []
for i in range(4):
    j = (i + 1) % 4; F += [(i, j, 4 + j), (i, 4 + j, 4 + i)]
for i in range(4): F.append((4 + i, 4 + (i + 1) % 4, 8))
P = np.array(P)
# UV je Fläche von der nächstgelegenen High-Fläche (Mittelpunkt)
cen = np.array([p.center[:] for p in o.data.polygons]); uv = o.data.uv_layers.active.data
puv = np.array([np.mean([uv[li].uv[:] for li in p.loop_indices], 0) for p in o.data.polygons]); tree = cKDTree(cen)
with open(os.path.join(d, 'LOD0.obj'), 'w') as f:
    for p in P: f.write('v %.6f %.6f %.6f\n' % tuple(p))
    for fc in F:
        m = P[list(fc)].mean(0); m[2] = m[2] if fc[2] != 8 else (m[2] + hi[2]) / 2
        _, k = tree.query(m); t = puv[k]
        for _ in range(3): f.write('vt %.6f %.6f\n' % tuple(t))
    for i, fc in enumerate(F): f.write('f %d/%d %d/%d %d/%d\n' % (fc[0] + 1, 3 * i + 1, fc[1] + 1, 3 * i + 2, fc[2] + 1, 3 * i + 3))
print('Lowest', len(F), 'Dreiecke; Box-Abweichung', np.abs(P.min(0) - lo).max().round(6), np.abs(P.max(0) - hi).max().round(6), 'zw', round(float(zw), 3))
