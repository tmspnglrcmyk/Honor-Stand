# Kettenvorhang: Fläche in der Mitte der Ringlage, Bakes von den Originalringen (Farbe·AO, Deckung, Normale, Rauheit, Metall)
import bpy, sys, os, json, math, numpy as np
from mathutils import Vector
d, tex, out = sys.argv[sys.argv.index('--') + 1:]
os.makedirs(out, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=os.path.join(d, 'high.blend'))
sc = bpy.context.scene
mail = bpy.data.objects['Helm_Mail']; glocke = bpy.data.objects['Helm_Helmet_42']
G = np.array([v.co[:] for v in glocke.data.vertices]); cy = (G[:, 1].min() + G[:, 1].max()) / 2
M = np.array([v.co[:] for v in mail.data.vertices])
th = np.arctan2(M[:, 0], M[:, 1] - cy); rho = np.hypot(M[:, 0], M[:, 1] - cy); z = M[:, 2]
t0, t1 = np.percentile(th, 0.2), np.percentile(th, 99.8); z0, z1 = z.min(), z.max()
pad_t = (t1 - t0) * 0.02; t0 -= pad_t; t1 += pad_t; pad_z = (z1 - z0) * 0.02; z0 -= pad_z; z1 += pad_z

def radius_grid(NU, NV):
    tu = np.linspace(t0, t1, NU); zv = np.linspace(z0, z1, NV)
    R = np.full((NV, NU), np.nan)
    st, sz = (t1 - t0) / (NU - 1) * 0.9, (z1 - z0) / (NV - 1) * 0.9
    for j, zz in enumerate(zv):
        for i, tt in enumerate(tu):
            m = (np.abs(th - tt) < st) & (np.abs(z - zz) < sz)
            if m.sum() > 5: R[j, i] = np.median(rho[m])
    # Lücken füllen: nächster gültiger Nachbar entlang Zeilen/Spalten mitteln
    for _ in range(60):
        if not np.isnan(R).any(): break
        Rn = R.copy()
        for j in range(NV):
            for i in range(NU):
                if np.isnan(R[j, i]):
                    nb = [R[jj, ii] for jj, ii in ((j-1, i), (j+1, i), (j, i-1), (j, i+1)) if 0 <= jj < NV and 0 <= ii < NU and not np.isnan(R[jj, ii])]
                    if nb: Rn[j, i] = np.mean(nb)
        R = Rn
    return tu, zv, R

