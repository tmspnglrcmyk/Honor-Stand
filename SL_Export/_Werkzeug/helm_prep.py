# Helm: Teile importieren, verschweißen, zentrieren, high.blend + je Teil high_<Teil>.obj
import bpy, sys, os, json, numpy as np
from mathutils import Matrix, Vector
d, tex = sys.argv[sys.argv.index('--')+1:]
TEILE = ['Helmet_42', 'Face_guard', 'Mail', 'Liner']
bpy.ops.wm.read_factory_settings(use_empty=True)
objs = []
for t in TEILE:
    b = set(bpy.data.objects)
    bpy.ops.wm.obj_import(filepath=os.path.join(d, t + '.obj'), forward_axis='Y', up_axis='Z')
    o = [x for x in bpy.data.objects if x not in b][0]; o.name = 'Helm_' + t; o.data.name = o.name
    n0 = len(o.data.vertices)
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=1e-6); bpy.ops.object.mode_set(mode='OBJECT')
    print(t, 'Vertices', n0, '->', len(o.data.vertices), 'Dreiecke', len(o.data.polygons))
    objs.append(o)
V = np.array([list(v.co) for o in objs for v in o.data.vertices]); c = (V.min(0) + V.max(0)) / 2
for o in objs: o.data.transform(Matrix.Translation(Vector(-c)))
V = np.array([list(v.co) for o in objs for v in o.data.vertices])
info = dict(masse_m=(V.max(0) - V.min(0)).round(4).tolist(), verschiebung=(-c).round(4).tolist())
for o in objs:
    o.data.materials.clear()
    m = bpy.data.materials.new(o.name[5:]); m.use_nodes = True; nt = m.node_tree; bs = nt.nodes['Principled BSDF']
    t = nt.nodes.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(os.path.join(tex, o.name[5:] + '_albedo.jpeg'))
    nt.links.new(t.outputs[0], bs.inputs['Base Color']); o.data.materials.append(m)
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True)
    bpy.ops.wm.obj_export(filepath=os.path.join(d, 'high_' + o.name[5:] + '.obj'), export_selected_objects=True, export_materials=False, export_normals=False, export_uv=True, forward_axis='Y', up_axis='Z')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(d, 'high.blend'))
json.dump(info, open(os.path.join(d, 'info.json'), 'w'))
print(info)
