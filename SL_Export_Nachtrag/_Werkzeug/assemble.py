# Zusammenbau je Objekt: High + LODs + Physik, Anker, Material, DAE, LI-Schätzung, Arbeitsdatei
import bpy, sys, os, json, zlib, math, numpy as np
from mathutils import Vector

name, wk, out = sys.argv[sys.argv.index('--') + 1:]
od = os.path.join(out, name)
bpy.ops.wm.open_mainfile(filepath=os.path.join(wk, name, 'high.blend'))
sc = bpy.context.scene
high = bpy.data.objects[name + '_High']
for c in list(sc.collection.children): pass

col = bpy.data.collections.new(name + ' – SL Export'); sc.collection.children.link(col)
for _c in list(high.users_collection): _c.objects.unlink(high)
col.objects.link(high)

def bbox(o):
    v = np.array([list(x.co) for x in o.data.vertices]); return v.min(0), v.max(0)

hmin, hmax = bbox(high)

# ---------- Lowest: UVs auf wenige Farbpunkte legen ----------
from PIL import Image
from scipy.ndimage import gaussian_filter
farbe = np.asarray(Image.open(os.path.join(od, 'Texturen', name + '_Farbe.png')).convert('RGB'), np.float64) / 255
H_, W_ = farbe.shape[:2]
blur = np.stack([gaussian_filter(farbe[..., i], 8) for i in range(3)], -1)
nrmtex = np.asarray(Image.open(os.path.join(od, 'Texturen', 'PBR_optional', name + '_Normal.png')).convert('RGB'), np.float64) / 255
nblur = np.stack([gaussian_filter(nrmtex[..., i], 4) for i in range(3)], -1)
ndev = np.linalg.norm(nblur - np.array([0.5, 0.5, 1.0]), axis=-1)
def sample(img, uv):
    x = np.clip((uv[:, 0] * W_).astype(int), 0, W_ - 1); y = np.clip(((1 - uv[:, 1]) * H_).astype(int), 0, H_ - 1)
    return img[y, x]
def poly_uv_centroids(o):
    uvd = o.data.uv_layers.active.data
    return np.array([np.mean([uvd[li].uv[:] for li in p.loop_indices], 0) for p in o.data.polygons])
def collapse_uv(o, high):
    cu = poly_uv_centroids(o); col_ = sample(blur, cu)
    area = np.array([p.area for p in o.data.polygons]) + 1e-12
    # k-means mit k=2 (Metall / Holz bzw. Farbe)
    c = np.array([col_[np.argmin(col_.sum(1))], col_[np.argmax(col_.sum(1))]])
    for _ in range(20):
        lab = np.argmin(((col_[:, None] - c[None]) ** 2).sum(-1), 1)
        c = np.array([np.average(col_[lab == k], 0, area[lab == k]) if (lab == k).any() else c[k] for k in range(2)])
    # Kandidaten: Flächenmittelpunkte des High (liegen sicher in UV-Inseln)
    hc = poly_uv_centroids(high); hcol = sample(blur, hc)
    hx = np.clip((hc[:, 0] * W_).astype(int), 0, W_ - 1); hy = np.clip(((1 - hc[:, 1]) * H_).astype(int), 0, H_ - 1)
    hdev = ndev[hy, hx]
    rand = (hx < 10) | (hx > W_ - 11) | (hy < 10) | (hy > H_ - 11)
    hdev = np.where(rand, 1e3, hdev)
    pts = [hc[np.argmin(((hcol - c[k]) ** 2).sum(1) + 0.5 * hdev ** 2)] for k in range(2)]
    # winzige, unverzerrte UV-Fläche (2 px) statt Einzelpunkt, damit die Tangentenbasis definiert bleibt
    uvd = o.data.uv_layers.active.data
    V = np.array([v.co[:] for v in o.data.vertices])
    for k in range(2):
        polys = [p for p, l in zip(o.data.polygons, lab) if l == k]
        if not polys: continue
        vid = sorted({v for p in polys for v in p.vertices}); P = V[vid] - V[vid].mean(0)
        _, _, vt = np.linalg.svd(P, full_matrices=False) if len(vid) > 2 else (None, None, np.eye(3))
        proj = P @ vt[:2].T; ext = max(np.abs(proj).max(), 1e-9)
        size = np.array([2.0 / W_, 2.0 / H_])
        m = {v: pts[k] + proj[i] / ext * size for i, v in enumerate(vid)}
        for p in polys:
            for li in p.loop_indices: uvd[li].uv = m[o.data.loops[li].vertex_index]
    global lowest_farben
    lowest_farben = [dict(farbe_rgb=[int(x * 255) for x in c[k]], uv=[round(float(v), 4) for v in pts[k]], anteil=round(float(area[lab == k].sum() / area.sum()), 3)) for k in range(2)]
