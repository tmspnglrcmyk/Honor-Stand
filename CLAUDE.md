# 1st Axe Honor Stand für Second Life

Die ZIPs mit Endungen .part001, .part002 usw. sind in aufsteigender Reihenfolge bytegenau zusammenzusetzen. In der Linux-Cloud im Repository-Hauptordner ausführen:

```bash
for first in *.zip.part001; do
  [ -f "$first" ] || continue
  archive=${first%.part001}
  cat "$archive".part[0-9][0-9][0-9] > "$archive"
  unzip -t "$archive" || exit 1
done
```

Bereite Axt, Schild, Speer und den vorgesehenen Helm als statische Dekoobjekte für SL auf. Prüfe zuerst Inhalt und Lizenz. Zwei Helmarchive und ein Waffenpaket liegen zur Auswahl bei. Wenn der vorgesehene Helm unklar ist, arbeite zunächst an Axt, Schild und Speer. Bearbeite Stücke aus dem Waffenpaket nur auf ausdrücklichen Wunsch.

Erhalte das Erscheinungsbild. Liefere pro Objekt DAE, LODs, einfache Physik, Texturen, Blender-Arbeitsdatei und kurze Uploadanleitung mit Quellenangabe. Eine gemeinsame Vorschau genügt. Blender darf für diesen Auftrag in der Cloud laufen. Lege die fertigen Dateien unter SL_Export ab. Upload, Land Impact und Gebühren werden später im SL-Viewer geprüft.
