# Helm: Zusammenbau mit fünf Materialflächen, LODs, Anker, Physik, DAE, LI-Schätzung, Arbeitsdatei
import bpy, bmesh, sys, os, json, zlib, math, numpy as np
from mathutils import Vector
from PIL import Image
from scipy.ndimage import gaussian_filter

wk, out = sys.argv[sys.argv.index('--') + 1:]
NAME = 'Helm'; d = os.path.join(wk, 'Helm'); od = os.path.join(out, NAME); tex = os.path.join(od, 'Texturen')
MATS = ['Helm_Glocke', 'Helm_Visier', 'Helm_Ringe', 'Helm_Futter', 'Helm_Vorhang']
bpy.ops.wm.open_mainfile(filepath=os.path.join(d, 'high.blend'))
sc = bpy.context.scene
for o in list(bpy.data.objects):
    if o.type == 'MESH' and not o.name.startswith('Helm_'): bpy.data.objects.remove(o, do_unlink=True)
col = bpy.data.collections.new('Helm – SL Export'); sc.collection.children.link(col)

# ---------- Materialien ----------
mats = []
for i, mn in enumerate(MATS):
    m = bpy.data.materials.new(mn); m.use_nodes = True; nt = m.node_tree; bs = nt.nodes['Principled BSDF']
    def img(p, cs):
        im = bpy.data.images.load(p); im.colorspace_settings.name = cs; return im
    tc = nt.nodes.new('ShaderNodeTexImage'); tc.image = img(os.path.join(tex, mn + '_Farbe.png'), 'sRGB')
    to = nt.nodes.new('ShaderNodeTexImage'); to.image = img(os.path.join(tex, 'PBR_optional', mn + '_ORM.png'), 'Non-Color')
    tn = nt.nodes.new('ShaderNodeTexImage'); tn.image = img(os.path.join(tex, 'PBR_optional', mn + '_Normal.png'), 'Non-Color')
    sp = nt.nodes.new('ShaderNodeSeparateColor'); nm = nt.nodes.new('ShaderNodeNormalMap')
    nt.links.new(tc.outputs['Color'], bs.inputs['Base Color']); nt.links.new(to.outputs['Color'], sp.inputs[0])
    nt.links.new(sp.outputs['Green'], bs.inputs['Roughness']); nt.links.new(sp.outputs['Blue'], bs.inputs['Metallic'])
    nt.links.new(tn.outputs['Color'], nm.inputs['Color']); nt.links.new(nm.outputs[0], bs.inputs['Normal'])
    if mn == 'Helm_Vorhang': nt.links.new(tc.outputs['Alpha'], bs.inputs['Alpha'])
    mats.append(m)

# Texturdaten für Farbflächen im Lowest
def texdata(mn):
    a = np.asarray(Image.open(os.path.join(tex, mn + '_Farbe.png')).convert('RGBA'), np.float64) / 255
    n = np.asarray(Image.open(os.path.join(tex, 'PBR_optional', mn + '_Normal.png')).convert('RGB'), np.float64) / 255
    bl = np.stack([gaussian_filter(a[..., i], 6) for i in range(4)], -1)
    nd = np.linalg.norm(np.stack([gaussian_filter(n[..., i], 4) for i in range(3)], -1) - [0.5, 0.5, 1.0], axis=-1)
    return bl, nd
def sample(img, uv):
    H, W = img.shape[:2]
    x = np.clip((uv[:, 0] * W).astype(int), 0, W - 1); y = np.clip(((1 - uv[:, 1]) * H).astype(int), 0, H - 1)
    return img[y, x], x, y
def puv(o):
    u = o.data.uv_layers.active.data
    return np.array([np.mean([u[li].uv[:] for li in p.loop_indices], 0) for p in o.data.polygons])
