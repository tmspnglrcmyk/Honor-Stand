# Helm · Upload-Anleitung Second Life

Wikingerhelm mit Brillenvisier und Kettenbehang, statisches Dekoobjekt für den 1st Axe Honor Stand. Maße 0,234 × 0,323 × 0,324 m (X × Y × Z), Visier zeigt nach −Y, Kettenbehang nach +Y.

## Dateien

| Datei | Zweck |
|---|---|
| `Helm.dae` | High, 173.917 Dreiecke (Originalgeometrie mit echten Kettenringen, Originalnormalen) |
| `Helm_LOD2.dae` | Medium, 11.970 Dreiecke, Kettenbehang als Alpha-Vorhang |
| `Helm_LOD1.dae` | Low, 2.314 Dreiecke |
| `Helm_LOD0.dae` | Lowest, 27 Dreiecke (Kuppel, Visierband, Behang) |
| `Helm_PHYS.dae` | Physik, Quader 12 Dreiecke |
| `Texturen/Helm_<Fläche>_Farbe.png` | Farbtextur mit eingebackenem AO, beim Vorhang mit Alpha |
| `Texturen/Helm_<Fläche>_Normal.png` | Normal Map, OpenGL, Alpha = Glanzgrad |
| `Texturen/Helm_<Fläche>_Glanz.png` | Specular Map, RGB = Glanzfarbe, Alpha = Umgebungsreflexion |
| `Texturen/PBR_optional/` | BaseColor, Normal, ORM je Fläche |
| `Blender/Helm.blend` | Arbeitsdatei mit High, LODs, Physik und Materialien, Texturen relativ verknüpft |

## Materialflächen

| Nr. | Material | High | Medium | Low | Lowest | Textur |
|---|---|---|---|---|---|---|
| 1 | Helm_Glocke | 58.368 | 5.002 | 1.202 | 21 | 1024 |
| 2 | Helm_Visier | 52.784 | 5.000 | 1.000 | 6 | 1024 |
| 3 | Helm_Ringe | 57.308 | – | – | – | 1024 |
| 4 | Helm_Futter | 5.456 | 400 | – | – | 512 |
| 5 | Helm_Vorhang | 1 (verdeckt) | 1.568 | 112 | – | 512, Alpha |

Die echten Kettenringe (Fläche 3) gibt es nur im High, das bis etwa 1,1 m Abstand gilt. Ab Medium trägt ein doppelseitiger Vorhang (Fläche 5) die Ringe als Alpha-Maske. Farbe, Deckung und Normalen sind von den Originalringen gebacken, Ringgröße und Muster bleiben gleich. Weil jede LOD-Stufe nur Materialien des High verwenden darf, enthält das High ein verdecktes Dreieck von 0,5 mm mit dem Vorhangmaterial (in der Glocke über dem Futter). Im Lowest liegt der Behang deckend auf der Glocken-Textur, eine Alpha-Maske würde aus der Ferne verschwinden.

Das Innenfutter fehlt ab Low, es ist von außen kaum sichtbar.

## Upload im Mesh-Uploader

1. `Helm.dae` als Modell wählen.
2. Reiter *Level of Detail*
   - Medium „Load from file“ `Helm_LOD2.dae`
   - Low „Load from file“ `Helm_LOD1.dae`
   - Lowest „Load from file“ `Helm_LOD0.dae`
3. Reiter *Physics* „From file“ `Helm_PHYS.dae`. Analyze ist nicht nötig.
4. Reiter *Upload options* Scale 1, „Include textures“ an.
5. „Calculate weights & fee“, Werte notieren, dann hochladen.

Größte Fläche im High hat 39.744 Vertices und liegt damit unter der Grenze von 65.536 je Fläche. Ob der Uploader große Flächen trotzdem aufteilt, konnte ich nicht prüfen. Meldet er mehr als 8 Flächen oder einen Fehler zur Vertexzahl, bitte Bescheid geben. Dann reduziere ich das High der Ringe.

## Nach dem Rezzen