lowest_farben = None

# ---------- LODs einlesen ----------
lods = {}
for key, label in (('LOD2', 'Medium'), ('LOD1', 'Low'), ('LOD0', 'Lowest')):
    before = set(bpy.data.objects)
    bpy.ops.wm.obj_import(filepath=os.path.join(wk, name, key + '.obj'), forward_axis='Y', up_axis='Z')
    o = [x for x in bpy.data.objects if x not in before][0]
    for c in o.users_collection: c.objects.unlink(o)
    col.objects.link(o)
    o.name = f'{name}_{key}'; o.data.name = o.name
    o.data.materials.clear()
    o.data.shade_smooth()
    try:
        bpy.context.view_layer.objects.active = o; o.select_set(True)
        bpy.ops.object.shade_smooth_by_angle(angle=math.radians(40))
        o.select_set(False)
    except Exception as e:
        print('smooth by angle:', e)
    # Punkte, die durch die Reduktion über die High-Box hinausragen, auf die Box klemmen (Millimeterbereich)
    lmin0, lmax0 = bbox(o)
    ueber = float(max((hmin - lmin0).max(), (lmax0 - hmax).max(), 0))
    for v in o.data.vertices:
        v.co = Vector([min(max(v.co[i], hmin[i]), hmax[i]) for i in range(3)])
    if key == 'LOD0':
        collapse_uv(o, high)
    # Anker, falls Bounding Box abweicht (nie strecken)
    lmin, lmax = bbox(o)
    dev = float(max(np.abs(lmin - hmin).max(), np.abs(lmax - hmax).max()))
    anchors = 0
    if dev > 1e-4:
        me = o.data
        import bmesh
        bm = bmesh.new(); bm.from_mesh(me)
        uvl = bm.loops.layers.uv.active
        bm.faces.ensure_lookup_table(); ref = bm.faces[0].loops[0][uvl].uv.copy()
        for corner, sgn in ((hmin, 1), (hmax, -1)):
            p = Vector(corner); e = 0.0005 * sgn
            vs = [bm.verts.new(p), bm.verts.new(p + Vector((e, 0, 0))), bm.verts.new(p + Vector((0, e, 0)))]
            f = bm.faces.new(vs)
            # UV einer vorhandenen Ecke übernehmen
            for l in f.loops: l[uvl].uv = ref
            anchors += 1
        bm.to_mesh(me); bm.free()
        lmin, lmax = bbox(o); dev2 = float(max(np.abs(lmin - hmin).max(), np.abs(lmax - hmax).max()))
    else:
        dev2 = dev
    lods[key] = dict(label=label, obj=o, geklemmt_mm=round(ueber * 1000, 3), abweichung_vorher_mm=round(dev * 1000, 3), abweichung_nachher_mm=round(dev2 * 1000, 3), anker=anchors)

# ---------- Physik: einfache Box ----------
import bmesh
me = bpy.data.meshes.new(name + '_PHYS'); bm = bmesh.new()
bmesh.ops.create_cube(bm, size=1.0)
for v in bm.verts:
    v.co = Vector([(hmin[i] + hmax[i]) / 2 + v.co[i] * (hmax[i] - hmin[i]) for i in range(3)])
