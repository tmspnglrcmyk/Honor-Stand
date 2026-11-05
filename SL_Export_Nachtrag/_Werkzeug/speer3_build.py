# Hilfen: Hülle mit unverzerrter 2-px-UV-Fläche erzeugen und OBJs zusammenfügen
import json, math, sys, os
def rd(p):
    V = []; T = []; F = []
    for l in open(p):
        s = l.split()
        if not s: continue
        if s[0] == 'v': V.append(tuple(map(float, s[1:4])))
        elif s[0] == 'vt': T.append(tuple(map(float, s[1:3])))
        elif s[0] == 'f': F.append([tuple(int(x) for x in q.split('/')[:2]) for q in s[1:]])
    return V, T, F
def huelle(d, N):
    h = json.load(open(os.path.join(d, 'huelle.json'))); px = 2 / 1024
    rv, rt, rf = rd(os.path.join(d, 'teil_rope.obj')); cx = sum(v[0] for v in rv) / len(rv); cy = sum(v[1] for v in rv) / len(rv)
    # Farbpunkt: Wicklungsfläche, deren Farbe dem flächengewichteten Mittel der Wicklung am nächsten liegt
    import numpy as np
    from PIL import Image
    from scipy.ndimage import gaussian_filter
    img = np.asarray(Image.open(os.environ['SPEER_FARBE']).convert('RGB'), float) / 255; H, W = img.shape[:2]
    bl = np.stack([gaussian_filter(img[..., i], 1.5) for i in range(3)], -1)
    V = np.array(rv); T_ = np.array(rt); cols = []; ws = []; uvs = []
    for f in rf:
        pv = V[[a - 1 for a, _ in f]]; pt = T_[[b - 1 for _, b in f]]; c = pt.mean(0)
        ar = 0.5 * np.linalg.norm(np.cross(pv[1] - pv[0], pv[2] - pv[0])) + (0.5 * np.linalg.norm(np.cross(pv[2] - pv[0], pv[3] - pv[0])) if len(pv) > 3 else 0)
        cols.append(bl[min(int((1 - c[1]) * H), H - 1), min(int(c[0] * W), W - 1)]); ws.append(ar); uvs.append(c)
    cols = np.array(cols); ws = np.array(ws); sicht = cols.mean(1) > 0.06   # verdeckte Unterseiten (AO ~0) nicht mitteln
    mean = np.average(cols[sicht], 0, ws[sicht])
    # ruhige Stelle innerhalb der Wicklungsinseln: lokales Mittel nahe der Zielfarbe, geringe Streuung (5x5)
    from PIL import ImageDraw
    from scipy.ndimage import uniform_filter
    mk = Image.new('L', (W, H), 0); dr = ImageDraw.Draw(mk)
    for f in rf:
        pt = T_[[b - 1 for _, b in f]] * [W, H]; pt[:, 1] = H - pt[:, 1]; c = pt.mean(0)
        dr.polygon([tuple(c + (q - c) * 0.7) for q in pt], fill=255)
    mk = np.asarray(mk) > 0
    lm = np.stack([uniform_filter(img[..., i], 5) for i in range(3)], -1)
    lv = sum(uniform_filter(img[..., i] ** 2, 5) - lm[..., i] ** 2 for i in range(3))
    score = ((lm - mean) ** 2).sum(-1) + 2 * np.sqrt(np.clip(lv, 0, None)) ** 2 + (~mk) * 1e3
    yy, xx = np.unravel_index(np.argmin(score), score.shape)
    u0 = [(xx + 0.5 - 1) / W, 1 - (yy + 0.5 + 1) / H]     # 2-px-Fläche liegt um den Punkt
    h['patch_std'] = float(np.sqrt(max(lv[yy, xx], 0))); h['patch_rgb'] = [int(v * 255) for v in lm[yy, xx]]
    h['hue_rgb'] = [int(x * 255) for x in mean]; h['hue_uv'] = u0; json.dump(h, open(os.path.join(d, 'huelle.json'), 'w'))
    V = [(cx + h['r'] * math.cos(2 * math.pi * i / N), cy + h['r'] * math.sin(2 * math.pi * i / N), z) for z in (h['z0'], h['z1']) for i in range(N)]
    T = [(u0[0] + px * (i % N) / N, u0[1] + px * (i // N)) for i in range(2 * N)]
    F = []
    for i in range(N):
        j = (i + 1) % N; F += [[(i + 1, i + 1), (j + 1, j + 1), (N + j + 1, N + j + 1)], [(i + 1, i + 1), (N + j + 1, N + j + 1), (N + i + 1, N + i + 1)]]
    return V, T, F
def merge(parts, out):
    V = []; T = []; F = []
    for pv, pt, pf in parts:
        ov, ot = len(V), len(T); V += pv; T += pt; F += [[(a + ov, b + ot) for a, b in f] for f in pf]
    with open(out, 'w') as f:
        for v in V: f.write('v %.6f %.6f %.6f\n' % v)
        for t in T: f.write('vt %.6f %.6f\n' % t)
        for fc in F: f.write('f ' + ' '.join('%d/%d' % x for x in fc) + '\n')
    return sum(len(x) - 2 for x in F)
if __name__ == '__main__':
    d, out, n = sys.argv[1], sys.argv[2], int(sys.argv[3]); parts = [rd(os.path.join(d, p)) for p in sys.argv[4:]]
    if n > 0: parts.append(huelle(d, n))
    print(os.path.basename(out), merge(parts, out), 'Dreiecke')
