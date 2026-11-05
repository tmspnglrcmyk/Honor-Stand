# Schild (Nachtrag) · Upload-Anleitung Second Life

Rabenschild aus `Shield.blend`, statisches Dekoobjekt. Maße 0,850 × 0,136 × 0,850 m, Buckel und Bemalung zeigen nach −Y.

## Dateien

| Datei | Zweck |
|---|---|
| `Schild.dae` | High, 2.084 Dreiecke (Originalgeometrie, alle acht Teile vereint) |
| `Schild_LOD2.dae` | Medium, 1.000 Dreiecke (Blender Decimate) |
| `Schild_LOD1.dae` | Low, 302 Dreiecke |
| `Schild_LOD0.dae` | Lowest, 30 Dreiecke, flaches Achteck, vorn Rot, hinten Holz |
| `Schild_PHYS.dae` | Physik, Quader |
| `Texturen/Schild_Farbe.png` | Farbe mit eingebackenem AO (1024) |
| `Texturen/Schild_Normal.png` | Normal Map OpenGL, Alpha = Glanzgrad |
| `Texturen/Schild_Glanz.png` | Specular Map, Alpha = Umgebungsreflexion |
| `Texturen/PBR_optional/` | BaseColor, Normal, ORM |
| `Blender/Schild.blend` | Arbeitsdatei |

## Upload

Wie beim bisherigen Schild in `SL_Export/Schild/ANLEITUNG.md`. High `Schild.dae`, Medium `_LOD2`, Low `_LOD1`, Lowest `_LOD0`, Physik `_PHYS`, „Include textures“ an. Nach dem Rezzen Normal und Glanz zuweisen, Repeats 1, Alpha mode None. Pflicht-Uploads 3 Texturen.

## LI-Schätzung

| Stufe | Dreiecke | Bytes geschätzt |
|---|---|---|
| High | 2.084 | 23.199 |
| Medium | 1.000 | 15.429 |
| Low | 302 | 5.263 |
| Lowest | 30 | 335 |

Download im Uploader erwartet etwa 0,80, LI erwartet 1. Nicht im Viewer gemessen.

## Was geändert wurde

Die acht Teile wurden mit ihrem Modifier „Smooth by Angle“ angewendet und zu einem Objekt vereint. Der Schild ist gleichmäßig von 1,12 m auf 0,85 m skaliert, damit er zum bisherigen Export passt, und auf die Mitte zentriert. Die Texturen kommen aus `shield-nachtrag-texturen.zip` (4096 px auf 1024 verkleinert). Sie sind identisch mit den in `Shield.blend` eingepackten Bildern. Es gibt keine AO-Karte im Original, die Selbstverschattung wurde in Cycles gebacken (8 cm).

## Schwächste Stelle

Die Textur nutzt nur 27 % der Fläche. Aus nächster Nähe wirkt die Bemalung bei 1024 px weicher als im Original mit 4096 px.

## Quelle und Lizenz

`shield-nachtrag-blender.zip` und `shield-nachtrag-texturen.zip` (je 2 Teile). Blender 4.4, Pfad `E:\ProjectBlend\Shield`, keine Autoren- oder Lizenzangaben, Herkunft **unbelegt**. Vor einem Verkauf Quelle und Lizenz klären.