| Fläche | Textur | Bumpiness (normal) | Shininess (specular) | Alpha mode |
|---|---|---|---|---|
| Helm_Glocke | `Helm_Glocke_Farbe.png` | `Helm_Glocke_Normal.png` | `Helm_Glocke_Glanz.png` | None |
| Helm_Visier | `Helm_Visier_Farbe.png` | `Helm_Visier_Normal.png` | `Helm_Visier_Glanz.png` | None |
| Helm_Ringe | `Helm_Ringe_Farbe.png` | `Helm_Ringe_Normal.png` | `Helm_Ringe_Glanz.png` | None |
| Helm_Futter | `Helm_Futter_Farbe.png` | `Helm_Futter_Normal.png` | `Helm_Futter_Glanz.png` | None |
| Helm_Vorhang | `Helm_Vorhang_Farbe.png` | `Helm_Vorhang_Normal.png` | `Helm_Vorhang_Glanz.png` | **Alpha masking, Cutoff 128** |

- Repeats 1, Offset 0, Rotation 0 für alle Karten.
- Glanz-Startwerte wie bei den Waffen (Glossiness 51, Environment 0, Farbe weiß). Alles zuerst über „Local“ im Texturwähler testen.
- Pflicht-Uploads 10 Texturen (Normal und Glanz je Fläche, die Farben kommen mit dem Mesh). Sparmöglichkeit: Futter-Glanz weglassen (Futter ist Leder ohne Metall, kaum sichtbar), dann 9.

## LI-Schätzung

Eigener Schätzer, Kalibrierung 0,706, Radius 0,257 m. Umschaltabstände etwa 1,1 m, 4,3 m, 8,6 m.

| Stufe | Dreiecke | komprimierte Bytes (geschätzt) | Anteil im Uploader |
|---|---|---|---|
| High | 173.917 | 1.682.295 | 0,16 |
| Medium | 11.970 | 158.987 | 0,22 |
| Low | 2.314 | 35.476 | 0,16 |
| Lowest | 27 | 440 | 0,83 |

Download im Uploader erwartet etwa **1,36**. Der Viewer rundet, erwarteter LI damit **1**. Der Abstand zur Grenze 1,5 ist knapp, und die Kalibrierung beruht auf einem einzigen Messpunkt. Zeigt der Uploader 2, sind die Hebel in dieser Reihenfolge das Low (−0,08 bei halber Dreieckszahl) und der Behang im Lowest (ohne ihn etwa −0,15).

## Was am Original geändert wurde

- Einheiten von Zentimeter auf Meter, Y-oben auf Z-oben, auf die Mitte der Bounding Box zentriert. Form und Größe unverändert.
- Unverschweißte Assimp-Geometrie verschweißt (keine sichtbare Änderung). Beim Visier entfielen dabei 448 entartete Dreiecke ohne Fläche.
- Texturen von 2048 auf 1024 (Futter 512), Normal Maps als Vektor gemittelt. Alle vier Normal Maps sind OpenGL (Prüfung über die Divergenz der Kanäle, an Axt und Schild gegengeprüft).
- AO aus den Originalkarten in die Farbtextur eingerechnet.
- LODs Medium und Low mit MeshLab (Quadric Edge Collapse mit Texturerhalt). Lowest von Hand aus den Originalradien gebaut, Farbe als 2-Pixel-UV-Fläche (Stahl der Außenseite, ohne Innenseite und Fugen). LOD-Punkte bis 3,3 mm auf die High-Box geklemmt, Bounding Box aller Stufen identisch.

## Schwächste Stelle

Das Low (4,3 bis 8,6 m) zeigt am rechten Wangenschutz einen abgelösten Splitter und schmale dunkle Fugen zwischen Glocke und Bändern. Mehr Dreiecke beheben das, kosten aber LI, und der Helm liegt schon nah an der Rundungsgrenze. Das Lowest ist eine grobe graue Kuppel mit kantigem Visierband. Ab 8,6 m ist der Helm nur wenige Pixel groß.

## Quelle und Lizenz

- Archiv im Repository `viking-helmet-free-download.zip` (4 Teile)
- verwendete Dateien `source/model.zip` → `model/model.dae` (Assimp-Export vom 8.6.2023) und `textures/*` (Helmet_42, Face_guard, Mail, Liner)
- Keine Lizenzdatei, kein Autorenname, keine URL im Archiv. Ordneraufbau `source/` und `textures/` und der Name „free-download“ sprechen für einen Sketchfab-Download. Eine Websuche fand das Modell nicht. Herkunft und Lizenz **unbelegt**.

**Vor einem Verkauf in SL** die Originalseite finden, Lizenz prüfen und den Nachweis ablegen. Viele kostenlose Sketchfab-Modelle stehen unter CC BY, dann ist eine Namensnennung in der Produktbeschreibung Pflicht. Das ist hier nicht geprüft.
