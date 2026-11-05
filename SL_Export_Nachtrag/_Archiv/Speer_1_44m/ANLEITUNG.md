# Speer (Nachtrag) · Upload-Anleitung Second Life

Wurfspeer aus `spear-nachtrag-modell.fbx` mit Stahlspitze, Lederwicklung und verwittertem Holzschaft. Statisches Dekoobjekt, Originalgröße 1,44 m (0,035 × 0,019 × 1,440 m), Spitze nach +Z.

## Dateien

| Datei | Zweck |
|---|---|
| `Speer.dae` | High, 12.956 Dreiecke (Originalgeometrie, drei Teile vereint) |
| `Speer_LOD2.dae` | Medium, 1.502 Dreiecke (Blender Decimate) |
| `Speer_LOD1.dae` | Low, 154 Dreiecke, Wicklung als sechsseitige Hülle in Lederfarbe |
| `Speer_LOD0.dae` | Lowest, 12 Dreiecke, von Hand, trifft die Box ohne Anker |
| `Speer_PHYS.dae` | Physik, Quader |
| `Texturen/Speer_Farbe.png` | Farbe mit AO (1024, Atlas aus Holz, Stahl, Leder) |
| `Texturen/Speer_Normal.png` | Normal Map OpenGL, Alpha = Glanzgrad |
| `Texturen/Speer_Glanz.png` | Specular Map, Alpha = Umgebungsreflexion |
| `Texturen/PBR_optional/` | BaseColor, Normal, ORM |
| `Blender/Speer.blend` | Arbeitsdatei |

## Upload

High `Speer.dae`, Medium `Speer_LOD2.dae`, Low `Speer_LOD1.dae`, Lowest `Speer_LOD0.dae`, Physik `Speer_PHYS.dae` „From file“, Scale 1, „Include textures“ an. Nach dem Rezzen Normal und Glanz zuweisen, Repeats 1, Alpha mode None, Physics Shape Type „Convex Hull“. Pflicht-Uploads 3 Texturen.

## Ein Material statt drei

Das Original hat drei Materialien mit je drei 2048er-Karten (9 Uploads, drei Flächen mit Kopfdaten in jeder LOD-Stufe). Alle drei liegen jetzt auf einem Atlas. Die Atlas-UV entstand aus den Original-UVs nur durch Verschieben und gleichmäßiges Skalieren der Inseln, ohne Drehung und ohne Spiegelung (geprüft, höchstens 0,02°). Deshalb ließen sich die Normal Maps direkt umbacken. Die Spitze hat doppelte Texeldichte gegenüber Schaft und Wicklung. Die Original-Normal-Maps sind DirectX, der Grünkanal wurde für SL auf OpenGL gedreht.

## LI-Schätzung

Schätzer mit Kopfaufschlag je Fläche, kalibriert auf die Messung am Helm (1,9). Radius 0,72 m, Umschaltabstände etwa 3 m, 12 m, 24 m.

| Stufe | Dreiecke | Bytes geschätzt |
|---|---|---|
| High | 12.956 | 142.023 |
| Medium | 1.502 | 26.740 |
| Low | 154 | 3.060 |
| Lowest | 12 | 353 |

Download im Uploader erwartet etwa **1,08**, LI erwartet **1**. Wird der Speer in SL vergrößert, steigt der LI. Auf 2,2 m skaliert wären es geschätzt etwa 1,6, also 2 LI. Für 2,2 m bitte vorher Bescheid geben, dann baue ich die LODs für diese Größe.

## Schwächste Stelle

Das Lowest ist ein dünner brauner Stab mit Spitze. Die Spitze bekommt dort keinen eigenen Stahlton, aber ab 24 m Abstand ist sie nur ein bis zwei Pixel breit. Die Atlas-Textur hat für die Wicklung weniger Auflösung als das 2048er-Original.

## Quelle und Lizenz

`spear-nachtrag-modell.fbx` und `spear-nachtrag-texturen-2k.zip` (2 Teile). FBX mit Blender 4.2.3 LTS exportiert, Texturen vom 14.3.2025. Keine Lizenzdatei, kein Autor, Herkunft **unbelegt**. Vor einem Verkauf Quelle und Lizenz klären.
