# Lowest der Kiste: Quader über die ganze Kiste ohne Boden (10 Dreiecke), Holzfarbe
import sys, os, numpy as np
d = sys.argv[1]
V = np.vstack([np.array([[float(x) for x in l.split()[1:4]] for l in open(os.path.join(d, f)) if l.startswith('v ')]) for f in ('high_Holz.obj', 'high_Metall.obj')])
lo, hi = V.min(0), V.max(0)
P = [(x, y, z) for z in (lo[2], hi[2]) for y in (lo[1], hi[1]) for x in (lo[0], hi[0])]
# Indizes: unten 0..3, oben 4..7 ; (x,y) Reihenfolge 0:(-,-) 1:(+,-) 2:(-,+) 3:(+,+)
F = [(4, 5, 7), (4, 7, 6),            # oben
     (0, 1, 5), (0, 5, 4),            # vorn (-Y)
     (3, 2, 6), (3, 6, 7),            # hinten (+Y)
     (2, 0, 4), (2, 4, 6),            # links (-X)
     (1, 3, 7), (1, 7, 5)]            # rechts (+X)
with open(os.path.join(d, 'Holz_LOD0.obj'), 'w') as f:
    for p in P: f.write('v %.6f %.6f %.6f\n' % p)
    for i in range(len(F) * 3): f.write('vt 0.5 0.5\n')
    for i, fc in enumerate(F): f.write('f %d/%d %d/%d %d/%d\n' % (fc[0] + 1, 3 * i + 1, fc[1] + 1, 3 * i + 2, fc[2] + 1, 3 * i + 3))
print('Quader', len(F), 'Dreiecke')