farbpunkte = {}
def collapse(o, cand_obj, mn, k, ziel=None, key=None):
    bl, nd = texdata(mn); H, W = bl.shape[:2]
    # Farben aus dem High (Flächenmittelpunkte liegen sicher in den UV-Inseln), Zuordnung über den nächsten High-Punkt im Raum
    from scipy.spatial import cKDTree
    hcen = np.array([p.center[:] for p in cand_obj.data.polygons]); harea = np.array([p.area for p in cand_obj.data.polygons]) + 1e-12
    hcol_all = sample(bl, puv(cand_obj))[0][:, :3]
    area = np.array([p.area for p in o.data.polygons]) + 1e-12
    if k == 2:
        c_ = hcol_all
        cc = np.array([np.percentile(c_.sum(1), 25), np.percentile(c_.sum(1), 75)])
        cc = np.array([c_[np.argmin(np.abs(c_.sum(1) - v))] for v in cc])
        for _ in range(30):
            hl = np.argmin(((c_[:, None] - cc[None]) ** 2).sum(-1), 1)
            cc = np.array([np.average(c_[hl == j], 0, harea[hl == j]) if (hl == j).any() else cc[j] for j in range(k)])
        tree = cKDTree(hcen)
        lab = []
        for p in o.data.polygons:
            pts_ = [p.center[:]] + [o.data.vertices[v].co[:] for v in p.vertices]
            _, ii = tree.query(np.array(pts_), k=8)
            lab.append(np.bincount(hl[ii.ravel()], weights=harea[ii.ravel()], minlength=k).argmax())
        lab = np.array(lab)
    else:
        lab = np.zeros(len(o.data.polygons), int)
    hc = puv(cand_obj); hcol, hx, hy = sample(bl, hc)
    bad = (hx < 10) | (hx > W - 11) | (hy < 10) | (hy > H - 11) | (hcol[:, 3] < 0.98)
    if k == 1: cc = np.array([ziel])
    score = lambda j: ((hcol[:, :3] - cc[j]) ** 2).sum(1) + 0.5 * nd[hy, hx] ** 2 + bad * 1e3
    pts = [hc[np.argmin(score(j))] for j in range(k)]
    uvd = o.data.uv_layers.active.data; V = np.array([v.co[:] for v in o.data.vertices])
    for j in range(k):
        polys = [p for p, l in zip(o.data.polygons, lab) if l == j]
        if not polys: continue
        vid = sorted({v for p in polys for v in p.vertices}); P = V[vid] - V[vid].mean(0)
        vt = np.linalg.svd(P, full_matrices=False)[2] if len(vid) > 2 else np.eye(3)
        pr = P @ vt[:2].T; ext = max(np.abs(pr).max(), 1e-9)
        mp = {v: pts[j] + pr[i] / ext * np.array([2.0 / W, 2.0 / H]) for i, v in enumerate(vid)}
        for p in polys:
            for li in p.loop_indices: uvd[li].uv = mp[o.data.loops[li].vertex_index]
    farbpunkte[key or mn] = [dict(rgb=[int(x * 255) for x in cc[j]], uv=[round(float(v), 4) for v in pts[j]], anteil=round(float(area[lab == j].sum() / area.sum()), 3)) for j in range(k)]

def aussen_farbe(h, mn):
    # flächengewichtetes Mittel der nach außen zeigenden High-Flächen (Innenseite ist durch AO sehr dunkel)
    bl, _ = texdata(mn); c = sample(bl, puv(h))[0][:, :3]
    cen = np.array([p.center[:] for p in h.data.polygons]); nr = np.array([p.normal[:] for p in h.data.polygons]); ar = np.array([p.area for p in h.data.polygons])
    C = np.array([0.0, cy_ref, 0.0]); auss = ((cen - C) * nr).sum(1) > 0
    c, ar = c[auss], ar[auss]
    hell = c.sum(1); grau = (np.abs(c[:, 0] - c[:, 2]) < 0.05) & (hell > np.percentile(hell, 35))   # Stahl: unbunt, ohne Fugen/Innenseite
    if grau.sum() > 50: return np.average(c[grau], 0, ar[grau])
    # zwei Farbgruppen (Stahl / Bronze), die flächengrößere gewinnt
    cc = np.array([c[np.argmin(np.abs(c.sum(1) - np.percentile(c.sum(1), q)))] for q in (25, 75)])
    for _ in range(30):
        lab = np.argmin(((c[:, None] - cc[None]) ** 2).sum(-1), 1)
        cc = np.array([np.average(c[lab == j], 0, ar[lab == j]) if (lab == j).any() else cc[j] for j in range(2)])
    w = [ar[lab == j].sum() for j in range(2)]
    return cc[int(np.argmax(w))]
