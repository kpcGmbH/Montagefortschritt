#!/usr/bin/env python3
"""
KPC-PDF-Generator – wandelt eine Markdown-Datei in ein PDF im KPC-Corporate-Design um.

Design: beiger Kopfbalken (#d7c1ae) mit "KPC | Montagefortschritt" + Dokumenttitel,
Überschriften in KPC-Braun (#895500), durchgängig Roboto Condensed Light, Fußzeile mit
Seitenzahl. Die Schrift liegt mit im Repo (tools/fonts/), läuft also ohne Installation
auf Mac und Windows.

VORAUSSETZUNG (einmalig):
    pip install markdown fpdf2

VERWENDUNG:
    python tools/md2pdf_kpc.py <quelle.md> [ziel.pdf] ["Titel"]

BEISPIELE:
    python tools/md2pdf_kpc.py UEBERGABE-ENTWICKLUNG.md
    python tools/md2pdf_kpc.py SICHERHEIT.md SICHERHEIT.pdf "Sicherheit"

Ohne Zielname wird <quelle>.pdf erzeugt; ohne Titel wird der Dateiname verwendet.
"""
import sys, os, re
import markdown
from fpdf import FPDF

# ── KPC-Corporate-Design ──────────────────────────────────────────────────────
BROWN = (137, 85, 0)      # #895500  Überschriften / Akzent
BEIGE = (215, 193, 174)   # #d7c1ae  Kopfbalken
INK   = (45, 38, 32)      # Fließtext
GREY  = (150, 150, 150)   # Fußzeile

# Schrift suchen: erst im Repo (self-contained), dann gängige System-Pfade.
_HERE = os.path.dirname(os.path.abspath(__file__))
_FONT_CANDIDATES = [
    os.path.join(_HERE, "fonts", "RobotoCondensedLight.ttf"),
    os.path.expanduser("~/Library/Fonts/RobotoCondensedLight-Standalone.ttf"),
    r"C:\Windows\Fonts\RobotoCondensed-Light.ttf",
    os.path.expanduser("~/AppData/Local/Microsoft/Windows/Fonts/RobotoCondensed-Light.ttf"),
]
FONT = next((p for p in _FONT_CANDIDATES if os.path.exists(p)), None)
if not FONT:
    sys.exit("Schrift nicht gefunden – tools/fonts/RobotoCondensedLight.ttf fehlt.")

# Zeichen, die ein PDF-Font nicht (zuverlässig) kann -> Klartext/entfernen.
REPL = {
    '✅':'', '🎉':'', '🎯':'', '📋':'', '⚠️':'! ', '⚠':'! ', '➕':'+ ', '🎂':'', '✓':'[x]',
    '→':'->', '←':'<-', '↔':'<->', '⇒':'=>', '•':'-', '↻':'', '⟳':'', '⮕':'->', '⬆':'', '⬇':'',
    '…':'...', '–':'-', '—':'-', '‚':"'", '‘':"'", '’':"'", '„':'"', '“':'"', '”':'"', '€':'EUR',
}


def build_html(md_text):
    md_text = re.sub(r'^#\s+.*\n', '', md_text, count=1)          # erste # …-Zeile -> Titel im Kopf
    for k, v in REPL.items():
        md_text = md_text.replace(k, v)
    html = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'sane_lists'])
    html = ''.join(ch for ch in html if ord(ch) < 0x2500)        # restliche Sonderzeichen raus
    # fpdf2 verträgt keine Inline-Tags in Tabellenzellen -> dort entfernen (Text bleibt)
    html = re.sub(r'<(td|th)([^>]*)>(.*?)</\1>',
                  lambda m: '<%s%s>%s</%s>' % (m.group(1), m.group(2),
                      re.sub(r'</?(code|strong|em|b|i|a)[^>]*>', '', m.group(3)), m.group(1)),
                  html, flags=re.S)
    # Überschriften in KPC-Braun
    html = re.sub(r'<(h[1-4])>(.*?)</\1>',
                  lambda m: '<%s><font color="#895500">%s</font></%s>' % (m.group(1), m.group(2), m.group(1)),
                  html, flags=re.S)
    return html


class KpcPDF(FPDF):
    title = ""
    def header(self):
        self.set_fill_color(*BEIGE); self.rect(0, 0, self.w, 16, 'F')
        self.set_fill_color(*BROWN);  self.rect(0, 16, self.w, 1.1, 'F')
        self.set_text_color(*BROWN); self.set_font('RC', '', 9.5)
        self.set_xy(self.l_margin, 5); self.cell(0, 6, 'KPC  |  Montagefortschritt', align='L')
        self.set_xy(-120 - self.r_margin, 5); self.cell(120, 6, self.title, align='R')
        self.set_y(24)
    def footer(self):
        self.set_y(-12); self.set_font('RC', '', 8); self.set_text_color(*GREY)
        self.cell(0, 8, 'KPC GmbH  ·  Seite %s' % self.page_no(), align='C')


def convert(src, out, title):
    html = build_html(open(src, encoding='utf-8').read())
    pdf = KpcPDF(format='A4'); pdf.title = title
    pdf.set_top_margin(24); pdf.set_auto_page_break(True, margin=16)
    for st in ('', 'B', 'I', 'BI'):
        pdf.add_font('RC', st, FONT)          # nur Light – Hierarchie über Größe/Farbe
    pdf.add_page()
    pdf.set_font('RC', '', 20); pdf.set_text_color(*BROWN)
    pdf.multi_cell(0, 9, title); pdf.ln(1)
    pdf.set_draw_color(*BEIGE); pdf.set_line_width(0.6)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y()); pdf.ln(4)
    pdf.set_text_color(*INK); pdf.set_font('RC', '', 11)
    pdf.write_html(html, table_line_separators=True)
    pdf.output(out)
    print('PDF erstellt:', out, '(%d Bytes)' % os.path.getsize(out))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + '.pdf'
    title = sys.argv[3] if len(sys.argv) > 3 else os.path.splitext(os.path.basename(src))[0]
    convert(src, out, title)
