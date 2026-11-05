import sys, os, json, numpy as np
from PIL import Image
S = sys.argv[1]; WK = sys.argv[2]; OUT = sys.argv[3]
U = 'scandinavian_battle_shield/textures/original/Unity5/Unity Universal Render Pipeline (Metallic Standard)/2048x2048/Viking shield_Shield_'
A = 'battle_ax_with_runes/axe2zip/2k/axe2_lp_axeLP_'
P = 'weapon_spear_s1/970_SpearS1/63_SpearS1M_'
cfg = {
 'Axt':   dict(base=A+'BaseColor.png', normal=A+'Normal.png', rough=A+'Roughness.png', metal=A+'Metallic.png', ao=WK+'/Axt/ao_bake.png', size=(1024,1024), crop=None),
 'Schild':dict(base=U+'AlbedoTransparency.png', normal=U+'Normal.png', smooth=U+'MetallicSmoothness.png', metal=U+'MetallicSmoothness.png',
               ao='scandinavian_battle_shield/textures/original/UnrealEngine4/2048x2048/Viking shield_Shield_OcclusionRoughnessMetallic.png', size=(1024,1024), crop=None),
 'Speer': dict(base=P+'Base_color.png', normal=P+'Normal_OpenGL.png', rough=P+'Roughness.png', metal=P+'Metallic.png', ao=P+'Mixed_AO.png', size=(256,1024), crop=(0,0,224,2048)),
}
def load(path, mode, c):
    path = path if os.path.isabs(path) else os.path.join(S, path)
    im = Image.open(path)
    if im.mode == 'I;16' or im.mode == 'I': im = Image.fromarray((np.asarray(im, np.float64) / 257).clip(0, 255).astype(np.uint8))
    if c['crop'] and im.size == (2048, 2048): im = im.crop(c['crop'])
    return im.convert(mode)
def fit(im, c, res=Image.LANCZOS): return im.resize(c['size'], res)
def f(im): return np.asarray(im, np.float64) / 255.0
def save(a, path, mode):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8), mode).save(path, optimize=True)
rep = {}
for name, c in cfg.items():
    base = f(fit(load(c['base'], 'RGB', c), c))
    # Normal: als Vektor mitteln, renormieren
    nsrc = f(load(c['normal'], 'RGB', c)) * 2 - 1
    ch = [np.asarray(Image.fromarray(nsrc[..., i].astype(np.float32), 'F').resize(c['size'], Image.BOX)) for i in range(3)]
    n = np.stack(ch, -1); n /= np.linalg.norm(n, axis=-1, keepdims=True) + 1e-9; n = n * 0.5 + 0.5
    if 'smooth' in c:
        ms = load(c['smooth'], 'RGBA', c); ms = fit(ms, c)
        metal = f(ms)[..., 0]; rough = 1 - f(ms)[..., 3]
    else:
        rough = f(fit(load(c['rough'], 'L', c), c)); metal = f(fit(load(c['metal'], 'L', c), c))
    if name == 'Schild': ao = f(fit(load(c['ao'], 'RGB', c), c))[..., 0]
    else: ao = f(fit(load(c['ao'], 'L', c), c))
    if name == 'Axt':   # Selbstverschattung aus Bake: weich, nicht schwarz; ungebackener Rand neutral
        raw = f(load(c['ao'], 'L', c)); leer = np.asarray(Image.fromarray((raw <= 0).astype(np.uint8) * 255).resize(c['size'], Image.NEAREST)) > 0
        ao = np.where(leer, 1.0, 0.25 + 0.75 * ao)
    sh = ao[..., None]
    farbe = base * sh
    gloss = np.clip(1 - rough, 0.04, 1)
    spec_grey = np.full_like(base, 0.22)
    spec = (spec_grey * (1 - metal[..., None]) + base * metal[..., None]) * sh * (0.35 + 0.65 * gloss[..., None])
    env = metal * gloss * 0.8
    o = os.path.join(OUT, name, 'Texturen')
    save(farbe, os.path.join(o, name + '_Farbe.png'), 'RGB')
    save(np.dstack([n, gloss]), os.path.join(o, name + '_Normal.png'), 'RGBA')
    save(np.dstack([spec, env]), os.path.join(o, name + '_Glanz.png'), 'RGBA')
    save(base, os.path.join(o, 'PBR_optional', name + '_BaseColor.png'), 'RGB')
    save(n, os.path.join(o, 'PBR_optional', name + '_Normal.png'), 'RGB')
    save(np.dstack([ao, rough, metal]), os.path.join(o, 'PBR_optional', name + '_ORM.png'), 'RGB')
    rep[name] = dict(groesse=c['size'], ao_mittel=round(float(ao.mean()), 3), metall_anteil=round(float((metal > 0.5).mean()), 3), rauheit_mittel=round(float(rough.mean()), 3))
print(json.dumps(rep, indent=1))