def imp(path, nm):
    b = set(bpy.data.objects); bpy.ops.wm.obj_import(filepath=path, forward_axis='Y', up_axis='Z')
    o = [x for x in bpy.data.objects if x not in b][0]; o.name = nm; o.data.name = nm; o.data.materials.clear()
    return o
def smooth(o, ang=40):
    o.data.shade_smooth(); bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(ang))
def set_mat(o, idx):
    o.data.materials.clear()
    for m in mats: o.data.materials.append(m)
    for p in o.data.polygons: p.material_index = idx
def join(objs, nm):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]; bpy.ops.object.join()
    o = bpy.context.view_layer.objects.active; o.name = nm; o.data.name = nm
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o); return o

# ---------- High ----------
hp = {'Helmet_42': 0, 'Face_guard': 1, 'Mail': 2, 'Liner': 3}
parts = []
for t, i in hp.items():
    o = bpy.data.objects['Helm_' + t]; set_mat(o, i); parts.append(o)
G = np.array([v.co[:] for v in bpy.data.objects['Helm_Helmet_42'].data.vertices])
cy = (G[:, 1].min() + G[:, 1].max()) / 2
# verdecktes Mini-Dreieck für den Vorhang (liegt in der Helmglocke über dem Futter)
me = bpy.data.meshes.new('vd'); p0 = Vector((0, cy, G[:, 2].max() - 0.02))
me.from_pydata([p0, p0 + Vector((0.0005, 0, 0)), p0 + Vector((0, 0.0005, 0))], [], [(0, 1, 2)]); me.uv_layers.new(name='UVMap')
dummy = bpy.data.objects.new('vd', me); sc.collection.objects.link(dummy); set_mat(dummy, 4)
high = join(parts + [dummy], 'Helm_High')
hmin = np.array([v.co[:] for v in high.data.vertices]).min(0); hmax = np.array([v.co[:] for v in high.data.vertices]).max(0)
# UV des Mini-Dreiecks auf deckende Vorhangstelle (wird nach dem Lowest gesetzt)

# ---------- LODs ----------
plan = {
 'LOD2': [('Helmet_42_LOD2.obj', 0), ('Face_guard_LOD2.obj', 1), ('Liner_LOD2.obj', 3), ('Vorhang_LOD2.obj', 4)],
 'LOD1': [('Helmet_42_LOD1.obj', 0), ('Face_guard_LOD1.obj', 1), ('Vorhang_LOD1.obj', 4)],
 'LOD0': [('Helmet_42_LOD0.obj', 0), ('Face_guard_LOD0.obj', 1), ('Vorhang_LOD0.obj', 4)],
}
label = {'LOD2': 'Medium', 'LOD1': 'Low', 'LOD0': 'Lowest'}
cy_ref = cy
cand = {0: imp(os.path.join(d, 'high_Helmet_42.obj'), 'c0'), 1: imp(os.path.join(d, 'high_Face_guard.obj'), 'c1'), 4: imp(os.path.join(d, 'Vorhang_LOD2.obj'), 'c4')}
lods = {}
for key, lst in plan.items():
    objs = []
    for f, i in lst:
        o = imp(os.path.join(d, f), f'{key}_{i}')
        if i == 4 or key == 'LOD0': o.data.shade_smooth()
        else: smooth(o)
        if key == 'LOD0' and i == 4:
            # Kettenvorhang im Lowest deckend auf der Glocken-Textur (Alpha würde aus der Ferne verschwinden)
            va = np.asarray(Image.open(os.path.join(tex, 'Helm_Vorhang_Farbe.png')).convert('RGBA'), np.float64) / 255
            collapse(o, cand[0], MATS[0], 1, ziel=va[..., :3][va[..., 3] > 0.5].mean(0), key='Vorhang_auf_Glocke'); i = 0
        elif key == 'LOD0': collapse(o, cand[i], MATS[i], 1, ziel=aussen_farbe(cand[i], MATS[i]))
        set_mat(o, i); objs.append(o)
    o = join(objs, f'Helm_{key}')
    V = np.array([v.co[:] for v in o.data.vertices]); ueber = float(max((hmin - V.min(0)).max(), (V.max(0) - hmax).max(), 0))
    for v in o.data.vertices: v.co = Vector([min(max(v.co[i], hmin[i]), hmax[i]) for i in range(3)])
    V = np.array([v.co[:] for v in o.data.vertices]); dev = float(max(np.abs(V.min(0) - hmin).max(), np.abs(V.max(0) - hmax).max()))
    if dev > 1e-4:
        bm = bmesh.new(); bm.from_mesh(o.data); uvl = bm.loops.layers.uv.active; bm.faces.ensure_lookup_table()
        ref = next(f for f in bm.faces if f.material_index == 0).loops[0][uvl].uv.copy()
        for corner, s in ((hmin, 1), (hmax, -1)):
            p = Vector(corner); e = 0.0005 * s
            f = bm.faces.new([bm.verts.new(p), bm.verts.new(p + Vector((e, 0, 0))), bm.verts.new(p + Vector((0, e, 0)))]); f.material_index = 0
            for l in f.loops: l[uvl].uv = ref
        bm.to_mesh(o.data); bm.free()
    V = np.array([v.co[:] for v in o.data.vertices]); dev2 = float(max(np.abs(V.min(0) - hmin).max(), np.abs(V.max(0) - hmax).max()))
    lods[key] = dict(obj=o, label=label[key], geklemmt_mm=round(ueber * 1000, 2), vorher_mm=round(dev * 1000, 2), nachher_mm=round(dev2 * 1000, 3))
