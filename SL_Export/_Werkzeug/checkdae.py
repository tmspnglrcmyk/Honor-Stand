import sys, glob, os, collada, numpy as np
for p in sorted(glob.glob(os.path.join(sys.argv[1], '*', '*.dae'))):
    c = collada.Collada(p)
    tris = 0; P = []
    for g in c.geometries:
        for prim in g.primitives:
            tris += len(prim); P.append(prim.vertex)
            uv = prim.texcoordset[0] if len(prim.texcoordset) else None
    P = np.vstack(P); e = P.max(0) - P.min(0)
    imgs = [i.path for i in c.images]
    print('%-28s tris=%6d  box=%s  uvmin/max=%s  bild=%s' % (os.path.relpath(p, sys.argv[1]), tris, np.round(e, 4).tolist(),
          (np.round(uv.min(0), 3).tolist(), np.round(uv.max(0), 3).tolist()) if uv is not None else '-', imgs))
