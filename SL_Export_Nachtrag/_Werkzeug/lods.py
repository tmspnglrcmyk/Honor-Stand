import pymeshlab, sys, os, json, numpy as np
d = sys.argv[1]; name = sys.argv[2]; n = int(sys.argv[3]); srcname = sys.argv[4] if len(sys.argv) > 4 else 'high.obj'
def wobj(path, V, F, T):
    with open(path, 'w') as fo:
        for v in V: fo.write('v %.6f %.6f %.6f\n' % tuple(v))
        for t in T: fo.write('vt %.6f %.6f\n' % (t[0], t[1]))
        for i, f in enumerate(F): fo.write('f %d/%d %d/%d %d/%d\n' % (f[0]+1, 3*i+1, f[1]+1, 3*i+2, f[2]+1, 3*i+3))
tmp = os.path.join(d, '_tmp_' + name + '.obj')
ms = pymeshlab.MeshSet(); ms.load_new_mesh(os.path.join(d, srcname))
m = ms.current_mesh()
V, F, T = m.vertex_matrix().copy(), m.face_matrix().copy(), m.wedge_tex_coord_matrix().copy()
cur = len(F)
while cur > n:
    step = max(n, int(cur * 0.6))
    wobj(tmp, V, F, T); ms = pymeshlab.MeshSet(); ms.load_new_mesh(tmp)
    ms.meshing_decimation_quadric_edge_collapse_with_texture(targetfacenum=step, qualitythr=0.5, extratcoordw=1.5,
        preserveboundary=(len(sys.argv) < 6), boundaryweight=2.0, optimalplacement=True, preservenormal=True, planarquadric=True)
    ms.meshing_remove_unreferenced_vertices()
    m = ms.current_mesh()
    V, F, T = m.vertex_matrix().copy(), m.face_matrix().copy(), m.wedge_tex_coord_matrix().copy()
    if len(F) >= cur: break
    cur = len(F)
wobj(os.path.join(d, name + '.obj'), V, F, T)
os.path.exists(tmp) and os.remove(tmp)
print(name, 'Ziel', n, 'erreicht', len(F))
