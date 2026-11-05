# Speer · Upload-Anleitung Second Life

Statisches Dekoobjekt für den 1st Axe Honor Stand. Maße 0.046 × 0.035 × 2.200 m (X × Y × Z).

## Dateien

| Datei | Zweck |
|---|---|
| `Speer.dae` | High, 12506 Dreiecke (Originalgeometrie, Originalnormalen) |
| `Speer_LOD2.dae` | Medium, 702 Dreiecke |
| `Speer_LOD1.dae` | Low, 122 Dreiecke |
| `Speer_LOD0.dae` | Lowest, 14 Dreiecke |
| `Speer_PHYS.dae` | Physik, Quader 12 Dreiecke |
| `Texturen/Speer_Farbe.png` | Farbtextur mit eingebackenem AO (256 × 1024) |
| `Texturen/Speer_Normal.png` | Normal Map, OpenGL, Alpha = Glanzgrad |
| `Texturen/Speer_Glanz.png` | Specular Map, RGB = Glanzfarbe, Alpha = Umgebungsreflexion |
| `Texturen/PBR_optional/` | BaseColor, Normal, ORM für PBR-Materialien (nur bei Bedarf) |
| `Blender/Speer.blend` | Arbeitsdatei mit High, LODs, Physik und Material, Texturen relativ verknüpft |

Alle LODs haben exakt die Bounding Box des High. Fehlende Extrempunkte sind mit je zwei winzigen Anker-Dreiecken (0,5 mm) gesichert, nichts ist gestreckt.

## Upload im Mesh-Uploader

1. Datei `Speer.dae` als Modell wählen.
2. Reiter *Level of Detail*
   - High ist `Speer.dae`
   - Medium „Load from file“ `Speer_LOD2.dae`
   - Low „Load from file“ `Speer_LOD1.dae`
   - Lowest „Load from file“ `Speer_LOD0.dae`
3. Reiter *Physics* „From file“ `Speer_PHYS.dae`. Analyze ist nicht nötig.
4. Reiter *Upload options* Scale 1, „Include textures“ an. Damit kommt `Speer_Farbe.png` mit.
5. „Calculate weights & fee“, Werte notieren (Download, Physik, Server), dann hochladen.

## Nach dem Rezzen

| Fläche | Textur | Bumpiness (normal) | Shininess (specular) |
|---|---|---|---|
| einzige Fläche (Material `Speer_Material`) | `Speer_Farbe.png` | `Speer_Normal.png` | `Speer_Glanz.png` |

- Repeats 1, Offset 0, Rotation 0 für alle drei Karten. Alpha mode „None“.
- Physics Shape Type „Convex Hull“ lassen.
- Startwerte für Glanz Glossiness 51, Environment 0, Farbe weiß. Laut SL-Wiki liest der Viewer den Glanzgrad aus dem Alphakanal der Normal Map und die Umgebungsreflexion aus dem Alphakanal der Specular Map. Im Viewer nicht geprüft. Normal und Glanz zuerst über „Local“ im Texturwähler kostenlos testen, erst dann hochladen.
- Pflicht-Uploads 3 Texturen (Farbe kommt mit dem Mesh, Normal und Glanz einzeln). Die PBR-Karten nur hochladen, wenn das Objekt ein PBR-Material bekommen soll.

## LI-Schätzung

Eigener Schätzer (Verfahren der Mesh-Anleitung, Kalibrierung 0,706 aus Jarlswoman v8). Radius 1.1004 m.

| Stufe | Dreiecke | komprimierte Bytes (geschätzt) |
|---|---|---|
| High | 12506 | 267146 |
| Medium | 702 | 8997 |
| Low | 122 | 1879 |
| Lowest | 14 | 326 |

Download-Gewicht roh 1.878, im Uploader erwartet etwa **1.326**. Server-Gewicht mindestens 0,5, Physik als Quader klein. Erwarteter LI damit etwa **1**. Nicht im Viewer gemessen, bitte den Uploader-Wert in die STAND.md eintragen und neu eichen.

Lowest nach dem Farbpunkt-Verfahren. Statt eines einzigen UV-Punkts liegt jede Farbgruppe auf einer unverzerrten UV-Fläche von 2 Pixeln an einer Stelle mit flacher Normal Map. Ein Einzelpunkt macht die Tangentenbasis entartet und rendert mit Normal Map schwarz (im Blender-Test so aufgetreten).
Farbgruppen RGB (162, 56, 47) (97 % der Fläche), RGB (137, 125, 114) (3 % der Fläche). Nach jeder Änderung der Farbtextur neu bestimmen.

## Was am Original geändert wurde

Gleichmäßig auf 2,20 m Länge skaliert (Original 4,71 m bei 7,5 cm Schaftdicke, ergibt jetzt 3,5 cm), aufrecht gestellt, Spitze nach +Z. Die Originaltextur nutzt nur einen Streifen von 10,7 % der Breite. Dieser Streifen wurde ausgeschnitten und die UVs nur in U gestreckt, daher die Textur 256 × 1024 statt 1024 × 1024. Keine neuen Nähte, volle Breitenauflösung.

Texturen von 2048 auf 256 × 1024 verkleinert (Normal Map als Vektor gemittelt und renormiert). Normal-Map-Konvention Die mitgelieferte Datei 63_SpearS1M_Normal_OpenGL.png wurde verwendet. AO aus 63_SpearS1M_Mixed_AO.png des Originals.

LODs mit MeshLab (Quadric Edge Collapse mit Texturerhalt), Lowest ohne Randerhalt. LOD-Punkte, die bei der Reduktion um wenige Millimeter über die High-Box hinausrutschten, wurden auf die Box geklemmt.

## Schwächste Stelle

Das High behält alle 12.506 Dreiecke des Originals und macht damit gut ein Drittel des Download-Gewichts aus. Ein reduziertes High würde etwa 0,3 LI sparen, verändert aber die Form, deshalb nicht gemacht.

## Quelle und Lizenz

- Archiv im Repository `weapon spear s1.zip`
- verwendete Dateien `970_SpearS1/63_SpearS1.fbx (Objekt Box.014), Texturen 63_SpearS1M_*.png`
- FBX aus Blender 4.3.2, Quellpfad im FBX deutet auf eine Asset-Sammlung („_1K_Asset_Work“). Die Datei enthält den Speer doppelt (Box.014 und Box.015 sind identisch), verwendet wurde einer. Keine Lizenzdatei, kein Autorenname, keine URL.
- Websuche nach „Spear S1“ und der Nummer 970 ergab keinen Treffer. Herkunft **unbekannt**.

**Vor einem Verkauf in SL** die Lizenz an der Originalseite prüfen und den Nachweis (Screenshot der Lizenz, Kaufbeleg oder Download-Bestätigung) ablegen. Ohne belegte Lizenz nur zum eigenen Gebrauch verwenden.
