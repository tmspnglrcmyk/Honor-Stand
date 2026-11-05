import sys, json, os
from PIL import Image, ImageDraw, ImageFont
L, WK, OUT = sys.argv[1:4]
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 26)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 34)
def im(n, size): return Image.open(os.path.join(L, n)).convert('RGB').resize(size, Image.LANCZOS)
Wd = 1800; tiles = []
r1 = [(im('hi_Axt_iso.png', (600, 600)), 'Axt schräg'), (im('hi_Schild_front.png', (600, 600)), 'Schild vorn'),
      (im('hi_Speer_front.png', (300, 600)), 'Speer'), (im('hi_Speer_kopf.png', (300, 600)), 'Speerspitze')]
r2 = [(im('hi_Axt_back.png', (600, 600)), 'Axt Rückseite'), (im('hi_Schild_back.png', (600, 600)), 'Schild hinten'), (im('hi_Schild_iso.png', (600, 600)), 'Schild schräg')]
r3 = [(im('hi_Helm_iso.png', (600, 600)), 'Helm schräg'), (im('hi_Helm_front.png', (600, 600)), 'Helm vorn'), (im('hi_Helm_back.png', (600, 600)), 'Helm hinten')]
lod = []
for o in ('Axt', 'Schild', 'Speer', 'Helm'):
    b = json.load(open(os.path.join(WK, o, 'bericht.json')))
    t = {k: (sum(v.values()) if isinstance(v, dict) else v) for k, v in b['dreiecke'].items()}
    lod.append((im('lods_%s.png' % o, (1800, 675)), '%s  LODs: High %d · Medium %d · Low %d · Lowest %d Dreiecke  |  Download geschätzt %.2f' % (o, t['High'], t['Medium'], t['Low'], t['Lowest'], b['download_uploader_geschaetzt'])))
H = 90 + 3 * 600 + 4 * 675
out = Image.new('RGB', (Wd, H), (60, 62, 66)); d = ImageDraw.Draw(out)
d.text((24, 26), '1st Axe Honor Stand · SL-Export Vorschau', font=FB, fill=(235, 235, 235))
y = 90; x = 0
for img, lab in r1:
    out.paste(img, (x, y)); d.text((x + 14, y + 10), lab, font=F, fill=(20, 20, 20)); x += img.width
y += 600; x = 0
for img, lab in r2:
    out.paste(img, (x, y)); d.text((x + 14, y + 10), lab, font=F, fill=(20, 20, 20)); x += img.width
y += 600; x = 0
for img, lab in r3:
    out.paste(img, (x, y)); d.text((x + 14, y + 10), lab, font=F, fill=(20, 20, 20)); x += img.width
y += 600
for img, lab in lod:
    out.paste(img, (0, y)); d.text((14, y + 10), lab, font=F, fill=(20, 20, 20)); y += 675
out.save(OUT, optimize=True)
print(out.size, os.path.getsize(OUT))
