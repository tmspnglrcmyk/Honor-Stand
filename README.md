# Honor-Stand-Nachträge und Wikingerkiste

Jedes ZIP wurde in zwei Teile von höchstens 24 MiB zerlegt. Beide Teile eines ZIPs gehören in denselben Ordner. Die FBX-Datei kann direkt verwendet werden.

In der Linux-Cloud im Ordner mit diesen drei Unterordnern ausführen. Die Teile bleiben erhalten.

```bash
set -e
for first in */*.zip.part001; do
  archive=${first%.part001}
  cat "$archive.part001" "$archive.part002" > "$archive"
  unzip -t "$archive"
done
```

Beim Speer gehören die 2K-Texturen zur FBX-Datei. Beim Schild gehören das Blender- und das Texturarchiv zusammen. Bei der Kiste liegt das DAE-Modell im inneren Archiv `source/model.zip`.

Für diese Dateien lag kein Lizenznachweis bei. Vor öffentlicher Veröffentlichung die Quellen und die Erlaubnis zur Weitergabe klären.