def build(name, NU, NV, double):
    tu, zv, R = radius_grid(NU, NV)
    verts, uvs = [], []
    for j in range(NV):
        for i in range(NU):
            r = R[j, i]; verts.append((r * math.sin(tu[i]), cy + r * math.cos(tu[i]), zv[j]))
            uvs.append((0.01 + 0.98 * i / (NU - 1), 0.01 + 0.98 * j / (NV - 1)))
    faces = []
    for j in range(NV - 1):
        for i in range(NU - 1):
            a, b, c, e = j * NU + i, j * NU + i + 1, (j + 1) * NU + i + 1, (j + 1) * NU + i
            faces.append((a, e, c, b))     # Normale nach außen (weg von der Achse)
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    uv = me.uv_layers.new(name='UVMap')
    for p in me.polygons:
        for li in p.loop_indices: uv.data[li].uv = uvs[me.loops[li].vertex_index]
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o)
    # Normalen prüfen: sollen von der Achse weg zeigen
    p = me.polygons[len(me.polygons) // 2]; c = p.center
    if Vector((c.x, c.y - cy, 0)).dot(p.normal) < 0: me.flip_normals()
    return o, R

sheet, R = build('Vorhang_Bake', 41, 21, False)
arc = float(np.nanmean(R)) * (t1 - t0); hgt = z1 - z0
print('Vorhang Bogenlänge %.3f m, Höhe %.3f m, Radius %.3f..%.3f' % (arc, hgt, np.nanmin(R), np.nanmax(R)))

# Bake-Material am Mail: Emission umschaltbar
img = lambda n: bpy.data.images.load(os.path.join(tex, n))
mm = bpy.data.materials.new('MailBake'); mm.use_nodes = True; nt = mm.node_tree; nt.nodes.clear()
outn = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission')
bs = nt.nodes.new('ShaderNodeBsdfDiffuse'); mix = nt.nodes.new('ShaderNodeAddShader')
t_alb = nt.nodes.new('ShaderNodeTexImage'); t_alb.image = img('Mail_albedo.jpeg')
t_ao = nt.nodes.new('ShaderNodeTexImage'); t_ao.image = img('Mail_AO.jpeg'); t_ao.image.colorspace_settings.name = 'Non-Color'
t_r = nt.nodes.new('ShaderNodeTexImage'); t_r.image = img('Mail_roughness.jpeg'); t_r.image.colorspace_settings.name = 'Non-Color'
t_m = nt.nodes.new('ShaderNodeTexImage'); t_m.image = img('Mail_metallic.jpeg'); t_m.image.colorspace_settings.name = 'Non-Color'
t_n = nt.nodes.new('ShaderNodeTexImage'); t_n.image = bpy.data.images.load(os.path.join(tex, 'Mail_normal.png')); t_n.image.colorspace_settings.name = 'Non-Color'
nm = nt.nodes.new('ShaderNodeNormalMap'); nt.links.new(t_n.outputs[0], nm.inputs['Color']); nt.links.new(nm.outputs[0], bs.inputs['Normal'])
mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'; mul.inputs[0].default_value = 1.0
nt.links.new(t_alb.outputs[0], mul.inputs[6]); nt.links.new(t_ao.outputs[0], mul.inputs[7])
nt.links.new(em.outputs[0], mix.inputs[0]); nt.links.new(bs.outputs[0], mix.inputs[1]); nt.links.new(mix.outputs[0], outn.inputs[0])
em.inputs['Strength'].default_value = 1.0
mail.data.materials.clear(); mail.data.materials.append(mm)
# Diffuse-Anteil schwarz, damit EMIT nur Emission liefert (Normal-Bake nutzt die Normale des BSDF)
bs.inputs['Color'].default_value = (0, 0, 0, 1)

RW, RH = 2048, 1024
sm = bpy.data.materials.new('SheetBake'); sm.use_nodes = True; snt = sm.node_tree
tgt = snt.nodes.new('ShaderNodeTexImage'); snt.nodes.active = tgt
sheet.data.materials.append(sm)
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 4
bk = sc.render.bake; bk.use_selected_to_active = True; bk.cage_extrusion = 0.025; bk.max_ray_distance = 0.05; bk.margin = 0
bpy.ops.object.select_all(action='DESELECT'); mail.select_set(True); sheet.select_set(True); bpy.context.view_layer.objects.active = sheet
from PIL import Image
def bake(kind, src_socket, fname, ncol=False):
    im = bpy.data.images.new(fname, RW, RH, float_buffer=True); im.generated_color = (0, 0, 0, 0)
    tgt.image = im
    for l in list(em.inputs['Color'].links): nt.links.remove(l)
    if src_socket is not None: nt.links.new(src_socket, em.inputs['Color'])
    else: em.inputs['Color'].default_value = (1, 1, 1, 1)
    bpy.ops.object.bake(type=kind)
    px = np.array(im.pixels[:]).reshape(RH, RW, 4)[::-1]
    np.save(os.path.join(out, fname + '.npy'), px.astype(np.float32))
    return px
alpha = bake('EMIT', None, 'deckung')
col = bake('EMIT', mul.outputs[2], 'farbe')
rough = bake('EMIT', t_r.outputs[0], 'rauheit')
metal = bake('EMIT', t_m.outputs[0], 'metall')
bk.normal_space = 'TANGENT'
nrm = bake('NORMAL', None, 'normal')
print('Deckung Mittel %.3f, Anteil >0.5 %.3f' % (alpha[..., 0].mean(), (alpha[..., 0] > 0.5).mean()))
json.dump(dict(t0=float(t0), t1=float(t1), z0=float(z0), z1=float(z1), cy=float(cy), arc=arc, hoehe=float(hgt)), open(os.path.join(out, 'vorhang.json'), 'w'))
# Vorhang-Meshes für die LODs als OBJ (UV gleich), Medium/Low doppelseitig, Lowest einseitig
for nm_, NU, NV, dbl in (('Vorhang_LOD2', 29, 15, True), ('Vorhang_LOD1', 8, 5, True), ('Vorhang_LOD0', 3, 2, False), ('Vorhang_High', 2, 2, False)):
    o, _ = build(nm_, NU, NV, dbl)
    if dbl:
        import bmesh
        bm = bmesh.new(); bm.from_mesh(o.data)
        res = bmesh.ops.duplicate(bm, geom=bm.faces[:] + bm.verts[:] + bm.edges[:])
        nf = [g for g in res['geom'] if isinstance(g, bmesh.types.BMFace)]
        bmesh.ops.reverse_faces(bm, faces=nf, flip_multires=False)
        bm.to_mesh(o.data); bm.free()
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.wm.obj_export(filepath=os.path.join(d, nm_ + '.obj'), export_selected_objects=True, export_materials=False, export_normals=False, export_uv=True, export_triangulated_mesh=True, forward_axis='Y', up_axis='Z')
print('ok')