uvl = bm.loops.layers.uv.new('UVMap')
bm.to_mesh(me); bm.free()
phys = bpy.data.objects.new(name + '_PHYS', me); col.objects.link(phys)
phys.display_type = 'WIRE'; phys.hide_render = True

# ---------- Material ----------
tex = os.path.join(od, 'Texturen')
mat = bpy.data.materials.new(name + '_Material'); mat.use_nodes = True
nt = mat.node_tree; bsdf = nt.nodes['Principled BSDF']
def img(path, cs):
    im = bpy.data.images.load(path); im.colorspace_settings.name = cs; return im
t_col = nt.nodes.new('ShaderNodeTexImage'); t_col.image = img(os.path.join(tex, name + '_Farbe.png'), 'sRGB'); t_col.location = (-600, 300)
t_orm = nt.nodes.new('ShaderNodeTexImage'); t_orm.image = img(os.path.join(tex, 'PBR_optional', name + '_ORM.png'), 'Non-Color'); t_orm.location = (-600, 0)
t_nrm = nt.nodes.new('ShaderNodeTexImage'); t_nrm.image = img(os.path.join(tex, 'PBR_optional', name + '_Normal.png'), 'Non-Color'); t_nrm.location = (-600, -300)
sep = nt.nodes.new('ShaderNodeSeparateColor'); sep.location = (-300, 0)
nm = nt.nodes.new('ShaderNodeNormalMap'); nm.location = (-300, -300)
nt.links.new(t_col.outputs['Color'], bsdf.inputs['Base Color'])
nt.links.new(t_orm.outputs['Color'], sep.inputs['Color'])
nt.links.new(sep.outputs['Green'], bsdf.inputs['Roughness'])
nt.links.new(sep.outputs['Blue'], bsdf.inputs['Metallic'])
nt.links.new(t_nrm.outputs['Color'], nm.inputs['Color'])
nt.links.new(nm.outputs['Normal'], bsdf.inputs['Normal'])
for o in [high] + [d['obj'] for d in lods.values()] + [phys]:
    o.data.materials.clear(); o.data.materials.append(mat)

# ---------- Geometrie auslesen ----------
def mesh_data(o):
    m = o.data
    m.calc_loop_triangles()
    P = np.array([list(v.co) for v in m.vertices])
    N = np.array([list(n.vector) for n in m.corner_normals]) if hasattr(m, 'corner_normals') else np.array([list(l.normal) for l in m.loops])
    uvd = m.uv_layers.active.data if m.uv_layers.active else None
    T = np.array([list(d.uv) for d in uvd]) if uvd else np.zeros((len(m.loops), 2))
    tris = []
    for lt in m.loop_triangles:
        tris.append([(m.loops[li].vertex_index, li) for li in lt.loops])
    return P, N, T, tris

