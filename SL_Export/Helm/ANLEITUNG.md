# Helm · Upload-Anleitung Second Life (Fassung 2)

Fassung 2 senkt den LI. Der erste Upload zeigte 1,9 im Uploader und 2 LI in der Welt. Geändert sind nur die Mesh-Dateien, die Texturen sind byte-gleich zu Fassung 1 und müssen nicht neu hochgeladen werden.

Wikingerhelm mit Brillenvisier und Kettenbehang, statisches Dekoobjekt für den 1st Axe Honor Stand. Maße 0,234 × 0,323 × 0,324 m (X × Y × Z), Visier zeigt nach −Y, Kettenbehang nach +Y.

## Dateien

| Datei | Zweck |
|---|---|
| `Helm.dae` | High, 173.917 Dreiecke (Originalgeometrie mit echten Kettenringen, Originalnormalen) |
| `Helm_LOD2.dae` | Medium, 9.970 Dreiecke, Kettenbehang als Alpha-Vorhang |
| `Helm_LOD1.dae` | Low, 2.314 Dreiecke (jetzt mit Blender reduziert, ohne Risse) |
| `Helm_LOD0.dae` | Lowest, 12 Dreiecke, eine einzige Fläche (Glocke), Silhouette aus Kuppel, Visier und Behang |
| `Helm_PHYS.dae` | Physik, Quader 12 Dreiecke |
| `Texturen/Helm_<Fläche>_Farbe.png` | Farbtextur mit eingebackenem AO, beim Vorhang mit Alpha |
| `Texturen/Helm_<Fläche>_Normal.png` | Normal Map, OpenGL, Alpha = Glanzgrad |
| `Texturen/Helm_<Fläche>_Glanz.png` | Specular Map, RGB = Glanzfarbe, Alpha = Umgebungsreflexion |
| `Texturen/PBR_optional/` | BaseColor, Normal, ORM je Fläche |
| `Blender/Helm.blend` | Arbeitsdatei mit High, LODs, Physik und Materialien, Texturen relativ verknüpft |

## Materialflächen

| Nr. | Material | High | Medium | Low | Lowest | Textur |
|---|---|---|---|---|---|---|
| 1 | Helm_Glocke | 58.368 | 4.002 | 1.202 | 12 | 1024 |
| 2 | Helm_Visier | 52.784 | 4.000 | 1.000 | – | 1024 |
| 3 | Helm_Ringe | 57.308 | – | – | – | 1024 |
| 4 | Helm_Futter | 5.456 | 400 | – | – | 512 |
| 5 | Helm_Vorhang | 1 (verdeckt) | 1.568 | 112 | – | 512, Alpha |

Die echten Kettenringe (Fläche 3) gibt es nur im High, das bis etwa 1,1 m Abstand gilt. Ab Medium trägt ein doppelseitiger Vorhang (Fläche 5) die Ringe als Alpha-Maske. Farbe, Deckung und Normalen sind von den Originalringen gebacken, Ringgröße und Muster bleiben gleich. Weil jede LOD-Stufe nur Materialien des High verwenden darf, enthält das High ein verdecktes Dreieck von 0,5 mm mit dem Vorhangmaterial (in der Glocke über dem Futter). Das Lowest besteht nur aus der Glockenfläche in Stahlgrau. Jede weitere Fläche kostet dort Kopfdaten, die bei diesem kleinen Objekt teuer sind.

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

## LI

**Messung Fassung 1** Uploader 1,9, in der Welt 2 LI.

**Ursache** Mein Schätzer zählte nur die Geometrie, nicht die Kopfdaten, die SL für jede Materialfläche einer LOD-Stufe speichert. Bei einem 32-cm-Objekt fällt fast die ganze Sichtfläche auf das Lowest, dort kostet jedes Byte etwa 0,0026 LI. Fassung 1 hatte im Lowest zwei Flächen. Kalibriert auf die Messung sind es rund 75 Byte je Fläche und 20 je leerer Fläche. Mit diesem Aufschlag trifft der Schätzer Fassung 1 mit 1,92.

**Fassung 2**

| Stufe | Dreiecke | Bytes geschätzt | Anteil im Uploader |
|---|---|---|---|
| High | 173.917 | 1.682.670 | 0,16 |
| Medium | 9.970 | 133.077 | 0,19 |
| Low | 2.314 | 39.198 | 0,17 |
| Lowest | 12 | 312 | 0,49 |

Download im Uploader erwartet etwa **1,0**, LI in der Welt erwartet **1**. Abstand zur Rundungsgrenze 1,5 etwa 0,5. Bitte den neuen Uploader-Wert melden, dann eiche ich weiter.

Physics Shape Type in der Welt auf „Convex Hull“ lassen. Zeigt die Welt trotzdem 2, im Bearbeiten-Fenster „More info“ die drei Gewichte ansehen. Ist das Physikgewicht der Treiber, liegt es am Physikmodell, nicht an der Grafik.

## Was am Original geändert wurde

- Einheiten von Zentimeter auf Meter, Y-oben auf Z-oben, auf die Mitte der Bounding Box zentriert. Form und Größe unverändert.
- Unverschweißte Assimp-Geometrie verschweißt (keine sichtbare Änderung). Beim Visier entfielen dabei 448 entartete Dreiecke ohne Fläche.
- Texturen von 2048 auf 1024 (Futter 512), Normal Maps als Vektor gemittelt. Alle vier Normal Maps sind OpenGL (Prüfung über die Divergenz der Kanäle, an Axt und Schild gegengeprüft).
- AO aus den Originalkarten in die Farbtextur eingerechnet.
- Medium mit MeshLab (Quadric Edge Collapse mit Texturerhalt), Low mit Blender Decimate. Lowest von Hand, neun Punkte genau auf der High-Box (keine Anker nötig), Farbe als 2-Pixel-UV-Fläche (Stahl der Außenseite). LOD-Punkte bis 3,3 mm auf die High-Box geklemmt, Bounding Box aller Stufen identisch.

## Schwächste Stelle

Das Lowest ist eine grobe stahlgraue Spitzform ohne Bronzebänder. Es gilt ab 8,6 m, bei Firestorm mit LOD-Faktor 2 erst ab etwa 17 m, dort ist der Helm nur wenige Pixel groß. Das Low aus Fassung 1 hatte Risse am Visier, in Fassung 2 sind sie durch die Blender-Reduktion verschwunden.

## Quelle und Lizenz

- Archiv im Repository `viking-helmet-free-download.zip` (4 Teile)
- verwendete Dateien `source/model.zip` → `model/model.dae` (Assimp-Export vom 8.6.2023) und `textures/*` (Helmet_42, Face_guard, Mail, Liner)
- Keine Lizenzdatei, kein Autorenname, keine URL im Archiv. Ordneraufbau `source/` und `textures/` und der Name „free-download“ sprechen für einen Sketchfab-Download. Eine Websuche fand das Modell nicht. Herkunft und Lizenz **unbelegt**.

**Vor einem Verkauf in SL** die Originalseite finden, Lizenz prüfen und den Nachweis ablegen. Viele kostenlose Sketchfab-Modelle stehen unter CC BY, dann ist eine Namensnennung in der Produktbeschreibung Pflicht. Das ist hier nicht geprüft.
