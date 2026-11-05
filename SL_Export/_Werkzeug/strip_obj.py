# entfernt Kleinteile (Durchmesser unter Grenze) aus einer OBJ, UVs bleiben (Wedge)
import pymeshlab, sys
src, dst, lim = sys.argv[1], sys.argv[2], float(sys.argv[3])
ms = pymeshlab.MeshSet(); ms.load_new_mesh(src)
ms.meshing_merge_close_vertices(threshold=pymeshlab.PercentageValue(0.0001))
n0 = ms.current_mesh().face_number()
ms.meshing_remove_connected_component_by_diameter(mincomponentdiag=pymeshlab.PureValue(lim))
ms.meshing_remove_unreferenced_vertices()
m = ms.current_mesh(); V, F, T = m.vertex_matrix(), m.face_matrix(), m.wedge_tex_coord_matrix()
with open(dst, 'w') as fo:
    for v in V: fo.write('v %.6f %.6f %.6f\n' % tuple(v))
    for t in T: fo.write('vt %.6f %.6f\n' % (t[0], t[1]))
    for i, f in enumerate(F): fo.write('f %d/%d %d/%d %d/%d\n' % (f[0]+1, 3*i+1, f[1]+1, 3*i+2, f[2]+1, 3*i+3))
print('Flächen', n0, '->', len(F))
