# Nachtrags-Speer: Teile vereinen, eine Atlas-UV (nur verschieben/skalieren, keine Drehung),
# Originaltexturen (BC, MRAO, N) per Emission auf den Atlas backen, high.blend/high.obj schreiben
import bpy, bmesh, sys, os, json, math, numpy as np
from mathutils import Matrix, Vector
src, T, out = sys.argv[sys.argv.index('--') + 1:]
os.makedirs(out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=src)
ms = [o for o in bpy.data.objects if o.type == 'MESH']
for o in ms:
    mw = o.matrix_world.copy(); o.parent = None; o.data.transform(mw); o.matrix_world = Matrix.Identity(4)
    o.data.uv_layers.active.name = 'UVorig'
for o in list(bpy.data.objects):
    if o.type != 'MESH': bpy.data.objects.remove(o, do_unlink=True)
names = {o.name: o.material_slots[0].material.name for o in ms}
bpy.ops.object.select_all(action='DESELECT')
for o in ms: o.select_set(True)
bpy.context.view_layer.objects.active = ms[0]; bpy.ops.object.join(); sp = bpy.context.view_layer.objects.active
sp.name = 'Speer_High'; sp.data.name = 'Speer_High'
matnames = [m.name for m in sp.data.materials]
info = dict(quelle=src, materialien=matnames, dreiecke=sum(len(p.vertices) - 2 for p in sp.data.polygons))
# zentrieren (Größe bleibt Original)
V = np.array([v.co[:] for v in sp.data.vertices]); c = (V.min(0) + V.max(0)) / 2
sp.data.transform(Matrix.Translation(Vector(-c))); V = np.array([v.co[:] for v in sp.data.vertices])
info['masse_m'] = (V.max(0) - V.min(0)).round(4).tolist()

# Atlas-UV
uv_new = sp.data.uv_layers.new(name='UVMap')
for i, l in enumerate(sp.data.uv_layers['UVorig'].data): uv_new.data[i].uv = l.uv
sp.data.uv_layers.active = uv_new
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.select_all(action='SELECT'); bpy.ops.uv.average_islands_scale()
bpy.ops.object.mode_set(mode='OBJECT')
# Spitze (steel) doppelt so dicht wie Holz und Wicklung
bm = bmesh.new(); bm.from_mesh(sp.data); ul = bm.loops.layers.uv['UVMap']
steel = matnames.index('steel')
# Inseln der Stahlfläche um ihren Mittelpunkt skalieren
bm.faces.ensure_lookup_table()
seen = set()
for f in bm.faces:
    if f.material_index != steel or f.index in seen: continue
    # Insel über gemeinsame UV-Kanten sammeln
    isl = [f]; seen.add(f.index); st = [f]
    while st:
        g = st.pop()
        for e in g.edges:
            for h in e.link_faces:
                if h.index in seen or h.material_index != steel: continue
                # gleiche UV an beiden Kantenenden?
                ok = True
                for v in e.verts:
                    a = [l[ul].uv for l in g.loops if l.vert == v][0]; b = [l[ul].uv for l in h.loops if l.vert == v][0]
                    if (a - b).length > 1e-6: ok = False
                if ok: seen.add(h.index); isl.append(h); st.append(h)
    pts = [l[ul].uv.copy() for g in isl for l in g.loops]; cc = sum(pts, Vector((0, 0))) / len(pts)
    for g in isl:
        for l in g.loops: l[ul].uv = cc + (l[ul].uv - cc) * 2.0
bm.to_mesh(sp.data); bm.free()
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.uv.select_all(action='SELECT')
bpy.ops.uv.pack_islands(rotate=False, margin=0.006, scale=True)
bpy.ops.object.mode_set(mode='OBJECT')
# Kontrolle: keine Drehung, keine Spiegelung je Fläche (Vorzeichen der UV-Fläche gleich wie im Original)
o_uv = sp.data.uv_layers['UVorig'].data; n_uv = sp.data.uv_layers['UVMap'].data
def sarea(uvd, p):
    q = [uvd[li].uv for li in p.loop_indices]; return sum((q[i].x * q[(i + 1) % len(q)].y - q[(i + 1) % len(q)].x * q[i].y) for i in range(len(q)))
flips = sum(1 for p in sp.data.polygons if abs(sarea(o_uv, p)) > 1e-12 and np.sign(sarea(o_uv, p)) != np.sign(sarea(n_uv, p)))
# Drehwinkel je Fläche über eine Kante prüfen
rot = []
for p in sp.data.polygons:
    l0, l1 = p.loop_indices[0], p.loop_indices[1]
    a = o_uv[l1].uv - o_uv[l0].uv; b = n_uv[l1].uv - n_uv[l0].uv
    if a.length > 1e-6 and b.length > 1e-9: rot.append(abs(math.degrees(math.atan2(a.x * b.y - a.y * b.x, a.dot(b)))))
info['uv_spiegelungen'] = flips; info['uv_drehung_max_grad'] = round(max(rot), 3)
print('Spiegelungen', flips, 'max. Drehung', round(max(rot), 3), 'Grad')

# Bake: je Material Emission aus der Originaltextur über UVorig
RES = 2048
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 1
sc.render.bake.margin = 12; sc.render.bake.use_selected_to_active = False
target = bpy.data.images.new('atlas', RES, RES, float_buffer=True)
for m in sp.data.materials:
    nt = m.node_tree; nt.nodes.clear()
    o_ = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission'); nt.links.new(em.outputs[0], o_.inputs[0])
    uvn = nt.nodes.new('ShaderNodeUVMap'); uvn.uv_map = 'UVorig'
    tx = nt.nodes.new('ShaderNodeTexImage'); tx.name = 'src'; nt.links.new(uvn.outputs[0], tx.inputs[0]); nt.links.new(tx.outputs[0], em.inputs[0])
    tg = nt.nodes.new('ShaderNodeTexImage'); tg.image = target; nt.nodes.active = tg
bpy.ops.object.select_all(action='DESELECT'); sp.select_set(True); bpy.context.view_layer.objects.active = sp
from PIL import Image
for kanal, cs in (('BC', 'Linear Rec.709'), ('MRAO', 'Non-Color'), ('N', 'Non-Color')):
    for m in sp.data.materials:
        im = bpy.data.images.load(os.path.join(T, '%s_%s.png' % (m.name, kanal)), check_existing=True); im.colorspace_settings.name = 'Non-Color'
        m.node_tree.nodes['src'].image = im
    target.generated_color = (0, 0, 0, 1)
    bpy.ops.object.bake(type='EMIT')
    px = np.array(target.pixels[:]).reshape(RES, RES, 4)[::-1, :, :3]
    Image.fromarray((np.clip(px, 0, 1) * 255 + 0.5).astype(np.uint8)).save(os.path.join(out, 'atlas_%s.png' % kanal))
    print('gebacken', kanal)
# Material vereinheitlichen, alte UV entfernen
sp.data.uv_layers.remove(sp.data.uv_layers['UVorig'])
sp.data.materials.clear()
for p in sp.data.polygons: p.material_index = 0
for im in list(bpy.data.images): bpy.data.images.remove(im)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, 'high.blend'))
bpy.ops.object.select_all(action='DESELECT'); sp.select_set(True)
bpy.ops.wm.obj_export(filepath=os.path.join(out, 'high.obj'), export_selected_objects=True, export_materials=False, export_normals=False, export_uv=True, forward_axis='Y', up_axis='Z')
info.update(skalierung=1.0, zielmass='Originalmaß 1,44 m')
json.dump(info, open(os.path.join(out, 'info.json'), 'w'), indent=1, ensure_ascii=False); print(info)
