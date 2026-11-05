import bpy, sys, math, numpy as np
from mathutils import Vector
blend, out = sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.open_mainfile(filepath=blend); sc = bpy.context.scene
V = {o.name: np.array([list(o.matrix_world @ v.co) for v in o.data.vertices]) for o in bpy.data.objects if o.type == 'MESH'}
A = np.vstack(list(V.values())); ax = np.argmax(A.max(0) - A.min(0)); L = A[:, ax].max() - A[:, ax].min()
print('Gesamtlänge %.3f m entlang Achse %d' % (L, ax))
for n, P in V.items():
    q = np.delete(P, ax, 1); print('  %-10s Länge %.3f  Querschnitt %s  von %.3f bis %.3f' % (n, P[:, ax].max() - P[:, ax].min(), np.round(q.max(0) - q.min(0), 4), P[:, ax].min(), P[:, ax].max()))
sc.render.engine = 'CYCLES'; sc.cycles.samples = 32
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.6, 0.6, 0.62, 1)
sun = bpy.data.objects.new('s', bpy.data.lights.new('s', 'SUN')); sun.data.energy = 3; sun.rotation_euler = (0.7, 0.2, 0.5); sc.collection.objects.link(sun)
cam = bpy.data.objects.new('c', bpy.data.cameras.new('c')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.type = 'ORTHO'
sc.render.resolution_x, sc.render.resolution_y = 1600, 500
hi = A[:, ax].max(); lo = A[:, ax].min()
for tag, (a, b) in (('spitze', (hi - 0.35, hi)), ('ende', (lo, lo + 0.35)), ('ganz', (lo, hi))):
    c = A.mean(0).copy(); c[ax] = (a + b) / 2
    cam.data.ortho_scale = (b - a) * 1.05
    d = np.zeros(3); d[(ax + 1) % 3] = -1; d[(ax + 2) % 3] = 0.3
    cam.location = Vector(c + d * 2); cam.rotation_euler = (Vector(c) - cam.location).to_track_quat('-Z', 'Y').to_euler()
    up = np.zeros(3); up[ax] = 1
    cam.rotation_euler = (Vector(c) - cam.location).to_track_quat('-Z', 'X' if ax == 0 else ('Y' if ax == 1 else 'Z')).to_euler()
    sc.render.filepath = out + '_' + tag + '.png'; bpy.ops.render.render(write_still=True)
