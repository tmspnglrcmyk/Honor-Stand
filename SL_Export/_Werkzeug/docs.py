# schreibt ANLEITUNG.md je Objekt aus den Berichtsdaten
import json, os, sys
WK, OUT = sys.argv[1:3]

quelle = {
 'Axt': dict(archiv='battle ax with runes.zip (2 Teile)', datei='axe2zip/axe2.fbx, Texturen axe2zip/2k/axe2_lp_axeLP_*.png',
             meta='FBX aus Blender 3.5.1 exportiert, Texturen im Substance-Namensschema. Keine Lizenzdatei, kein Autorenname, keine Herkunfts-URL im Archiv.',
             spur='Websuche ergab einen möglichen Treffer „model of a viking battle ax with runes“ auf CGTrader (cgtrader.com/3d-models/military/melee/model-of-a-viking-battle-ax-with-runes). Die Seite war aus der Arbeitsumgebung nicht abrufbar, Übereinstimmung und Lizenz sind deshalb **nicht belegt**.',
             normal='OpenGL (Prüfung über eine Rinne in der Mittelrippe, Grünkanal), unverändert übernommen.',
             ao='Kein AO im Original. Selbstverschattung in Cycles gebacken (1024 px, 256 Samples, Distanz 8 cm), weich eingerechnet (25 % Mindesthelligkeit).'),
 'Schild': dict(archiv='scandinavian battle shield.zip (11 Teile)', datei='BLEND/Viking shield.blend, Texturen textures/original/Unity5/…(Metallic Standard)/2048x2048 und UnrealEngine4/2048x2048 (nur AO)',
             meta='Blender 2.92, Substance-Export in vier Varianten. Mitgeliefertes Referenzbild textures/original/shield_free_1.jpg. Keine Lizenzdatei, kein Autorenname im Archiv.',
             spur='Websuche ergab auf CGTrader ein kostenloses Modell „Scandinavian Battle Shield“ (cgtrader.com/free-3d-models/military/armor/scandinavian-battle-shield). Laut Suchergebnis Lizenz „Royalty Free, No AI“, Texturen 512 bis 4096 px als PNG, rund 1.785 Polygone. Das passt zum Archiv, die Seite selbst war aus der Arbeitsumgebung aber nicht abrufbar. Lizenz damit **nicht am Original geprüft**.',
             normal='Der Unity-Satz ist OpenGL und wurde verwendet. Der Satz „PBR metallic roughnes“ ist DirectX (Grünkanal umgekehrt) und wurde bewusst nicht genommen.',
             ao='AO aus dem Rotkanal der UnrealEngine4-ORM-Karte des Originals.'),
 'Speer': dict(archiv='weapon spear s1.zip', datei='970_SpearS1/63_SpearS1.fbx (Objekt Box.014), Texturen 63_SpearS1M_*.png',
             meta='FBX aus Blender 4.3.2, Quellpfad im FBX deutet auf eine Asset-Sammlung („_1K_Asset_Work“). Die Datei enthält den Speer doppelt (Box.014 und Box.015 sind identisch), verwendet wurde einer. Keine Lizenzdatei, kein Autorenname, keine URL.',
             spur='Websuche nach „Spear S1“ und der Nummer 970 ergab keinen Treffer. Herkunft **unbekannt**.',
             normal='Die mitgelieferte Datei 63_SpearS1M_Normal_OpenGL.png wurde verwendet.',
             ao='AO aus 63_SpearS1M_Mixed_AO.png des Originals.'),
}
anpassung = {
 'Axt': 'Keine Änderung an Maß oder Ausrichtung. Länge 27 cm wie im Original (eher Beil als Streitaxt). Stiel liegt entlang X, Klinge zeigt nach unten.',
 'Schild': 'Gleichmäßig auf 0,85 m Durchmesser skaliert (Original 2,60 m, unrealistisch), um 180° um Z gedreht, damit der Buckel nach −Y zeigt. Form unverändert.',
 'Speer': 'Gleichmäßig auf 2,20 m Länge skaliert (Original 4,71 m bei 7,5 cm Schaftdicke, ergibt jetzt 3,5 cm), aufrecht gestellt, Spitze nach +Z. Die Originaltextur nutzt nur einen Streifen von 10,7 % der Breite. Dieser Streifen wurde ausgeschnitten und die UVs nur in U gestreckt, daher die Textur 256 × 1024 statt 1024 × 1024. Keine neuen Nähte, volle Breitenauflösung.',
}
schwach = {
 'Axt': 'Das Lowest (18 Dreiecke) zeigt die Klinge nur noch als schmalen Keil. Es greift ab etwa 4,9 m Abstand. Mehr Dreiecke dort kosten fast 1:1 LI, weil bei kleinen Objekten nahezu die gesamte Sichtfläche auf das Lowest entfällt. Wird die Axt in SL vergrößert, steigt der LI.',
 'Schild': 'Das Low (301 Dreiecke, ab etwa 10 m) zeigt den Buckel leicht fleckig, Nieten sind ab Medium nur noch in der Normal Map. Das Lowest ist ein flaches Achteck in Holzbraun mit Metallrand.',
 'Speer': 'Das High behält alle 12.506 Dreiecke des Originals und macht damit gut ein Drittel des Download-Gewichts aus. Ein reduziertes High würde etwa 0,3 LI sparen, verändert aber die Form, deshalb nicht gemacht.',
}
for name in ('Axt', 'Schild', 'Speer'):
    b = json.load(open(os.path.join(WK, name, 'bericht.json')))
    q = quelle[name]; t = b['dreiecke']; by = b['bytes_geschaetzt']
    tex_size = '256 × 1024' if name == 'Speer' else '1024 × 1024'
    fp = b['lowest_farbpunkte']
    s = f"""# {name} · Upload-Anleitung Second Life

Statisches Dekoobjekt für den 1st Axe Honor Stand. Maße {b['masse_m'][0]:.3f} × {b['masse_m'][1]:.3f} × {b['masse_m'][2]:.3f} m (X × Y × Z).

## Dateien

| Datei | Zweck |
|---|---|
| `{name}.dae` | High, {t['High']} Dreiecke (Originalgeometrie, Originalnormalen) |
| `{name}_LOD2.dae` | Medium, {t['Medium']} Dreiecke |
| `{name}_LOD1.dae` | Low, {t['Low']} Dreiecke |
| `{name}_LOD0.dae` | Lowest, {t['Lowest']} Dreiecke |
| `{name}_PHYS.dae` | Physik, Quader 12 Dreiecke |
| `Texturen/{name}_Farbe.png` | Farbtextur mit eingebackenem AO ({tex_size}) |
| `Texturen/{name}_Normal.png` | Normal Map, OpenGL, Alpha = Glanzgrad |
| `Texturen/{name}_Glanz.png` | Specular Map, RGB = Glanzfarbe, Alpha = Umgebungsreflexion |
| `Texturen/PBR_optional/` | BaseColor, Normal, ORM für PBR-Materialien (nur bei Bedarf) |
| `Blender/{name}.blend` | Arbeitsdatei mit High, LODs, Physik und Material, Texturen relativ verknüpft |

Alle LODs haben exakt die Bounding Box des High. Fehlende Extrempunkte sind mit je zwei winzigen Anker-Dreiecken (0,5 mm) gesichert, nichts ist gestreckt.

## Upload im Mesh-Uploader

1. Datei `{name}.dae` als Modell wählen.
2. Reiter *Level of Detail*
   - High ist `{name}.dae`
   - Medium „Load from file“ `{name}_LOD2.dae`
   - Low „Load from file“ `{name}_LOD1.dae`
   - Lowest „Load from file“ `{name}_LOD0.dae`
3. Reiter *Physics* „From file“ `{name}_PHYS.dae`. Analyze ist nicht nötig.
4. Reiter *Upload options* Scale 1, „Include textures“ an. Damit kommt `{name}_Farbe.png` mit.
5. „Calculate weights & fee“, Werte notieren (Download, Physik, Server), dann hochladen.

## Nach dem Rezzen

| Fläche | Textur | Bumpiness (normal) | Shininess (specular) |
|---|---|---|---|
| einzige Fläche (Material `{name}_Material`) | `{name}_Farbe.png` | `{name}_Normal.png` | `{name}_Glanz.png` |

- Repeats 1, Offset 0, Rotation 0 für alle drei Karten. Alpha mode „None“.
- Physics Shape Type „Convex Hull“ lassen.
- Startwerte für Glanz Glossiness 51, Environment 0, Farbe weiß. Laut SL-Wiki liest der Viewer den Glanzgrad aus dem Alphakanal der Normal Map und die Umgebungsreflexion aus dem Alphakanal der Specular Map. Im Viewer nicht geprüft. Normal und Glanz zuerst über „Local“ im Texturwähler kostenlos testen, erst dann hochladen.
- Pflicht-Uploads 3 Texturen (Farbe kommt mit dem Mesh, Normal und Glanz einzeln). Die PBR-Karten nur hochladen, wenn das Objekt ein PBR-Material bekommen soll.

## LI-Schätzung

Eigener Schätzer (Verfahren der Mesh-Anleitung, Kalibrierung 0,706 aus Jarlswoman v8). Radius {b['radius_m']} m.

| Stufe | Dreiecke | komprimierte Bytes (geschätzt) |
|---|---|---|
| High | {t['High']} | {by['High']} |
| Medium | {t['Medium']} | {by['Medium']} |
| Low | {t['Low']} | {by['Low']} |
| Lowest | {t['Lowest']} | {by['Lowest']} |

Download-Gewicht roh {b['download_schaetzwert']}, im Uploader erwartet etwa **{b['download_uploader_geschaetzt']}**. Server-Gewicht mindestens 0,5, Physik als Quader klein. Erwarteter LI damit etwa **1**. Nicht im Viewer gemessen, bitte den Uploader-Wert in die STAND.md eintragen und neu eichen.

Lowest nach dem Farbpunkt-Verfahren. Statt eines einzigen UV-Punkts liegt jede Farbgruppe auf einer unverzerrten UV-Fläche von 2 Pixeln an einer Stelle mit flacher Normal Map. Ein Einzelpunkt macht die Tangentenbasis entartet und rendert mit Normal Map schwarz (im Blender-Test so aufgetreten).
Farbgruppen {', '.join(f"RGB {tuple(p['farbe_rgb'])} ({p['anteil']*100:.0f} % der Fläche)" for p in fp)}. Nach jeder Änderung der Farbtextur neu bestimmen.

## Was am Original geändert wurde

{anpassung[name]}

Texturen von 2048 auf {tex_size} verkleinert (Normal Map als Vektor gemittelt und renormiert). Normal-Map-Konvention {q['normal']} {q['ao']}

LODs {"aus dem Schild ohne die 55 Nieten (unter 3 cm), mit Blenders Decimate (Collapse), das Lowest als flaches Achteck von Hand gebaut" if name == 'Schild' else "mit MeshLab (Quadric Edge Collapse mit Texturerhalt), Lowest ohne Randerhalt"}. LOD-Punkte, die bei der Reduktion um wenige Millimeter über die High-Box hinausrutschten, wurden auf die Box geklemmt.

## Schwächste Stelle

{schwach[name]}

## Quelle und Lizenz

- Archiv im Repository `{q['archiv']}`
- verwendete Dateien `{q['datei']}`
- {q['meta']}
- {q['spur']}

**Vor einem Verkauf in SL** die Lizenz an der Originalseite prüfen und den Nachweis (Screenshot der Lizenz, Kaufbeleg oder Download-Bestätigung) ablegen. Ohne belegte Lizenz nur zum eigenen Gebrauch verwenden.
"""
    open(os.path.join(OUT, name, 'ANLEITUNG.md'), 'w').write(s)
print('ok')
