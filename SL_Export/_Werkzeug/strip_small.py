# exportiert High ohne Kleinteile (Nieten) als Quelle für Low/Lowest
import bpy, sys, bmesh, numpy as np, os
d, lim = sys.argv[sys.argv.index('--')+1:]; lim=float(lim)
bpy.ops.wm.open_mainfile(filepath=os.path.join(d,'high.blend'))
o=[x for x in bpy.data.objects if x.type=='MESH'][0]
bm=bmesh.new(); bm.from_mesh(o.data); bm.verts.ensure_lookup_table()
seen=set(); kill=[]
for v in bm.verts:
    if v.index in seen: continue
    st=[v]; c=[]; seen.add(v.index)
    while st:
        x=st.pop(); c.append(x)
        for e in x.link_edges:
            y=e.other_vert(x)
            if y.index not in seen: seen.add(y.index); st.append(y)
    p=np.array([x.co[:] for x in c])
    if np.linalg.norm(p.max(0)-p.min(0))<lim: kill+=c
print('entfernt', len(kill),'Vertices')
bmesh.ops.delete(bm, geom=kill, context='VERTS'); bm.to_mesh(o.data)
bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active=o
bpy.ops.wm.obj_export(filepath=os.path.join(d,'high_reduziert.obj'), export_selected_objects=True, export_materials=False, export_normals=False, export_uv=True, forward_axis='Y', up_axis='Z')
