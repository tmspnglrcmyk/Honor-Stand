# Lowest für den Schild: flaches Achteck-Prisma, Deckflächen = Holz, Rand = Metall (UV aus High übernommen)
import bpy, sys, os, math, numpy as np
from mathutils import Vector
d = sys.argv[sys.argv.index('--')+1]
bpy.ops.wm.open_mainfile(filepath=os.path.join(d, 'high.blend'))
o = [x for x in bpy.data.objects if x.type == 'MESH'][0]
V = np.array([v.co[:] for v in o.data.vertices])
rad = np.hypot(V[:, 0], V[:, 2]); R = rad.max()
rim = V[rad > R * 0.93]; y0, y1 = rim[:, 1].min(), rim[:, 1].max()
uvd = o.data.uv_layers.active.data
cent = np.array([p.center[:] for p in o.data.polygons]); nrm = np.array([p.normal[:] for p in o.data.polygons])
puv = np.array([np.mean([uvd[li].uv[:] for li in p.loop_indices], 0) for p in o.data.polygons])
def uv_near(pt, ndir):
    sc = np.linalg.norm(cent - pt, axis=1) - 0.05 * (nrm @ ndir)
    return puv[np.argmin(sc)]
uv_front = uv_near(np.array([0.2, y0, 0.15]), np.array([0, -1, 0]))
uv_back = uv_near(np.array([0.2, y1, 0.15]), np.array([0, 1, 0]))
uv_side = uv_near(np.array([R, (y0 + y1) / 2, 0]), np.array([1, 0, 0]))
N = 8; ang = [2 * math.pi * (i + 0.5) / N for i in range(N)]
Rr = R / math.cos(math.pi / N) * 0.97     # Fläche des Achtecks ~ Kreis
pts = []
for y in (y0, y1):
    for a in ang: pts.append((Rr * math.cos(a), y, Rr * math.sin(a)))
faces = []; uvs = []
for k in range(1, N - 1): faces.append((0, k, k + 1)); uvs.append(uv_front)          # vorn (Normale -Y)
for k in range(1, N - 1): faces.append((N, N + k + 1, N + k)); uvs.append(uv_back)  # hinten
for i in range(N):
    j = (i + 1) % N
    faces.append((i, N + j, j)); uvs.append(uv_side); faces.append((i, N + i, N + j)); uvs.append(uv_side)
with open(os.path.join(d, 'LOD0.obj'), 'w') as f:
    for p in pts: f.write('v %.6f %.6f %.6f\n' % p)
    for t in uvs:
        for _ in range(3): f.write('vt %.6f %.6f\n' % tuple(t))
    for i, fc in enumerate(faces): f.write('f %d/%d %d/%d %d/%d\n' % (fc[0]+1, 3*i+1, fc[1]+1, 3*i+2, fc[2]+1, 3*i+3))
print('Achteck', len(faces), 'Dreiecke, y', round(y0, 4), round(y1, 4), 'R', round(R, 4))
