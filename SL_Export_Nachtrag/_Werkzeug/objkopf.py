# rendert die oberen 0,4 m mehrerer OBJ nebeneinander (Speerspitze), mit Farbtextur
import bpy, sys, math
from mathutils import Vector
a = sys.argv[sys.argv.index('--')+1:]; tex, out, files = a[0], a[1], a[2:]
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
m = bpy.data.materials.new('m'); m.use_nodes = True; nt = m.node_tree; t = nt.nodes.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(tex); nt.links.new(t.outputs[0], nt.nodes['Principled BSDF'].inputs[0])
for i, f in enumerate(files):
    b = set(bpy.data.objects); bpy.ops.wm.obj_import(filepath=f, forward_axis='Y', up_axis='Z')
    o = [q for q in bpy.data.objects if q not in b][0]; o.data.materials.clear(); o.data.materials.append(m); o.location.x = i * 0.08
    o.data.shade_smooth()
import numpy as np; zt = max(v.co.z for o_ in bpy.data.objects if o_.type == 'MESH' for v in o_.data.vertices)
sc.render.engine = 'CYCLES'; sc.cycles.samples = 16
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[1].default_value = 2.0
cam = bpy.data.objects.new('c', bpy.data.cameras.new('c')); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = 0.62; cam.location = ((len(files) - 1) * 0.04, -3, zt - 0.3); cam.rotation_euler = (math.pi / 2, 0, 0)
sc.render.resolution_x = 220 * len(files); sc.render.resolution_y = 900; sc.render.filepath = out
bpy.ops.render.render(write_still=True)
