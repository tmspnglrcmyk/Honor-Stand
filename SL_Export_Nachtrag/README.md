# Honor Stand · Nachtrag

Testexporte aus den nachgereichten Quellen. Der bisherige Export unter `SL_Export/` bleibt unverändert.

| Ordner | Inhalt | Download geschätzt |
|---|---|---|
| `Schild/` | Schild aus `Shield.blend` (Rabenschild), 0,85 m | 0,80 |
| `viking-chest/` | Wikingerkiste, 0,90 × 0,41 × 0,53 m | 0,27 |
| `Vorschau.png` | gemeinsame Vorschau, dazu der neue Speer im Vergleich | |

Aus dem neuen Speer wurde kein Testexport erstellt, Begründung unten.

## Zusammensetzen

Die Ordner `spear/`, `shield/` und `viking-chest/` aus der Nachtrags-README gibt es im Repository nicht, alle Teile liegen im Hauptordner. Zusammengesetzt wurde dort, bytegenau `.part001` dann `.part002`, jedes Archiv mit `unzip -t` geprüft. Alle vier sind fehlerfrei, ebenso das innere `source/model.zip` der Kiste.

## Herkunft und Lizenz

Keines der drei Modelle bringt einen Lizenznachweis mit, die Nachtrags-README sagt das selbst. Spuren in den Dateien
- `Shield.blend` mit Blender 4.4 gespeichert, Projektpfad `E:\ProjectBlend\Shield`, Windows-Benutzer „romas“. Keine Autoren- oder Lizenzfelder in den Asset-Daten.
- `spear-nachtrag-modell.fbx` mit Blender 4.2.3 LTS exportiert, Texturen vom 14.3.2025. Keine Angaben.
- `viking-chest.zip` mit Sketchfab-typischem Aufbau (`source/model.zip` und `textures/`), Assimp-Export vom 6.12.2019, Teilenamen französisch (BOIS, METAL, ANNEAU, COIN, HAUT). Keine Angaben.

Eine Websuche fand keine der Originalseiten. **Alle drei sind damit für einen Verkauf in SL nicht freigegeben**, bis die Quelle gefunden und die Lizenz belegt ist.

## Vergleich je Objekt

**Schild · neue Quelle besser geeignet.** 2.084 statt 3.482 Dreiecke, ein Material, echter Griff mit Halterungen auf der Rückseite, gemaltes Rabenmotiv. Native Blender-Datei mit sauberen Teilen, deshalb ergeben die LODs ohne Sonderbehandlung saubere Stufen (beim bisherigen Schild mussten 55 Nieten entfernt werden). Normal Map OpenGL. Die Texturen sind in `Shield.blend` eingepackt und byte-identisch mit dem Texturarchiv, sie werden also immer gefunden. Für den Export wurden sie aus dem Archiv neu verknüpft. Download-Gewicht praktisch gleich (0,80 gegen 0,77). Schwächste Stelle ist die UV-Ausnutzung von nur 27 %, bei 1024 px wirkt die Holzmaserung aus der Nähe weicher als beim bisherigen Schild. Das Rabenmotiv ist eine Gestaltungsentscheidung, der bisherige Schild ist unbemalt.

**Speer · neue Quelle nicht besser geeignet.** Es ist ein kurzer Wurfspeer, 1,44 m lang mit nur 1,3 cm Schaft, verwittertes Naturholz, schmale Spitze mit Lederwicklung. Er sieht historischer aus als der rote Schaft der bisherigen Quelle. Dagegen sprechen drei Materialien (9 statt 3 Textur-Uploads), Normal Maps in DirectX-Konvention (Grünkanal müsste gedreht werden) und eine Wicklung, die mit 11.688 von 12.956 Dreiecken fast das ganze Modell ausmacht. Auf 2,2 m skaliert wäre der Schaft 2 cm dick, schlanker als jeder andere Teil des Stands. Ein Testexport lohnt sich nur, wenn der Naturholz-Look gewünscht ist.

**Kiste · geeignet.** Low-Poly (1.956 Dreiecke), vollständige PBR-Texturen, Normal Maps OpenGL. Die Materialzuordnung war beim Assimp-Export verloren gegangen und wurde rekonstruiert (siehe `viking-chest/ANLEITUNG.md`). Die Einheit im DAE war falsch (Kiste 2 cm groß), sie wurde auf 0,90 m Breite skaliert.
