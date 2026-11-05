# 1st Axe Honor Stand · SL-Export

Axt, Schild und Speer als statische Dekoobjekte für Second Life. Gemeinsame Vorschau in `Vorschau.png`, Upload-Schritte und Quellenangaben je Objekt in `<Objekt>/ANLEITUNG.md`.

| Objekt | Maße (m) | Dreiecke High / Med / Low / Lowest | Download geschätzt | LI erwartet |
|---|---|---|---|---|
| Axt | 0,27 × 0,024 × 0,114 | 870 / 422 / 162 / 18 | 0,66 | ~1 |
| Schild | 0,85 × 0,105 × 0,85 | 3.482 / 1.002 / 301 / 30 | 0,77 | ~1 |
| Speer | 0,046 × 0,035 × 2,20 | 12.506 / 702 / 122 / 14 | 1,33 | ~1 |

Schätzung mit dem eigenen Schätzer und Faktor 0,706. Nicht im Viewer gemessen. Upload, Land Impact und Gebühren werden im SL-Viewer geprüft.

## Ablauf

1. Geteilte ZIPs nach CLAUDE.md zusammengesetzt, alle sechs Archive mit `unzip -t` fehlerfrei.
2. Originale geladen, nur gleichmäßig skaliert, gedreht und zentriert (Details je Anleitung). Geometrie, Normalen und UVs des High unverändert (beim Speer UV nur in U gestreckt, weil die Textur zugeschnitten wurde).
3. Texturen auf SL-Größe, AO in die Farbtextur, Normal Map OpenGL, Glanzkarten für Legacy-Materialien, PBR-Satz optional.
4. LODs reduziert, Bounding Box aller Stufen exakt wie High, Lowest nach dem Farbpunkt-Verfahren.
5. Physik als Quader, DAE mit eigenem Writer (Blender 5 hat keinen Collada-Export), mit pycollada gegengelesen.

Werkzeuge in `_Werkzeug/` (Blender 5.2.3 als Python-Modul `bpy`, MeshLab über `pymeshlab`, Pillow, SciPy).

## Lizenz · offen

Keines der Archive enthält eine Lizenzdatei oder einen Autorennamen. Die Herkunftsseiten waren aus der Arbeitsumgebung nicht abrufbar. Vor einem Verkauf in SL muss die Lizenz je Objekt am Original belegt werden. Hinweise je Objekt stehen in der Anleitung.

## Helm · offen

Zwei Helmarchive liegen bei, aus den Dateien geht nicht hervor, welcher zum Stand gehört.
- `early-medieval-nasal-helmet.zip` slawischer Nasalhelm mit Kettenbrünne, FBX aus 3ds Max, rund 324.000 Dreiecke (davon 275.000 Kettenhemd), zwei Texturensätze.
- `viking-helmet-free-download.zip` Wikingerhelm mit Brillenvisier und Kettenbehang, DAE (Assimp, Zentimeter), rund 174.000 Dreiecke, vier Materialien.
Beide brauchen für SL eine starke Reduktion, das Kettengeflecht als Alpha-Textur statt Geometrie.

## Nicht bearbeitet

`medieval weapons pack.zip` (12 Low-Poly-Waffen) nach Auftrag nur auf ausdrücklichen Wunsch.
