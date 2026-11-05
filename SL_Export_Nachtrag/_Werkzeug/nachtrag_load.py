# lädt die Nachtragsmodelle mit ihren Texturen in eine Blender-Datei (Vorschau/Prüfung)
import bpy, sys, os, json
art, out = sys.argv[sys.argv.index('--')+1:][:2]
S = os.path.dirname(os.path.dirname(os.path.dirname(out))) + '/src2'
def mat(name, bc, nrm, rough=None, metal=None, mrao=None, ao=None):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; bs = nt.nodes['Principled BSDF']
    def tex(p, cs):
        t = nt.nodes.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(p); t.image.colorspace_settings.name = cs; return t
    nt.links.new(tex(bc, 'sRGB').outputs[0], bs.inputs['Base Color'])
    if mrao:
        t = tex(mrao, 'Non-Color'); sp = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(t.outputs[0], sp.inputs[0])
        nt.links.new(sp.outputs[0], bs.inputs['Metallic']); nt.links.new(sp.outputs[1], bs.inputs['Roughness'])
    if rough: nt.links.new(tex(rough, 'Non-Color').outputs[0], bs.inputs['Roughness'])
    if metal: nt.links.new(tex(metal, 'Non-Color').outputs[0], bs.inputs['Metallic'])
    nm = nt.nodes.new('ShaderNodeNormalMap'); nt.links.new(tex(nrm, 'Non-Color').outputs[0], nm.inputs['Color']); nt.links.new(nm.outputs[0], bs.inputs['Normal'])
    return m
if art == 'speer':
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.fbx(filepath=S + '/spear-fbx/spear-nachtrag-modell.fbx')
    T = S + '/spear-nachtrag-texturen-2k/'
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        k = o.material_slots[0].material.name
        o.data.materials.clear(); o.data.materials.append(mat(k, T + k + '_BC.png', T + k + '_N.png', mrao=T + k + '_MRAO.png'))
elif art == 'schild':
    bpy.ops.wm.open_mainfile(filepath=S + '/shield-nachtrag-blender/Shield.blend')
    T = S + '/shield-nachtrag-texturen/'
    for im in bpy.data.images:
        if im.name.startswith('Shield_'):
            im.unpack(method='REMOVE') if im.packed_file else None
            im.filepath = T + im.name; im.reload(); print('neu verknüpft', im.name, im.size[:])
elif art == 'kiste':
    bpy.ops.wm.open_mainfile(filepath=os.path.dirname(out) + '/roh.blend')
    T = S + '/viking-chest/inner/model/textures/'
    z = json.load(open(os.path.dirname(out) + '/zuordnung.json'))
    M = {n: mat(n, T + n + '_albedo.jpg', T + n + '_normal.png', rough=T + n + '_roughness.jpg', metal=T + n + '_metallic.jpg') for n in ('BOIS', 'METAL', 'ANNEAU2')}
    for o in bpy.data.objects:
        if o.type == 'MESH': o.data.materials.clear(); o.data.materials.append(M[z[o.name]['best']])
bpy.ops.wm.save_as_mainfile(filepath=out)
