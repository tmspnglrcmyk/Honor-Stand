# liest model.dae (Assimp, cm, Y-up) und schreibt je Teil eine OBJ in Metern, Z-up, mit UV und Normalen
import collada, numpy as np, sys, os
src, out = sys.argv[1:3]
c = collada.Collada(src)
names = {}
for n in c.scene.nodes:
    for ch in n.children:
        names[ch.geometry.id] = n.id.replace(' ', '_')
for g in c.geometries:
    nm = names[g.id]
    for p in g.primitives:
        V = p.vertex * 0.01; V = np.stack([V[:, 0], -V[:, 2], V[:, 1]], 1)
        N = p.normal; N = np.stack([N[:, 0], -N[:, 2], N[:, 1]], 1)
        T = p.texcoordset[0]
        vi, ni, ti = (np.asarray(x).reshape(-1, 3) for x in (p.vertex_index, p.normal_index, p.texcoord_indexset[0]))
        with open(os.path.join(out, nm + '.obj'), 'w') as f:
            f.write('o %s\n' % nm)
            for v in V: f.write('v %.6f %.6f %.6f\n' % tuple(v))
            for t in T: f.write('vt %.6f %.6f\n' % tuple(t[:2]))
            for n_ in N: f.write('vn %.5f %.5f %.5f\n' % tuple(n_))
            for a, b, cc in zip(vi, ti, ni):
                f.write('f ' + ' '.join('%d/%d/%d' % (a[k] + 1, b[k] + 1, cc[k] + 1) for k in range(3)) + '\n')
        print(nm, len(vi), 'tris', np.round(V.min(0), 3), np.round(V.max(0), 3), 'uv', np.round(T.min(0), 3), np.round(T.max(0), 3))
