# AO je Teil aus der Kistengeometrie backen und mit den drei Original-AO-Karten korrelieren
import bpy, sys, os, json, numpy as np
from PIL import Image
d, tex = sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.open_mainfile(filepath=os.path.join(d, 'roh.blend'))
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 64
w = bpy.data.worlds.new('w'); sc.world = w; w.light_settings.distance = 0.15
R = 256
ref = {n: np.asarray(Image.open(os.path.join(tex, n + '_AO.jpg')).convert('L').resize((R, R), Image.BOX), float) / 255 for n in ('BOIS', 'METAL', 'ANNEAU2')}
res = {}
for o in [x for x in bpy.data.objects if x.type == 'MESH']:
    img = bpy.data.images.new('ao_' + o.name, R, R)
    m = bpy.data.materials.new('b_' + o.name); m.use_nodes = True; t = m.node_tree.nodes.new('ShaderNodeTexImage'); t.image = img; m.node_tree.nodes.active = t
    o.data.materials.clear(); o.data.materials.append(m)
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active = o
    sc.render.bake.margin = 0; img.generated_color = (0, 0, 0, 0)
    bpy.ops.object.bake(type='AO')
    px = np.array(img.pixels[:]).reshape(R, R, 4)[::-1]; a = px[..., 0]
    from PIL import ImageDraw
    mi = Image.new('L', (R, R), 0); dr = ImageDraw.Draw(mi); uv = o.data.uv_layers.active.data
    for pg in o.data.polygons:
        pts = [(uv[li].uv[0] * R, (1 - uv[li].uv[1]) * R) for li in pg.loop_indices]
        c = np.mean(pts, 0); pts = [tuple(c + (np.array(q) - c) * 0.8) for q in pts]   # Rand meiden
        dr.polygon(pts, fill=255)
    mask = np.asarray(mi) > 0
    sc_ = {n: float(np.corrcoef(a[mask], r[mask])[0, 1]) if mask.sum() > 20 else float('nan') for n, r in ref.items()}
    best = max(sc_, key=lambda k: -1 if np.isnan(sc_[k]) else sc_[k])
    res[o.name] = dict(best=best, korr={k: round(v, 3) for k, v in sc_.items()}, pixel=int(mask.sum()))
    print('%-16s %-8s %s px=%d' % (o.name, best, res[o.name]['korr'], mask.sum()))
json.dump(res, open(os.path.join(d, 'zuordnung.json'), 'w'), indent=1)
