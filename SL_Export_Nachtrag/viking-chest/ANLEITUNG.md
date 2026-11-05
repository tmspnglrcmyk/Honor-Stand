# Kiste · Upload-Anleitung Second Life

Wikingerkiste mit schrägen Beinen, Beschlägen und Ringgriffen, statisches Dekoobjekt. Maße 0,900 × 0,407 × 0,531 m.

## Verwendete Texturen

Das DAE (`source/model.zip` → `model/model.dae`) enthält **keine** Texturverweise, und alle 22 Teile tragen das Platzhaltermaterial `defaultMaterial`. Die Zuordnung wurde rekonstruiert. Für jedes Teil wurde aus der Kistengeometrie eine AO-Karte gebacken und innerhalb seiner UV-Inseln mit den drei Original-AO-Karten korreliert. Das Ergebnis ist eindeutig, die Werte liegen bei 0,57 bis 0,90, die anderen Sätze nahe null.

| Material in SL | Originalsatz | Teile | Textur |
|---|---|---|---|
| Kiste_Holz | BOIS | BASE, HAUT (Korpus, Deckel) | 1024 |
| Kiste_Metall | METAL | ANNEAU, ANNEAU1, COIN, COIN1, COIN2, DECO, DECO2 | 1024 |
| Kiste_Nieten | ANNEAU2 | AN1 bis AN4, pasted__AN1, POIN bis POIN7 | 512 |

Quelle der Bilder ist `model/textures/` im inneren Archiv. Der äußere Ordner `textures/` ist pixelgleich (geprüft), ihm fehlt nur `METAL_metallic`. Die Metallic-Karten von BOIS und METAL sind überall null, METAL wirkt also als nicht-metallisch, wie im Original. Genutzt wurden albedo, AO, roughness, metallic und normal (OpenGL).

## Dateien

| Datei | Zweck |
|---|---|
| `Kiste.dae` | High, 1.956 Dreiecke (Holz 264, Metall 648, Nieten 1.044) |
| `Kiste_LOD2.dae` | Medium, 1.066 Dreiecke |
| `Kiste_LOD1.dae` | Low, 322 Dreiecke, ohne Nieten |
| `Kiste_LOD0.dae` | Lowest, 12 Dreiecke, Quader in Holzfarbe |
| `Kiste_PHYS.dae` | Physik, Quader |
| `Texturen/Kiste_<Material>_Farbe/Normal/Glanz.png` | Legacy-Texturen, AO in der Farbe |
| `Texturen/PBR_optional/` | BaseColor, Normal, ORM |
| `Blender/Kiste.blend` | Arbeitsdatei |

## Upload

High `Kiste.dae`, Medium `Kiste_LOD2.dae`, Low `Kiste_LOD1.dae`, Lowest `Kiste_LOD0.dae`, Physik `Kiste_PHYS.dae`, „Include textures“ an. Danach je Fläche Normal und Glanz zuweisen, Repeats 1, Alpha mode None. Pflicht-Uploads 6 Texturen (je Fläche Normal und Glanz).

## LI-Schätzung

| Stufe | Dreiecke | Bytes geschätzt | Anteil im Uploader |
|---|---|---|---|
| High | 1.956 | 22.629 | 0,01 |
| Medium | 1.066 | 15.821 | 0,10 |
| Low | 322 | 5.423 | 0,11 |
| Lowest | 12 | 141 | 0,04 |

Download erwartet etwa 0,27. Bestimmend ist dann das Server-Gewicht von 0,5, LI erwartet 1. Wer die Kiste begehbar oder als Sitz nutzen will, sollte die Physik prüfen, der Quader schließt die Beine mit ein.

## Was geändert wurde

Die Einheit im DAE war falsch, die Kiste wäre 2 cm groß. Sie wurde gleichmäßig auf 0,90 m Breite skaliert (Vorbild Mästermyr-Truhe, 0,88 m), von Y-oben auf Z-oben gedreht und zentriert. Die Form ist unverändert.

## Schwächste Stelle

Das Lowest ist ein schlichter Quader ohne Beine. Er gilt erst ab etwa 18,7 m. Die Maßstabsannahme 0,90 m ist geschätzt, nicht belegt.

## Quelle und Lizenz

`viking-chest.zip` (2 Teile), innen `source/model.zip`. Sketchfab-typischer Aufbau, Assimp-Export vom 6.12.2019, französische Teilenamen. Keine Lizenzdatei, kein Autor, Herkunft **unbelegt**. Vor einem Verkauf Quelle und Lizenz klären, bei CC BY ist die Namensnennung Pflicht.
