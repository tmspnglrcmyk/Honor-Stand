# Axt · Upload-Anleitung Second Life

Statisches Dekoobjekt für den 1st Axe Honor Stand. Maße 0.270 × 0.024 × 0.114 m (X × Y × Z).

## Dateien

| Datei | Zweck |
|---|---|
| `Axt.dae` | High, 870 Dreiecke (Originalgeometrie, Originalnormalen) |
| `Axt_LOD2.dae` | Medium, 422 Dreiecke |
| `Axt_LOD1.dae` | Low, 162 Dreiecke |
| `Axt_LOD0.dae` | Lowest, 18 Dreiecke |
| `Axt_PHYS.dae` | Physik, Quader 12 Dreiecke |
| `Texturen/Axt_Farbe.png` | Farbtextur mit eingebackenem AO (1024 × 1024) |
| `Texturen/Axt_Normal.png` | Normal Map, OpenGL, Alpha = Glanzgrad |
| `Texturen/Axt_Glanz.png` | Specular Map, RGB = Glanzfarbe, Alpha = Umgebungsreflexion |
| `Texturen/PBR_optional/` | BaseColor, Normal, ORM für PBR-Materialien (nur bei Bedarf) |
| `Blender/Axt.blend` | Arbeitsdatei mit High, LODs, Physik und Material, Texturen relativ verknüpft |

Alle LODs haben exakt die Bounding Box des High. Fehlende Extrempunkte sind mit je zwei winzigen Anker-Dreiecken (0,5 mm) gesichert, nichts ist gestreckt.

## Upload im Mesh-Uploader

1. Datei `Axt.dae` als Modell wählen.
2. Reiter *Level of Detail*
   - High ist `Axt.dae`
   - Medium „Load from file“ `Axt_LOD2.dae`
   - Low „Load from file“ `Axt_LOD1.dae`
   - Lowest „Load from file“ `Axt_LOD0.dae`
3. Reiter *Physics* „From file“ `Axt_PHYS.dae`. Analyze ist nicht nötig.
4. Reiter *Upload options* Scale 1, „Include textures“ an. Damit kommt `Axt_Farbe.png` mit.
5. „Calculate weights & fee“, Werte notieren (Download, Physik, Server), dann hochladen.

## Nach dem Rezzen

| Fläche | Textur | Bumpiness (normal) | Shininess (specular) |
|---|---|---|---|
| einzige Fläche (Material `Axt_Material`) | `Axt_Farbe.png` | `Axt_Normal.png` | `Axt_Glanz.png` |

- Repeats 1, Offset 0, Rotation 0 für alle drei Karten. Alpha mode „None“.
- Physics Shape Type „Convex Hull“ lassen.
- Startwerte für Glanz Glossiness 51, Environment 0, Farbe weiß. Laut SL-Wiki liest der Viewer den Glanzgrad aus dem Alphakanal der Normal Map und die Umgebungsreflexion aus dem Alphakanal der Specular Map. Im Viewer nicht geprüft. Normal und Glanz zuerst über „Local“ im Texturwähler kostenlos testen, erst dann hochladen.
- Pflicht-Uploads 3 Texturen (Farbe kommt mit dem Mesh, Normal und Glanz einzeln). Die PBR-Karten nur hochladen, wenn das Objekt ein PBR-Material bekommen soll.

## LI-Schätzung

Eigener Schätzer (Verfahren der Mesh-Anleitung, Kalibrierung 0,706 aus Jarlswoman v8). Radius 0.1471 m.

| Stufe | Dreiecke | komprimierte Bytes (geschätzt) |
|---|---|---|
| High | 870 | 8852 |
| Medium | 422 | 5332 |
| Low | 162 | 2271 |
| Lowest | 18 | 374 |

Download-Gewicht roh 0.933, im Uploader erwartet etwa **0.659**. Server-Gewicht mindestens 0,5, Physik als Quader klein. Erwarteter LI damit etwa **1**. Nicht im Viewer gemessen, bitte den Uploader-Wert in die STAND.md eintragen und neu eichen.

Lowest nach dem Farbpunkt-Verfahren. Statt eines einzigen UV-Punkts liegt jede Farbgruppe auf einer unverzerrten UV-Fläche von 2 Pixeln an einer Stelle mit flacher Normal Map. Ein Einzelpunkt macht die Tangentenbasis entartet und rendert mit Normal Map schwarz (im Blender-Test so aufgetreten).
Farbgruppen RGB (87, 86, 85) (22 % der Fläche), RGB (146, 133, 83) (78 % der Fläche). Nach jeder Änderung der Farbtextur neu bestimmen.

## Was am Original geändert wurde

Keine Änderung an Maß oder Ausrichtung. Länge 27 cm wie im Original (eher Beil als Streitaxt). Stiel liegt entlang X, Klinge zeigt nach unten.

Texturen von 2048 auf 1024 × 1024 verkleinert (Normal Map als Vektor gemittelt und renormiert). Normal-Map-Konvention OpenGL (Prüfung über eine Rinne in der Mittelrippe, Grünkanal), unverändert übernommen. Kein AO im Original. Selbstverschattung in Cycles gebacken (1024 px, 256 Samples, Distanz 8 cm), weich eingerechnet (25 % Mindesthelligkeit).

LODs mit MeshLab (Quadric Edge Collapse mit Texturerhalt), Lowest ohne Randerhalt. LOD-Punkte, die bei der Reduktion um wenige Millimeter über die High-Box hinausrutschten, wurden auf die Box geklemmt.

## Schwächste Stelle

Das Lowest (18 Dreiecke) zeigt die Klinge nur noch als schmalen Keil. Es greift ab etwa 4,9 m Abstand. Mehr Dreiecke dort kosten fast 1:1 LI, weil bei kleinen Objekten nahezu die gesamte Sichtfläche auf das Lowest entfällt. Wird die Axt in SL vergrößert, steigt der LI.

## Quelle und Lizenz

- Archiv im Repository `battle ax with runes.zip (2 Teile)`
- verwendete Dateien `axe2zip/axe2.fbx, Texturen axe2zip/2k/axe2_lp_axeLP_*.png`
- FBX aus Blender 3.5.1 exportiert, Texturen im Substance-Namensschema. Keine Lizenzdatei, kein Autorenname, keine Herkunfts-URL im Archiv.
- Websuche ergab einen möglichen Treffer „model of a viking battle ax with runes“ auf CGTrader (cgtrader.com/3d-models/military/melee/model-of-a-viking-battle-ax-with-runes). Die Seite war aus der Arbeitsumgebung nicht abrufbar, Übereinstimmung und Lizenz sind deshalb **nicht belegt**.

**Vor einem Verkauf in SL** die Lizenz an der Originalseite prüfen und den Nachweis (Screenshot der Lizenz, Kaufbeleg oder Download-Bestätigung) ablegen. Ohne belegte Lizenz nur zum eigenen Gebrauch verwenden.
