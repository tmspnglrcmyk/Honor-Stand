import sys, os, json, numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, distance_transform_edt, binary_erosion
T, V, OUT = sys.argv[1:4]
o = os.path.join(OUT, 'Helm', 'Texturen'); os.makedirs(os.path.join(o, 'PBR_optional'), exist_ok=True)
def f(im): return np.asarray(im, np.float64) / 255
def save(a, path, mode): Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8), mode).save(path, optimize=True)
def renorm(n, size):
    n = n * 2 - 1
    ch = [np.asarray(Image.fromarray(n[..., i].astype(np.float32), 'F').resize(size, Image.BOX)) for i in range(3)]
    n = np.stack(ch, -1); n /= np.linalg.norm(n, axis=-1, keepdims=True) + 1e-9; return n * 0.5 + 0.5
def legacy(name, base, n, rough, metal, ao, alpha=None):
    gloss = np.clip(1 - rough, 0.04, 1); sh = ao[..., None]
    farbe = base * sh
    spec = (0.22 * (1 - metal[..., None]) + base * metal[..., None]) * sh * (0.35 + 0.65 * gloss[..., None])
    env = metal * gloss * 0.8
    if alpha is None: save(farbe, os.path.join(o, name + '_Farbe.png'), 'RGB')
    else: save(np.dstack([farbe, alpha]), os.path.join(o, name + '_Farbe.png'), 'RGBA')
    save(np.dstack([n, gloss]), os.path.join(o, name + '_Normal.png'), 'RGBA')
    save(np.dstack([spec, env]), os.path.join(o, name + '_Glanz.png'), 'RGBA')
    save(base, os.path.join(o, 'PBR_optional', name + '_BaseColor.png'), 'RGB')
    save(n, os.path.join(o, 'PBR_optional', name + '_Normal.png'), 'RGB')
    save(np.dstack([ao, rough, metal]), os.path.join(o, 'PBR_optional', name + '_ORM.png'), 'RGB')
rep = {}
for src, name, size in (('Helmet_42', 'Helm_Glocke', 1024), ('Face_guard', 'Helm_Visier', 1024), ('Mail', 'Helm_Ringe', 1024), ('Liner', 'Helm_Futter', 512)):
    S = (size, size); ld = lambda k, m: Image.open(os.path.join(T, '%s_%s' % (src, k))).convert(m).resize(S, Image.LANCZOS)
    base = f(ld('albedo.jpeg', 'RGB')); rough = f(ld('roughness.jpeg', 'L')); metal = f(ld('metallic.jpeg', 'L')); ao = f(ld('AO.jpeg', 'L'))
    n = renorm(f(Image.open(os.path.join(T, src + '_normal.png')).convert('RGB')), S)
    legacy(name, base, n, rough, metal, ao); rep[name] = dict(px=size, ao=round(ao.mean(), 3), metall=round(float((metal > .5).mean()), 3))
# Vorhang aus den Bakes (2048x1024 -> 512x512)
S = (512, 512)
def ld(nm): return np.load(os.path.join(V, nm + '.npy'))
def rs(a): return np.asarray(Image.fromarray(a.astype(np.float32), 'F').resize(S, Image.BOX))
al = rs(ld('deckung')[..., 0])
lin = ld('farbe')[..., :3]; srgb = np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * np.clip(lin, 0, None) ** (1 / 2.4) - 0.055)
col = np.stack([rs(srgb[..., i]) / np.maximum(al, 1e-3) for i in range(3)], -1)   # vorgemischt -> gerade Farbe
rough = rs(ld('rauheit')[..., 0]) / np.maximum(al, 1e-3); metal = rs(ld('metall')[..., 0]) / np.maximum(al, 1e-3)
nb = ld('normal')[..., :3]; nb = np.where(ld('deckung')[..., :1] > 0.5, nb, np.array([0.5, 0.5, 1.0]))
n = renorm(nb, S)
mask = al > 0.5
# Farbe, Rauheit, Metall in transparente Bereiche ausdehnen (nächster gedeckter Pixel)
_, idx = distance_transform_edt(~mask, return_indices=True)
col = col[idx[0], idx[1]]; rough = np.clip(rough[idx[0], idx[1]], 0, 1); metal = np.clip(metal[idx[0], idx[1]], 0, 1)
alpha = gaussian_filter(al, 0.6)
alpha = np.where(alpha > 0.55, 1.0, 0.0)            # harte Maske für Alpha masking 128
ao = np.ones(S)                                      # AO steckt schon in der gebackenen Farbe
legacy('Helm_Vorhang', np.clip(col, 0, 1), n, rough, metal, ao, alpha)
rep['Helm_Vorhang'] = dict(px=512, deckung=round(float(alpha.mean()), 3))
print(json.dumps(rep))
