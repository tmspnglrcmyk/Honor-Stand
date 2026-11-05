# Helm-Lowest v2: eine Fläche, 12 Dreiecke, 9 Punkte, trifft die High-Box exakt (keine Anker)
import sys, os, numpy as np
d = sys.argv[1]
def readv(p): return np.array([[float(x) for x in l.split()[1:4]] for l in open(p) if l.startswith('v ')])
A = np.vstack([readv(os.path.join(d, 'high_' + t + '.obj')) for t in ('Helmet_42', 'Face_guard', 'Mail', 'Liner')])
G = readv(os.path.join(d, 'high_Helmet_42.obj'))
lo, hi = A.min(0), A.max(0); cy = (G[:, 1].min() + G[:, 1].max()) / 2
zr = np.percentile(G[:, 2], 1)                      # Unterkante der Glocke
P = [(0, cy, hi[2]),                                # 0 Scheitel
     (0, lo[1], zr), (hi[0], cy, zr), (0, hi[1], zr), (lo[0], cy, zr),          # 1-4 Rand: vorn, rechts, hinten, links
     (0, lo[1] * 0.8 + cy * 0.2, lo[2]), (hi[0] * 0.8, cy, lo[2]), (0, hi[1], lo[2]), (lo[0] * 0.8, cy, lo[2])]  # 5-8 unten
F = []
for i in range(4):
    a, b = 1 + i, 1 + (i + 1) % 4
    F.append((0, a, b) if i % 2 else (0, a, b))
    c, e = 5 + i, 5 + (i + 1) % 4
    F += [(a, c, e), (a, e, b)]
# Wicklung nach außen ausrichten
P = np.array(P, float); C = np.array([0, cy, (zr + lo[2]) / 2])
F2 = []
for f in F:
    n = np.cross(P[f[1]] - P[f[0]], P[f[2]] - P[f[0]]); m = P[list(f)].mean(0)
    F2.append(f if n @ (m - C) > 0 else (f[0], f[2], f[1]))
with open(os.path.join(d, 'Helm_LOD0_v2.obj'), 'w') as fo:
    for p in P: fo.write('v %.6f %.6f %.6f\n' % tuple(p))
    for _ in range(len(F2) * 3): fo.write('vt 0.5 0.5\n')
    for i, f in enumerate(F2): fo.write('f %d/%d %d/%d %d/%d\n' % (f[0] + 1, 3 * i + 1, f[1] + 1, 3 * i + 2, f[2] + 1, 3 * i + 3))
print('Lowest v2', len(F2), 'Dreiecke, Box', np.round(P.min(0) - lo, 6), np.round(P.max(0) - hi, 6))
