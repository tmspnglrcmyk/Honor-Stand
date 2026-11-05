# Kistenteile nach ermittelter Textur zu drei Objekten vereinen, high.blend und high_<Gruppe>.obj
import bpy, sys, os, json
d = sys.argv[sys.argv.index('--')+1]
bpy.ops.wm.open_mainfile(filepath=os.path.join(d, 'roh.blend'))
z = json.load(open(os.path.join(d, 'zuordnung.json')))
G = {'BOIS': 'Holz', 'METAL': 'Metall', 'ANNEAU2': 'Nieten'}
for src, grp in G.items():
    names = [n for n, v in z.items() if v['best'] == src]; obs = [bpy.data.objects[n] for n in names]
    bpy.ops.object.select_all(action='DESELECT')
    for o in obs: o.select_set(True)
    bpy.context.view_layer.objects.active = obs[0]; bpy.ops.object.join()
    o = bpy.context.view_layer.objects.active; o.name = 'Kiste_' + grp; o.data.name = o.name; o.data.materials.clear()
    bpy.ops.wm.obj_export(filepath=os.path.join(d, 'high_' + grp + '.obj'), export_selected_objects=True, export_materials=False, export_normals=False, export_uv=True, forward_axis='Y', up_axis='Z')
    print(grp, names, sum(len(p.vertices) - 2 for p in o.data.polygons), 'Dreiecke')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(d, 'high.blend'))