for c in cand.values(): bpy.data.objects.remove(c, do_unlink=True)
# Mini-Dreieck im High auf den Vorhang-Farbpunkt legen
va = np.asarray(Image.open(os.path.join(tex, 'Helm_Vorhang_Farbe.png')).convert('RGBA'))[..., 3]
yy, xx = np.argwhere(va[10:-10, 10:-10] == 255)[len(np.argwhere(va[10:-10, 10:-10] == 255)) // 2] + 10
vp = (xx / va.shape[1], 1 - yy / va.shape[0]); uvd = high.data.uv_layers.active.data
for p in high.data.polygons:
    if p.material_index == 4:
        for k, li in enumerate(p.loop_indices): uvd[li].uv = (vp[0] + 0.001 * (k == 1), vp[1] + 0.001 * (k == 2))

# ---------- Physik ----------
me = bpy.data.meshes.new('Helm_PHYS'); bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
for v in bm.verts: v.co = Vector([(hmin[i] + hmax[i]) / 2 + v.co[i] * (hmax[i] - hmin[i]) for i in range(3)])
bm.loops.layers.uv.new('UVMap'); bm.to_mesh(me); bm.free()
phys = bpy.data.objects.new('Helm_PHYS', me); col.objects.link(phys); phys.display_type = 'WIRE'; phys.hide_render = True
phys.data.materials.append(mats[0])

# ---------- Geometrie, DAE, LI ----------
def tri_data(o):
    m = o.data; m.calc_loop_triangles()
    P = np.array([v.co[:] for v in m.vertices]); N = np.array([n.vector[:] for n in m.corner_normals])
    T = np.array([d_.uv[:] for d_ in m.uv_layers.active.data])
    by = {}
    for lt in m.loop_triangles: by.setdefault(lt.material_index, []).append([(m.loops[li].vertex_index, li) for li in lt.loops])
    return P, N, T, by
def fmt(a): return ' '.join('%.6g' % x for x in np.asarray(a).ravel())
def write_dae(o, path, tex_on=True):
    P, N, T, by = tri_data(o); gid = o.name
    nu, ninv = np.unique(np.round(N, 5), axis=0, return_inverse=True); tu, tinv = np.unique(np.round(T, 6), axis=0, return_inverse=True)
    ninv = ninv.ravel(); tinv = tinv.ravel()
    used = sorted(by); x = ['<?xml version="1.0" encoding="utf-8"?>', '<COLLADA xmlns="http://www.collada.org/2005/11/COLLADASchema" version="1.4.1">',
        '<asset><contributor><authoring_tool>Honor-Stand SL Export (Blender %s, eigener DAE-Writer)</authoring_tool></contributor><unit name="meter" meter="1"/><up_axis>Z_UP</up_axis></asset>' % bpy.app.version_string]
    if tex_on:
        x.append('<library_images>' + ''.join(f'<image id="{MATS[i]}-img" name="{MATS[i]}_Farbe"><init_from>Texturen/{MATS[i]}_Farbe.png</init_from></image>' for i in used) + '</library_images>')
    x.append('<library_effects>')
    for i in used:
        mid = MATS[i]
        if tex_on:
            x.append(f'<effect id="{mid}-fx"><profile_COMMON><newparam sid="{mid}-surface"><surface type="2D"><init_from>{mid}-img</init_from></surface></newparam><newparam sid="{mid}-sampler"><sampler2D><source>{mid}-surface</source></sampler2D></newparam><technique sid="common"><lambert><diffuse><texture texture="{mid}-sampler" texcoord="UVMap"/></diffuse></lambert></technique></profile_COMMON></effect>')
        else:
            x.append(f'<effect id="{mid}-fx"><profile_COMMON><technique sid="common"><lambert><diffuse><color sid="diffuse">0.8 0.8 0.8 1</color></diffuse></lambert></technique></profile_COMMON></effect>')
    x.append('</library_effects><library_materials>' + ''.join(f'<material id="{MATS[i]}" name="{MATS[i]}"><instance_effect url="#{MATS[i]}-fx"/></material>' for i in used) + '</library_materials>')
    x.append(f'<library_geometries><geometry id="{gid}-mesh" name="{gid}"><mesh>')
    x.append(f'<source id="{gid}-pos"><float_array id="{gid}-pos-a" count="{P.size}">{fmt(P)}</float_array><technique_common><accessor source="#{gid}-pos-a" count="{len(P)}" stride="3"><param name="X" type="float"/><param name="Y" type="float"/><param name="Z" type="float"/></accessor></technique_common></source>')
    x.append(f'<source id="{gid}-nrm"><float_array id="{gid}-nrm-a" count="{nu.size}">{fmt(nu)}</float_array><technique_common><accessor source="#{gid}-nrm-a" count="{len(nu)}" stride="3"><param name="X" type="float"/><param name="Y" type="float"/><param name="Z" type="float"/></accessor></technique_common></source>')
    x.append(f'<source id="{gid}-uv"><float_array id="{gid}-uv-a" count="{tu.size}">{fmt(tu)}</float_array><technique_common><accessor source="#{gid}-uv-a" count="{len(tu)}" stride="2"><param name="S" type="float"/><param name="T" type="float"/></accessor></technique_common></source>')
    x.append(f'<vertices id="{gid}-vtx"><input semantic="POSITION" source="#{gid}-pos"/></vertices>')
    cnt = {}
    for i in used:
        idx = []
        for tri in by[i]:
            for vi, li in tri: idx += [vi, int(ninv[li]), int(tinv[li])]
        cnt[MATS[i]] = len(by[i])
        x.append(f'<triangles material="{MATS[i]}" count="{len(by[i])}"><input semantic="VERTEX" source="#{gid}-vtx" offset="0"/><input semantic="NORMAL" source="#{gid}-nrm" offset="1"/><input semantic="TEXCOORD" source="#{gid}-uv" offset="2" set="0"/><p>{" ".join(map(str, idx))}</p></triangles>')
    x.append('</mesh></geometry></library_geometries>')
    x.append(f'<library_visual_scenes><visual_scene id="Scene" name="Scene"><node id="{gid}" name="{gid}" type="NODE"><matrix sid="transform">1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1</matrix><instance_geometry url="#{gid}-mesh" name="{gid}"><bind_material><technique_common>')
    x.append(''.join(f'<instance_material symbol="{MATS[i]}" target="#{MATS[i]}"><bind_vertex_input semantic="UVMap" input_semantic="TEXCOORD" input_set="0"/></instance_material>' for i in used))
    x.append('</technique_common></bind_material></instance_geometry></node></visual_scene></library_visual_scenes><scene><instance_visual_scene url="#Scene"/></scene></COLLADA>')
    with open(path, 'w', newline='\n') as f: f.write('\n'.join(x) + '\n')
    return cnt
def lod_bytes(o):
    P, N, T, by = tri_data(o); lo, hi = P.min(0), P.max(0); sp = np.maximum(hi - lo, 1e-9)
    qp = np.round((P - lo) / sp * 65535).astype(np.uint16); qn = np.round((N + 1) / 2 * 65535).astype(np.uint16)
    total = 0; nverts = {}
    for i, tris in by.items():
        lis = [li for t in tris for _, li in t]; tl = T[lis].min(0); ts = np.maximum(T[lis].max(0) - tl, 1e-9)
        keys = {}; ind = []
        for t in tris:
            for vi, li in t:
                k = (tuple(qp[vi]), tuple(qn[li]), tuple(np.round((T[li] - tl) / ts * 65535).astype(np.uint16)))
                if k not in keys: keys[k] = len(keys)
                ind.append(keys[k])
        ks = list(keys)
        buf = b''.join(np.array(k[0] + k[1] + k[2], np.uint16).tobytes() for k in ks) + np.array(ind, np.uint16 if len(ks) < 65536 else np.uint32).tobytes()
        total += len(zlib.compress(buf, 9)) * 0.82; nverts[MATS[i]] = len(ks)
    return total, nverts
r = float(np.linalg.norm(hmax - hmin) / 2)
dm, dlo, dl = min(r / 0.24, 512), min(r / 0.06, 512), min(r / 0.03, 512)
ha = math.pi * dm ** 2; ma = math.pi * dlo ** 2 - ha; la = math.pi * dl ** 2 - math.pi * dlo ** 2; lw = max(102944 - math.pi * dl ** 2, 0)
B = {}; VC = {}
B['High'], VC['High'] = lod_bytes(high)
for key, dd in lods.items(): B[dd['label']], VC[dd['label']] = lod_bytes(dd['obj'])
t = {k: max(v - 128, 16) / 16 for k, v in B.items()}
est = (t['High'] * ha + t['Medium'] * ma + t['Low'] * la + t['Lowest'] * lw) / 102944 / 250000 * 15000
anteil = {k: round(t[k] * a / 102944 / 250000 * 15000 * 0.706, 3) for k, a in (('High', ha), ('Medium', ma), ('Low', la), ('Lowest', lw))}

os.makedirs(od, exist_ok=True); tri = {}
tri['High'] = write_dae(high, os.path.join(od, 'Helm.dae'))
for key, dd in lods.items(): tri[dd['label']] = write_dae(dd['obj'], os.path.join(od, f'Helm_{key}.dae'))
tri['Physik'] = write_dae(phys, os.path.join(od, 'Helm_PHYS.dae'), tex_on=False)
bd = os.path.join(od, 'Blender'); os.makedirs(bd, exist_ok=True)
for i, dd in enumerate(lods.values()): dd['obj'].location.x = (i + 1) * 0.35; dd['obj'].hide_render = True
phys.location.x = -0.35
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(bd, 'Helm.blend'), relative_remap=True)
bpy.ops.file.make_paths_relative(); bpy.ops.wm.save_mainfile()
if os.path.exists(os.path.join(bd, 'Helm.blend1')): os.remove(os.path.join(bd, 'Helm.blend1'))
rep = dict(objekt='Helm', masse_m=[round(float(x), 4) for x in hmax - hmin], radius_m=round(r, 4), dreiecke=tri,
           vertices=VC, bytes_geschaetzt={k: int(v) for k, v in B.items()}, anteil_uploader=anteil, farbpunkte=farbpunkte,
           lod_bbox={dd['label']: dict(geklemmt_mm=dd['geklemmt_mm'], vorher_mm=dd['vorher_mm'], nachher_mm=dd['nachher_mm']) for dd in lods.values()},
           download_schaetzwert=round(est, 3), download_uploader_geschaetzt=round(est * 0.706, 3))
json.dump(rep, open(os.path.join(d, 'bericht.json'), 'w'), indent=1, ensure_ascii=False)
print('BERICHT', json.dumps(rep, ensure_ascii=False))
