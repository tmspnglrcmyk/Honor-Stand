import sys, os, numpy as np
from PIL import Image
T, OUT = sys.argv[1:3]
o = os.path.join(OUT, 'Kiste', 'Texturen'); os.makedirs(os.path.join(o, 'PBR_optional'), exist_ok=True)
f = lambda im: np.asarray(im, np.float64) / 255
def save(a, p, m): Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8), m).save(p, optimize=True)
for src, name, size in (('BOIS', 'Kiste_Holz', 1024), ('METAL', 'Kiste_Metall', 1024), ('ANNEAU2', 'Kiste_Nieten', 512)):
    S = (size, size); ld = lambda k, m: Image.open(os.path.join(T, '%s_%s' % (src, k))).convert(m).resize(S, Image.LANCZOS)
    base = f(ld('albedo.jpg', 'RGB')); rough = f(ld('roughness.jpg', 'L')); metal = f(ld('metallic.jpg', 'L')); ao = f(ld('AO.jpg', 'L'))
    n = f(Image.open(os.path.join(T, src + '_normal.png')).convert('RGB')) * 2 - 1
    n = np.stack([np.asarray(Image.fromarray(n[..., i].astype(np.float32), 'F').resize(S, Image.BOX)) for i in range(3)], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True) + 1e-9; n = n * 0.5 + 0.5
    gloss = np.clip(1 - rough, 0.04, 1); sh = ao[..., None]
    spec = (0.22 * (1 - metal[..., None]) + base * metal[..., None]) * sh * (0.35 + 0.65 * gloss[..., None]); env = metal * gloss * 0.8
    save(base * sh, os.path.join(o, name + '_Farbe.png'), 'RGB'); save(np.dstack([n, gloss]), os.path.join(o, name + '_Normal.png'), 'RGBA')
    save(np.dstack([spec, env]), os.path.join(o, name + '_Glanz.png'), 'RGBA')
    save(base, os.path.join(o, 'PBR_optional', name + '_BaseColor.png'), 'RGB'); save(n, os.path.join(o, 'PBR_optional', name + '_Normal.png'), 'RGB')
    save(np.dstack([ao, rough, metal]), os.path.join(o, 'PBR_optional', name + '_ORM.png'), 'RGB')
    print(name, size, 'AO %.2f Rauheit %.2f Metall %.2f' % (ao.mean(), rough.mean(), metal.mean()))
