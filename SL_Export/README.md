# 1st Axe Honor Stand · SL-Export

Axt, Schild, Speer und Helm als statische Dekoobjekte für Second Life. Gemeinsame Vorschau in `Vorschau.png`, Upload-Schritte und Quellenangaben je Objekt in `<Objekt>/ANLEITUNG.md`.

| Objekt | Maße (m) | Dreiecke High / Med / Low / Lowest | Download geschätzt | LI erwartet |
|---|---|---|---|---|
| Axt | 0,27 × 0,024 × 0,114 | 870 / 422 / 162 / 18 | 0,66 | ~1 |
| Schild | 0,85 × 0,105 × 0,85 | 3.482 / 1.002 / 301 / 30 | 0,77 | ~1 |
| Speer | 0,046 × 0,035 × 2,20 | 12.506 / 702 / 122 / 14 | 1,33 | ~1 |
| Helm (Fassung 2) | 0,234 × 0,323 × 0,324 | 173.917 / 9.970 / 2.314 / 12 | 1,0 | ~1 |

Schätzung mit dem eigenen Schätzer und Faktor 0,706. Gemessen ist bisher nur der Helm in Fassung 1 (Uploader 1,9). Daraus ergibt sich ein Aufschlag von rund 75 Byte Kopfdaten je Materialfläche, den der Schätzer bis dahin nicht kannte. Neu gerechnet liegen Axt bei 0,86, Schild bei 0,96 und Speer bei **1,52**, der Speer dürfte also auf 2 LI gerundet werden. Upload, Land Impact und Gebühren werden im SL-Viewer geprüft.

## Ablauf

1. Geteilte ZIPs nach CLAUDE.md zusammengesetzt, alle sechs Archive mit `unzip -t` fehlerfrei.
2. Originale geladen, nur gleichmäßig skaliert, gedreht und zentriert (Details je Anleitung). Geometrie, Normalen und UVs des High unverändert (beim Speer UV nur in U gestreckt, weil die Textur zugeschnitten wurde).
3. Texturen auf SL-Größe, AO in die Farbtextur, Normal Map OpenGL, Glanzkarten für Legacy-Materialien, PBR-Satz optional.
4. LODs reduziert, Bounding Box aller Stufen exakt wie High, Lowest nach dem Farbpunkt-Verfahren.
5. Physik als Quader, DAE mit eigenem Writer (Blender 5 hat keinen Collada-Export), mit pycollada gegengelesen.

Werkzeuge in `_Werkzeug/` (Blender 5.2.3 als Python-Modul `bpy`, MeshLab über `pymeshlab`, Pillow, SciPy).

## Lizenz · offen

Keines der Archive enthält eine Lizenzdatei oder einen Autorennamen, auch das Helmarchiv nicht. Die Herkunftsseiten waren aus der Arbeitsumgebung nicht abrufbar. Vor einem Verkauf in SL muss die Lizenz je Objekt am Original belegt werden. Hinweise je Objekt stehen in der Anleitung.

## Helm

Verwendet wurde der Wikingerhelm mit Brillenvisier (`viking-helmet-free-download.zip`), nach Auswahl durch den Auftraggeber. Fünf Materialflächen. Die echten Kettenringe gibt es nur im High, ab Medium trägt ein gebackener Alpha-Vorhang die Ringe. Einzelheiten in `Helm/ANLEITUNG.md`. Der Nasalhelm (`early-medieval-nasal-helmet.zip`) wurde nicht bearbeitet.

## Nicht bearbeitet

`medieval weapons pack.zip` (12 Low-Poly-Waffen) nach Auftrag nur auf ausdrücklichen Wunsch.