# ---------- DAE-Writer ----------
def fmt(a): return ' '.join('%.6g' % x for x in np.asarray(a).ravel())
def write_dae(o, path, with_tex=True):
    P, N, T, tris = mesh_data(o)
    # Normalen und UVs deduplizieren
    Nq = np.round(N, 5); Tq = np.round(T, 6)
    nu, ninv = np.unique(Nq, axis=0, return_inverse=True)
    tu, tinv = np.unique(Tq, axis=0, return_inverse=True)
    ninv = ninv.ravel(); tinv = tinv.ravel()
    idx = []
    for tri in tris:
        for vi, li in tri: idx += [vi, int(ninv[li]), int(tinv[li])]
    gid = o.name.replace(' ', '_'); mid = name + '_Material'
    rel = 'Texturen/' + name + '_Farbe.png'
    x = []
    x.append('<?xml version="1.0" encoding="utf-8"?>')
    x.append('<COLLADA xmlns="http://www.collada.org/2005/11/COLLADASchema" version="1.4.1">')
    x.append('<asset><contributor><authoring_tool>Honor-Stand SL Export (Blender %s, eigener DAE-Writer)</authoring_tool></contributor>' % bpy.app.version_string)
    x.append('<unit name="meter" meter="1"/><up_axis>Z_UP</up_axis></asset>')
    if with_tex:
        x.append(f'<library_images><image id="{mid}-img" name="{name}_Farbe"><init_from>{rel}</init_from></image></library_images>')
    x.append(f'<library_effects><effect id="{mid}-fx"><profile_COMMON>')
    if with_tex:
        x.append(f'<newparam sid="{mid}-surface"><surface type="2D"><init_from>{mid}-img</init_from></surface></newparam>')
        x.append(f'<newparam sid="{mid}-sampler"><sampler2D><source>{mid}-surface</source></sampler2D></newparam>')
        diff = f'<texture texture="{mid}-sampler" texcoord="UVMap"/>'
    else:
        diff = '<color sid="diffuse">0.8 0.8 0.8 1</color>'
    x.append(f'<technique sid="common"><lambert><diffuse>{diff}</diffuse></lambert></technique></profile_COMMON></effect></library_effects>')
    x.append(f'<library_materials><material id="{mid}" name="{mid}"><instance_effect url="#{mid}-fx"/></material></library_materials>')
    x.append(f'<library_geometries><geometry id="{gid}-mesh" name="{gid}"><mesh>')
    x.append(f'<source id="{gid}-pos"><float_array id="{gid}-pos-a" count="{P.size}">{fmt(P)}</float_array><technique_common><accessor source="#{gid}-pos-a" count="{len(P)}" stride="3"><param name="X" type="float"/><param name="Y" type="float"/><param name="Z" type="float"/></accessor></technique_common></source>')
    x.append(f'<source id="{gid}-nrm"><float_array id="{gid}-nrm-a" count="{nu.size}">{fmt(nu)}</float_array><technique_common><accessor source="#{gid}-nrm-a" count="{len(nu)}" stride="3"><param name="X" type="float"/><param name="Y" type="float"/><param name="Z" type="float"/></accessor></technique_common></source>')
    x.append(f'<source id="{gid}-uv"><float_array id="{gid}-uv-a" count="{tu.size}">{fmt(tu)}</float_array><technique_common><accessor source="#{gid}-uv-a" count="{len(tu)}" stride="2"><param name="S" type="float"/><param name="T" type="float"/></accessor></technique_common></source>')
    x.append(f'<vertices id="{gid}-vtx"><input semantic="POSITION" source="#{gid}-pos"/></vertices>')
    x.append(f'<triangles material="{mid}" count="{len(tris)}"><input semantic="VERTEX" source="#{gid}-vtx" offset="0"/><input semantic="NORMAL" source="#{gid}-nrm" offset="1"/><input semantic="TEXCOORD" source="#{gid}-uv" offset="2" set="0"/><p>{" ".join(map(str, idx))}</p></triangles>')
    x.append('</mesh></geometry></library_geometries>')
    x.append(f'<library_visual_scenes><visual_scene id="Scene" name="Scene"><node id="{gid}" name="{gid}" type="NODE"><matrix sid="transform">1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1</matrix>')
    x.append(f'<instance_geometry url="#{gid}-mesh" name="{gid}"><bind_material><technique_common><instance_material symbol="{mid}" target="#{mid}"><bind_vertex_input semantic="UVMap" input_semantic="TEXCOORD" input_set="0"/></instance_material></technique_common></bind_material></instance_geometry>')
    x.append('</node></visual_scene></library_visual_scenes><scene><instance_visual_scene url="#Scene"/></scene></COLLADA>')
    with open(path, 'w', newline='\n') as f: f.write('\n'.join(x) + '\n')
    return len(tris)

