# Schild · Upload-Anleitung Second Life

Statisches Dekoobjekt für den 1st Axe Honor Stand. Maße 0.850 × 0.105 × 0.850 m (X × Y × Z).

## Dateien

| Datei | Zweck |
|---|---|
| `Schild.dae` | High, 3482 Dreiecke (Originalgeometrie, Originalnormalen) |
| `Schild_LOD2.dae` | Medium, 1002 Dreiecke |
| `Schild_LOD1.dae` | Low, 301 Dreiecke |
| `Schild_LOD0.dae` | Lowest, 30 Dreiecke |
| `Schild_PHYS.dae` | Physik, Quader 12 Dreiecke |
| `Texturen/Schild_Farbe.png` | Farbtextur mit eingebackenem AO (1024 × 1024) |
| `Texturen/Schild_Normal.png` | Normal Map, OpenGL, Alpha = Glanzgrad |
| `Texturen/Schild_Glanz.png` | Specular Map, RGB = Glanzfarbe, Alpha = Umgebungsreflexion |
| `Texturen/PBR_optional/` | BaseColor, Normal, ORM für PBR-Materialien (nur bei Bedarf) |
| `Blender/Schild.blend` | Arbeitsdatei mit High, LODs, Physik und Material, Texturen relativ verknüpft |

Alle LODs haben exakt die Bounding Box des High. Fehlende Extrempunkte sind mit je zwei winzigen Anker-Dreiecken (0,5 mm) gesichert, nichts ist gestreckt.

## Upload im Mesh-Uploader

1. Datei `Schild.dae` als Modell wählen.
2. Reiter *Level of Detail*
   - High ist `Schild.dae`
   - Medium „Load from file“ `Schild_LOD2.dae`
   - Low „Load from file“ `Schild_LOD1.dae`
   - Lowest „Load from file“ `Schild_LOD0.dae`
3. Reiter *Physics* „From file“ `Schild_PHYS.dae`. Analyze ist nicht nötig.
4. Reiter *Upload options* Scale 1, „Include textures“ an. Damit kommt `Schild_Farbe.png` mit.
5. „Calculate weights & fee“, Werte notieren (Download, Physik, Server), dann hochladen.

## Nach dem Rezzen

| Fläche | Textur | Bumpiness (normal) | Shininess (specular) |
|---|---|---|---|
| einzige Fläche (Material `Schild_Material`) | `Schild_Farbe.png` | `Schild_Normal.png` | `Schild_Glanz.png` |

- Repeats 1, Offset 0, Rotation 0 für alle drei Karten. Alpha mode „None“.
- Physics Shape Type „Convex Hull“ lassen.
- Startwerte für Glanz Glossiness 51, Environment 0, Farbe weiß. Laut SL-Wiki liest der Viewer den Glanzgrad aus dem Alphakanal der Normal Map und die Umgebungsreflexion aus dem Alphakanal der Specular Map. Im Viewer nicht geprüft. Normal und Glanz zuerst über „Local“ im Texturwähler kostenlos testen, erst dann hochladen.
- Pflicht-Uploads 3 Texturen (Farbe kommt mit dem Mesh, Normal und Glanz einzeln). Die PBR-Karten nur hochladen, wenn das Objekt ein PBR-Material bekommen soll.

## LI-Schätzung

Eigener Schätzer (Verfahren der Mesh-Anleitung, Kalibrierung 0,706 aus Jarlswoman v8). Radius 0.6033 m.

| Stufe | Dreiecke | komprimierte Bytes (geschätzt) |
|---|---|---|
| High | 3482 | 37220 |
| Medium | 1002 | 13734 |
| Low | 301 | 4838 |
| Lowest | 30 | 329 |

Download-Gewicht roh 1.085, im Uploader erwartet etwa **0.766**. Server-Gewicht mindestens 0,5, Physik als Quader klein. Erwarteter LI damit etwa **1**. Nicht im Viewer gemessen, bitte den Uploader-Wert in die STAND.md eintragen und neu eichen.

Lowest nach dem Farbpunkt-Verfahren. Statt eines einzigen UV-Punkts liegt jede Farbgruppe auf einer unverzerrten UV-Fläche von 2 Pixeln an einer Stelle mit flacher Normal Map. Ein Einzelpunkt macht die Tangentenbasis entartet und rendert mit Normal Map schwarz (im Blender-Test so aufgetreten).
Farbgruppen RGB (59, 36, 27) (91 % der Fläche), RGB (104, 104, 104) (9 % der Fläche). Nach jeder Änderung der Farbtextur neu bestimmen.

## Was am Original geändert wurde

Gleichmäßig auf 0,85 m Durchmesser skaliert (Original 2,60 m, unrealistisch), um 180° um Z gedreht, damit der Buckel nach −Y zeigt. Form unverändert.

Texturen von 2048 auf 1024 × 1024 verkleinert (Normal Map als Vektor gemittelt und renormiert). Normal-Map-Konvention Der Unity-Satz ist OpenGL und wurde verwendet. Der Satz „PBR metallic roughnes“ ist DirectX (Grünkanal umgekehrt) und wurde bewusst nicht genommen. AO aus dem Rotkanal der UnrealEngine4-ORM-Karte des Originals.

LODs aus dem Schild ohne die 55 Nieten (unter 3 cm), mit Blenders Decimate (Collapse), das Lowest als flaches Achteck von Hand gebaut. LOD-Punkte, die bei der Reduktion um wenige Millimeter über die High-Box hinausrutschten, wurden auf die Box geklemmt.

## Schwächste Stelle

Das Low (301 Dreiecke, ab etwa 10 m) zeigt den Buckel leicht fleckig, Nieten sind ab Medium nur noch in der Normal Map. Das Lowest ist ein flaches Achteck in Holzbraun mit Metallrand.

## Quelle und Lizenz

- Archiv im Repository `scandinavian battle shield.zip (11 Teile)`
- verwendete Dateien `BLEND/Viking shield.blend, Texturen textures/original/Unity5/…(Metallic Standard)/2048x2048 und UnrealEngine4/2048x2048 (nur AO)`
- Blender 2.92, Substance-Export in vier Varianten. Mitgeliefertes Referenzbild textures/original/shield_free_1.jpg. Keine Lizenzdatei, kein Autorenname im Archiv.
- Websuche ergab auf CGTrader ein kostenloses Modell „Scandinavian Battle Shield“ (cgtrader.com/free-3d-models/military/armor/scandinavian-battle-shield). Laut Suchergebnis Lizenz „Royalty Free, No AI“, Texturen 512 bis 4096 px als PNG, rund 1.785 Polygone. Das passt zum Archiv, die Seite selbst war aus der Arbeitsumgebung aber nicht abrufbar. Lizenz damit **nicht am Original geprüft**.

**Vor einem Verkauf in SL** die Lizenz an der Originalseite prüfen und den Nachweis (Screenshot der Lizenz, Kaufbeleg oder Download-Bestätigung) ablegen. Ohne belegte Lizenz nur zum eigenen Gebrauch verwenden.
