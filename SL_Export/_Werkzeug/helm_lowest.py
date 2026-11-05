# Helm-Lowest von Hand: Kuppel (18 Dreiecke) und Visierband (8 Dreiecke), Radien aus den Originalpunkten
import sys, os, math, numpy as np
d = sys.argv[1]
def readv(p): return np.array([[float(x) for x in l.split()[1:4]] for l in open(p) if l.startswith('v ')])
G = readv(os.path.join(d, 'high_Helmet_42.obj')); F = readv(os.path.join(d, 'high_Face_guard.obj'))
cy = (G[:, 1].min() + G[:, 1].max()) / 2
def rmax(P, ang, z0, z1, cz=None):
    th = np.arctan2(P[:, 0], P[:, 1] - cy); m = (np.abs((th - ang + np.pi) % (2 * np.pi) - np.pi) < 0.35) & (P[:, 2] >= z0) & (P[:, 2] <= z1)
    return np.percentile(np.hypot(P[m, 0], P[m, 1] - cy), 97) if m.sum() > 10 else None
def wobj(path, V, Fc):
    with open(path, 'w') as f:
        for v in V: f.write('v %.6f %.6f %.6f\n' % tuple(v))
        for i, fc in enumerate(Fc): f.write('vt 0.5 0.5\n' * 3)
        for i, fc in enumerate(Fc): f.write('f %d/%d %d/%d %d/%d\n' % (fc[0] + 1, 3 * i + 1, fc[1] + 1, 3 * i + 2, fc[2] + 1, 3 * i + 3))
# Kuppel: Scheitel, Ring auf 55 % Höhe, Rand
zr, zt = np.percentile(G[:, 2], 1), G[:, 2].max(); N = 5
angs = [2 * math.pi * i / N for i in range(N)]
V = [(0, cy, zt)]
for frac in (0.55, 0.0):
    z = zr + frac * (zt - zr)
    for a in angs:
        r = rmax(G, a, z - 0.02, z + 0.02) or rmax(G, a, zr, zt)
        V.append((r * math.sin(a), cy + r * math.cos(a), z))
Fc = []
for i in range(N):
    j = (i + 1) % N
    Fc.append((0, 1 + j, 1 + i))
    a, b, c, e = 1 + i, 1 + j, 1 + N + j, 1 + N + i
    Fc += [(a, b, c), (a, c, e)]
wobj(os.path.join(d, 'Helmet_42_LOD0.obj'), V, Fc)
# Visierband vorn und seitlich: 5 Spalten, 2 Reihen
z0, z1 = F[:, 2].min(), F[:, 2].max()
angs = np.radians(np.linspace(-100, 100, 4)) + math.pi    # um die Front (-Y)
V = []
for z in (z1, z0):
    for a in angs:
        r = rmax(F, a, z0, z1) or 0.12
        V.append((r * math.sin(a), cy + r * math.cos(a), z))
Fc = []
for i in range(3):
    a, b, c, e = i, i + 1, 4 + i + 1, 4 + i
    Fc += [(a, b, c), (a, c, e)]
wobj(os.path.join(d, 'Face_guard_LOD0.obj'), V, Fc)
print('Kuppel 15, Visier 6 Dreiecke; Rand z %.3f Scheitel %.3f, Visier z %.3f..%.3f' % (zr, zt, z0, z1))
