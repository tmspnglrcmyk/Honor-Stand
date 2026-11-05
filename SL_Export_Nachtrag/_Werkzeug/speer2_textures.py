import sys, os, numpy as np
from PIL import Image
D, OUT = sys.argv[1:3]
o = os.path.join(OUT, 'Speer', 'Texturen'); os.makedirs(os.path.join(o, 'PBR_optional'), exist_ok=True)
S = (1024, 1024); f = lambda im: np.asarray(im, np.float64) / 255
def save(a, p, m): Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8), m).save(p, optimize=True)
base = f(Image.open(os.path.join(D, 'atlas_BC.png')).convert('RGB').resize(S, Image.LANCZOS))
mrao = f(Image.open(os.path.join(D, 'atlas_MRAO.png')).convert('RGB').resize(S, Image.LANCZOS))
metal, rough, ao = mrao[..., 0], mrao[..., 1], mrao[..., 2]
n = f(Image.open(os.path.join(D, 'atlas_N.png')).convert('RGB')) * 2 - 1
n[..., 1] *= -1                                      # DirectX -> OpenGL
n = np.stack([np.asarray(Image.fromarray(n[..., i].astype(np.float32), 'F').resize(S, Image.BOX)) for i in range(3)], -1)
roh = np.asarray(Image.open(os.path.join(D, 'atlas_N.png')).convert('RGB').resize(S, Image.NEAREST))
leer = roh.max(-1) < 3                                 # ungebackener Hintergrund (schwarz) -> flache Normale
n[leer] = [0, 0, 1]; n /= np.linalg.norm(n, axis=-1, keepdims=True) + 1e-9; n = n * 0.5 + 0.5
ao = np.where(leer, 1.0, ao)
gloss = np.clip(1 - rough, 0.04, 1); sh = ao[..., None]
spec = (0.22 * (1 - metal[..., None]) + base * metal[..., None]) * sh * (0.35 + 0.65 * gloss[..., None]); env = metal * gloss * 0.8
save(base * sh, os.path.join(o, 'Speer_Farbe.png'), 'RGB'); save(np.dstack([n, gloss]), os.path.join(o, 'Speer_Normal.png'), 'RGBA')
save(np.dstack([spec, env]), os.path.join(o, 'Speer_Glanz.png'), 'RGBA')
save(base, os.path.join(o, 'PBR_optional', 'Speer_BaseColor.png'), 'RGB'); save(n, os.path.join(o, 'PBR_optional', 'Speer_Normal.png'), 'RGB')
save(np.dstack([ao, rough, metal]), os.path.join(o, 'PBR_optional', 'Speer_ORM.png'), 'RGB')
print('AO %.2f Rauheit %.2f Metall-Anteil %.2f leer %.2f' % (ao[~leer].mean(), rough[~leer].mean(), (metal[~leer] > .5).mean(), leer.mean()))
