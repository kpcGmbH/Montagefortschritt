# tools/ – Hilfsskripte

## md2pdf_kpc.py – Doku als PDF im KPC-Design

Wandelt eine Markdown-Datei in ein gebrandetes PDF um (beiger KPC-Kopfbalken,
braune Überschriften, Roboto Condensed Light). Die Schrift liegt in
`tools/fonts/` – läuft daher ohne Installation auf Mac **und** Windows.

**Einmalig die zwei Bibliotheken installieren:**
```
pip install markdown fpdf2
```

**Verwenden** (aus dem Projekt-Hauptordner):
```
python tools/md2pdf_kpc.py UEBERGABE-ENTWICKLUNG.md
python tools/md2pdf_kpc.py SICHERHEIT.md SICHERHEIT.pdf "Sicherheit"
```
- Ohne Zielnamen wird `<quelle>.pdf` erzeugt.
- Ohne Titel wird der Dateiname als Titel verwendet.

**Hinweis:** Die erzeugten PDFs sind über `.gitignore` (`*.pdf`) vom Repo
ausgeschlossen – sie werden bei Bedarf neu erzeugt, nicht versioniert.

Farben/Design lassen sich oben im Skript anpassen (`BROWN`, `BEIGE`, `INK`).
