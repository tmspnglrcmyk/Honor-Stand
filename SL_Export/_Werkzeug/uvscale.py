import bpy, sys, os
d, f = sys.argv[sys.argv.index('--')+1:]
f = float(f)
bpy.ops.wm.open_mainfile(filepath=os.path.join(d, 'high.blend'))
o = [x for x in bpy.data.objects if x.type == 'MESH'][0]
for l in o.data.uv_layers.active.data: l.uv = (l.uv[0] * f, l.uv[1])
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(d, 'high.blend'))
bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active = o
bpy.ops.wm.obj_export(filepath=os.path.join(d, 'high.obj'), export_selected_objects=True, export_materials=False,
                      export_normals=False, export_uv=True, forward_axis='Y', up_axis='Z')
