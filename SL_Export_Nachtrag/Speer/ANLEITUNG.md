# Speer (Nachtrag) · Upload-Anleitung Second Life · Fassung 2,20 m

Wurfspeer aus `spear-nachtrag-modell.fbx` mit Stahlspitze, Lederwicklung und verwittertem Holzschaft. Statisches Dekoobjekt, **2,20 m lang** (0,053 × 0,030 × 2,200 m), Spitze nach +Z. Gleichmäßig um den Faktor 1,528 aus der Originalgröße 1,44 m vergrößert, die Form ist dabei unverändert. Der Schaft ist jetzt 2,0 cm dick, die Spitze 5,3 cm breit.

**Bitte in SL nicht weiter skalieren.** LODs und Physik sind für genau diese Größe gebaut. Jede Vergrößerung in SL erhöht den LI.

## Dateien

| Datei | Zweck |
|---|---|
| `Speer.dae` | High, 12.956 Dreiecke (Originalgeometrie, unverändert bis auf die Größe) |
| `Speer_LOD2.dae` | Medium, 618 Dreiecke. Schaft und Spitze mit Blender reduziert, die Wicklung als achtseitige Lederhülse |
| `Speer_LOD1.dae` | Low, 92 Dreiecke, Wicklung als sechsseitige Hülse |
| `Speer_LOD0.dae` | Lowest, 8 Dreiecke, von Hand gebaut, trifft die Box ohne Anker |
| `Speer_PHYS.dae` | Physik, Quader 0,053 × 0,030 × 2,20 m |
| `Texturen/Speer_Farbe.png` | Farbe mit AO (1024, Atlas aus Holz, Stahl, Leder) |
| `Texturen/Speer_Normal.png` | Normal Map OpenGL, Alpha = Glanzgrad |
| `Texturen/Speer_Glanz.png` | Specular Map, Alpha = Umgebungsreflexion |
| `Texturen/PBR_optional/` | BaseColor, Normal, ORM |
| `Blender/Speer.blend` | Arbeitsdatei mit High, LODs, Physik und Material |
| `Vorschau_Speer.png` | alle Stufen und Nahansicht der Spitze |

Die Texturen sind dieselben wie in der 1,44-m-Fassung. Wer sie dort schon hochgeladen hat, kann sie weiterverwenden.

## Upload im Mesh-Uploader

1. `Speer.dae` als Modell wählen.
2. *Level of Detail* Medium „Load from file“ `Speer_LOD2.dae`, Low `Speer_LOD1.dae`, Lowest `Speer_LOD0.dae`.
3. *Physics* „From file“ `Speer_PHYS.dae`, Analyze ist nicht nötig.
4. *Upload options* Scale 1, „Include textures“ an.
5. „Calculate weights & fee“. Bitte Download-, Physik- und Server-Gewicht notieren und mir melden.

Nach dem Rezzen gilt: `Speer_Normal.png` als Bumpiness (normal), `Speer_Glanz.png` als Shininess (specular), Repeats 1, Alpha mode None, Physics Shape Type „Convex Hull“.

## LI · Schätzung, nicht in SL geprüft

Schätzer mit Kopfaufschlag je Fläche, kalibriert auf die Messung am Helm (Uploader 1,9). Radius 1,10 m, Umschaltabstände etwa 4,6 m, 18 m und 37 m.

| Stufe | Dreiecke | Bytes geschätzt | Anteil geschätzt |
|---|---|---|---|
| High | 12.956 | 142.003 | 0,24 |
| Medium | 618 | 8.860 | 0,22 |
| Low | 92 | 2.085 | 0,16 |
| Lowest | 8 | 261 | 0,34 |

**Geschätzter Download im Uploader etwa 0,96, geschätzter LI 1.** Zum Vergleich: Die 1,44-m-Fassung, in SL auf 2,20 m vergrößert, kommt nach demselben Schätzer auf etwa 1,74, also 2 LI. Der Abstand zur Rundungsgrenze 1,5 beträgt etwa 0,5. Die Kalibrierung beruht auf einer einzigen Messung, deshalb ist der Wert bis zur Prüfung in SL eine Schätzung.

## Was sich gegenüber der 1,44-m-Fassung geändert hat

- **Größe** Gleichmäßig auf 2,20 m skaliert, die Physik-Box mit.
- **Medium** Bei 2,20 m gilt das Medium von 4,6 bis 18 m und kostete mit 1.502 Dreiecken allein etwa 0,68. Jetzt hat es 618 Dreiecke. Die Spitze bleibt rund, die Wicklung wird zu einer glatten Lederhülse.
- **Low** 92 statt 154 Dreiecke.
- **Lowest** 8 statt 12 Dreiecke, sechs Punkte, alle Extreme auf der Box.
- **Farbe der Hülse** RGB [93, 84, 73]. Das ist das Mittel der sichtbaren Lederfläche, ohne die verdeckten Unterseiten der Lederstreifen (AO nahe null). An einer Stelle mit ruhiger Umgebung abgegriffen, als unverzerrte 2-Pixel-UV-Fläche.

## Schwächste Stelle

Ab 4,6 m ist die Wicklung eine glatte Hülse, die Rillen der Lederstreifen sind dort nur noch in der High-Stufe zu sehen. Das Lowest (ab 37 m) ist ein brauner Stab mit dunkler Spitze. Die Texturauflösung ist gegenüber 1,44 m auf etwa zwei Drittel je Meter gesunken, aus nächster Nähe wirkt die Holzmaserung etwas weicher.

## Quelle und Lizenz

`spear-nachtrag-modell.fbx` und `spear-nachtrag-texturen-2k.zip` (2 Teile). FBX mit Blender 4.2.3 LTS exportiert, Texturen vom 14.3.2025. Keine Lizenzdatei, kein Autor, Herkunft **unbelegt**. Vor einem Verkauf Quelle und Lizenz klären.
