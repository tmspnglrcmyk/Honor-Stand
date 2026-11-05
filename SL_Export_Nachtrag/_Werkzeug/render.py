import bpy, sys, os, math
from mathutils import Vector
blend, out, mode = sys.argv[sys.argv.index('--')+1:][:3]
bpy.ops.wm.open_mainfile(filepath=blend)
sc = bpy.context.scene
name = os.path.basename(blend)[:-6]
objs = {o.name: o for o in bpy.data.objects}
for o in bpy.data.objects:
    o.hide_render = True
if mode == 'lods':
    show = [objs[name + s] for s in ('_High', '_LOD2', '_LOD1', '_LOD0')]
    W_ = max(o.dimensions.x for o in show) * 1.4 + 0.05
    for i, o in enumerate(show): o.location = (0, 0, 0); o.location.x = i * W_
else:
    show = [objs[name + '_High']]
for o in show: o.hide_render = False
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 64; sc.cycles.use_denoising = True
try: sc.cycles.denoiser = 'OPENIMAGEDENOISE'
except: pass
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs[0].default_value = (0.42, 0.43, 0.45, 1); w.node_tree.nodes['Background'].inputs[1].default_value = 0.8
sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); sun.data.energy = 3.2; sun.data.angle = 0.1
sun.rotation_euler = (math.radians(50), 0, math.radians(-35)); sc.collection.objects.link(sun)
pts = [o.matrix_world @ Vector(c) for o in show for c in o.bound_box]
if mode == 'kopf':
    vv = [o.matrix_world @ v.co for o in show for v in o.data.vertices]; zt = max(v.z for v in vv)
    pts = [v for v in vv if v.z > zt - 0.42]
mn = Vector([min(p[i] for p in pts) for i in range(3)]); mx = Vector([max(p[i] for p in pts) for i in range(3)])
c = (mn + mx) / 2; ext = mx - mn
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'PERSP'; cam.data.lens = 70
views = {'front': Vector((0.25, -1, 0.15)), 'back': Vector((-0.25, 1, 0.15)), 'iso': Vector((0.8, -1, 0.5))}
vk = sys.argv[-1] if sys.argv[-1] in views else 'front'
d = views[vk].normalized()
aspect = 1.0
if mode == 'lods':
    sc.render.resolution_x, sc.render.resolution_y = 1600, 600
else:
    sc.render.resolution_x, sc.render.resolution_y = (600, 1200) if name == 'Speer' else (900, 900)
if mode == 'kopf': sc.render.resolution_x, sc.render.resolution_y = 600, 1200
sc.render.film_transparent = False
# Abstand so, dass alles ins Bild passt
cam.data.sensor_fit = 'AUTO'
fov_l = 2 * math.atan(cam.data.sensor_width / 2 / cam.data.lens)
rx, ry = sc.render.resolution_x, sc.render.resolution_y
fov_w = fov_l if rx >= ry else 2 * math.atan(math.tan(fov_l / 2) * rx / ry)
fov_h = fov_l if ry > rx else 2 * math.atan(math.tan(fov_l / 2) * ry / rx)
# projizierte Halbbreiten grob über Ausdehnung quer zur Blickrichtung
right = d.cross(Vector((0, 0, 1))).normalized(); up = right.cross(d).normalized()
hw = max(abs((p - c).dot(right)) for p in pts) * 1.12; hh = max(abs((p - c).dot(up)) for p in pts) * 1.12
depth = max(abs((p - c).dot(d)) for p in pts)
dist = max(hw / math.tan(fov_w / 2), hh / math.tan(fov_h / 2)) + depth
cam.location = c + d * dist
cam.rotation_euler = (c - cam.location).to_track_quat('-Z', 'Y').to_euler()
cam.data.clip_start = dist * 0.01; cam.data.clip_end = dist * 10
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