# ---------- LI-Schätzung (Verfahren aus der Mesh-Anleitung) ----------
def lod_bytes(o):
    P, N, T, tris = mesh_data(o)
    lo, hi = P.min(0), P.max(0); span = np.maximum(hi - lo, 1e-9)
    qp = np.round((P - lo) / span * 65535).astype(np.uint16)
    qn = np.round((N + 1) / 2 * 65535).astype(np.uint16)
    tl, th = T.min(0), T.max(0); ts = np.maximum(th - tl, 1e-9)
    qt = np.round((T - tl) / ts * 65535).astype(np.uint16)
    keys = {}; ind = []; verts = []
    for tri in tris:
        for vi, li in tri:
            k = (tuple(qp[vi]), tuple(qn[li]), tuple(qt[li]))
            if k not in keys: keys[k] = len(keys); verts.append(k)
            ind.append(keys[k])
    buf = b''.join(np.array(k[0], np.uint16).tobytes() for k in verts) + \
          b''.join(np.array(k[1], np.uint16).tobytes() for k in verts) + \
          b''.join(np.array(k[2], np.uint16).tobytes() for k in verts) + np.array(ind, np.uint16).tobytes()
    return len(zlib.compress(buf, 9)) * 0.82 + 75, len(verts)   # +75 Byte Kopfdaten je Fläche (Messung Helm)

r = float(np.linalg.norm(hmax - hmin) / 2)
dm, dlo, dl = min(r / 0.24, 512), min(r / 0.06, 512), min(r / 0.03, 512)
ha = math.pi * dm ** 2; ma = math.pi * dlo ** 2 - ha; la = math.pi * dl ** 2 - math.pi * dlo ** 2; lw = max(102944 - math.pi * dl ** 2, 0)
B = {}
B['High'], vh = lod_bytes(high)
for key, d in lods.items(): B[d['label']], d['vertices'] = lod_bytes(d['obj'])
t = {k: max(v - 128, 16) / 16 for k, v in B.items()}
est = (t['High'] * ha + t['Medium'] * ma + t['Low'] * la + t['Lowest'] * lw) / 102944 / 250000 * 15000

# ---------- Export ----------
os.makedirs(od, exist_ok=True)
tri = {}
tri['High'] = write_dae(high, os.path.join(od, name + '.dae'))
for key, d in lods.items(): tri[d['label']] = write_dae(d['obj'], os.path.join(od, f'{name}_{key}.dae'))
tri['Physik'] = write_dae(phys, os.path.join(od, name + '_PHYS.dae'), with_tex=False)

# Arbeitsdatei mit relativen Texturpfaden
bd = os.path.join(od, 'Blender'); os.makedirs(bd, exist_ok=True)
for o in [d['obj'] for d in lods.values()]: o.hide_render = True
for i, d in enumerate(lods.values()): d['obj'].location.x = (i + 1) * (hmax[0] - hmin[0]) * 1.4 + 0.05
phys.location.x = -(hmax[0] - hmin[0]) * 1.4 - 0.05
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(bd, name + '.blend'), relative_remap=True)
bpy.ops.file.make_paths_relative()
bpy.ops.wm.save_mainfile()
b1 = os.path.join(bd, name + '.blend1')
if os.path.exists(b1): os.remove(b1)

info = json.load(open(os.path.join(wk, name, 'info.json')))
rep = dict(objekt=name, masse_m=[round(float(x), 4) for x in (hmax - hmin)], radius_m=round(r, 4),
           dreiecke=tri, bytes_geschaetzt={k: int(v) for k, v in B.items()},
           lowest_farbpunkte=lowest_farben, lod_bbox={d['label']: dict(geklemmt_mm=d['geklemmt_mm'], vorher_mm=d['abweichung_vorher_mm'], nachher_mm=d['abweichung_nachher_mm'], anker=d['anker']) for d in lods.values()},
           download_schaetzwert=round(est, 3), download_uploader_geschaetzt=round(est * 0.706, 3),
           skalierung=info['skalierung'], zielmass=info['zielmass'])
json.dump(rep, open(os.path.join(wk, name, 'bericht.json'), 'w'), indent=1, ensure_ascii=False)
print('BERICHT', json.dumps(rep, ensure_ascii=False))
