#!/usr/bin/env python3
"""
Erzeugt SVG-Nachbauten von App-Elementen (Gewerk-Filterleiste, Status-Zähler,
Beispiel-Position) im exakten KPC-/App-Design – als Bildvorlagen für die Anleitung.
Schreibt die SVGs nach tools/img/.  Rendering zu PNG erfolgt per qlmanage (Shell).
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "img"); os.makedirs(OUT, exist_ok=True)

# Farben (= App)
DARK="#2b2b2b"; ACCENT="#d7c1ae"; BORDER_DK="#4a443e"; BRAUN="#895500"
WHITE="#ffffff"; ACC2="#a8a8a8"; LINE="#d4cdc6"; BG="#f5f3f0"
GREEN="#3a7a3a"; C_SA="#1a5f7a"; C_DP="#2a7fa6"; C_EA="#b8860b"; C_IB="#5b4c8a"; C_EW="#1a6b6b"

def textw(label, fs):
    w=0.0
    for ch in label:
        o=ord(ch)
        if o>=0x2600: w+=fs*1.18          # Emoji
        elif ch==" ": w+=fs*0.30
        elif ch in "·.": w+=fs*0.30
        else: w+=fs*0.54
    return w

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

# ---------- 1) Gewerk-Filterleiste ----------
def filterbar(active):  # active in {None,'M','E','S'}
    FS=16; PADX=14; GAP=9; H=36; y=14; barH=64
    items=[("Alle", active is None and False),
           ("🔧 Montage", active=='M'),
           ("⚡ Elektro", active=='E'),
           ("🚿 Sanitär", active=='S')]
    x=16; svg_pills=[]
    for label,on in items:
        w=textw(label,FS)+2*PADX
        if on:
            fill=ACCENT; stroke="none"; tcol=DARK
        else:
            fill=DARK; stroke=BORDER_DK; tcol=WHITE
        op=' fill-opacity="0.85"' if not on else ''
        svg_pills.append(
            f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{H}" rx="{H/2}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>'
            f'<text x="{x+PADX:.1f}" y="{y+H/2+FS*0.36:.1f}" font-family="Arial" '
            f'font-size="{FS}" font-weight="700" fill="{tcol}"{op}>{esc(label)}</text>')
        x+=w+GAP
    W=int(x+6)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{barH}" '
            f'viewBox="0 0 {W} {barH}"><rect width="{W}" height="{barH}" fill="{DARK}"/>'
            + "".join(svg_pills) + '</svg>')

# ---------- 2) Status-Zähler-Filter ----------
def statusbar():
    FS=16; y=34; barH=58
    items=[("#5cb85c","Vollständig","120"),
           ("#e8aa40","Teilweise","60"),
           ("#2a7fa6","Angeschlossen","25"),
           ("#a8a8a8","Offen","70"),
           (None,"Gesamt","275")]
    x=16; parts=[]
    for dot,label,cnt in items:
        if dot:
            parts.append(f'<circle cx="{x+5:.1f}" cy="{y-FS*0.32:.1f}" r="5" fill="{dot}"/>')
            x+=15
        txt=f'{label}: '
        parts.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial" font-size="{FS}" '
                     f'fill="{WHITE}" fill-opacity="0.9">{esc(txt)}<tspan font-weight="700" '
                     f'fill="{WHITE}" fill-opacity="1">{cnt}</tspan></text>')
        x+=textw(txt,FS)+textw(cnt,FS)+22
    W=int(x+6)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{barH}" '
            f'viewBox="0 0 {W} {barH}"><rect width="{W}" height="{barH}" fill="{BRAUN}"/>'
            + "".join(parts) + '</svg>')

# ---------- 3) Beispiel-Position ----------
def position_card():
    W=560; FS=16
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="250" viewBox="0 0 {W} 250">']
    p.append(f'<rect width="{W}" height="250" fill="{BG}"/>')
    p.append(f'<rect x="0" y="0" width="4" height="250" fill="{ACCENT}"/>')
    # Pos-Badge
    p.append(f'<rect x="18" y="16" width="120" height="18" rx="4" fill="{DARK}"/>')
    p.append(f'<text x="26" y="29" font-family="Arial" font-size="10.5" font-weight="700" fill="{ACCENT}">01.02.00.00.01.</text>')
    # Bezeichnung + Meta
    p.append(f'<text x="18" y="56" font-family="Arial" font-size="16" font-weight="700" fill="{DARK}">Mischarmatur mit Schlauchhalter-Set</text>')
    p.append(f'<text x="18" y="76" font-family="Arial" font-size="12.5" fill="{ACC2}">1 Stk · KWC/Armag · 100.191</text>')
    # Checkbox-Pills
    # Beispiel: Sanitär-Gerät (Gewerk Montage+Sanitär) -> in "Alle" nur die relevanten Felder
    checks=[("Geliefert",GREEN,True),("Montiert",GREEN,True),("Sanitäranschluss",C_SA,True),("Dichtigkeitsprüfung",C_DP,False)]
    x=18; y=92; H=30; PADX=11; GAP=8; rowmax=W-16
    for label,col,on in checks:
        inner=("✓ " if on else "○ ")+label
        w=textw(inner,14)+2*PADX
        if x+w>rowmax: x=18; y+=H+8
        if on: fill=col; stroke="none"; tcol=WHITE
        else:  fill=WHITE; stroke=LINE; tcol=DARK
        p.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{H}" rx="14" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        p.append(f'<text x="{x+PADX:.1f}" y="{y+H/2+5:.1f}" font-family="Arial" font-size="13.5" '
                 f'font-weight="700" fill="{tcol}">{esc(inner)}</text>')
        x+=w+GAP
    # Buttons
    by=y+H+14
    for i,(lbl,em) in enumerate([("Foto","📷"),("Protokoll","📄")]):
        bx=18+i*120; inner=f'{em} {lbl}'; w=textw(inner,14)+24
        p.append(f'<rect x="{bx}" y="{by}" width="{w:.1f}" height="30" rx="15" fill="{DARK}"/>')
        p.append(f'<text x="{bx+12}" y="{by+20}" font-family="Arial" font-size="13.5" font-weight="700" fill="{WHITE}">{esc(inner)}</text>')
    # Anmerkung
    ay=by+40
    p.append(f'<rect x="18" y="{ay}" width="{W-36}" height="28" rx="6" fill="{WHITE}" stroke="{LINE}" stroke-width="1"/>')
    p.append(f'<text x="28" y="{ay+19}" font-family="Arial" font-size="12.5" fill="{ACC2}">Anmerkung …</text>')
    p.append('</svg>')
    # Höhe an Inhalt anpassen
    svg="".join(p).replace('height="250" viewBox="0 0 560 250"', f'height="{ay+40}" viewBox="0 0 {W} {ay+40}"')
    svg=svg.replace('<rect width="560" height="250"', f'<rect width="{W}" height="{ay+40}"')
    svg=svg.replace('<rect x="0" y="0" width="4" height="250"', f'<rect x="0" y="0" width="4" height="{ay+40}"')
    return svg

# ---------- 4) Gewerk-Komposit: Filterleiste + reduzierte Felder ----------
def gewerk_composite(active, fields):
    FS=16; H=36; PADX=14; GAP=9
    bar_items=[("Alle",False),("🔧 Montage",active=='M'),("⚡ Elektro",active=='E'),("🚿 Sanitär",active=='S')]
    bx=16; bar=[]
    for label,on in bar_items:
        w=textw(label,FS)+2*PADX
        fill=ACCENT if on else DARK; stroke="none" if on else BORDER_DK; tcol=DARK if on else WHITE
        op='' if on else ' fill-opacity="0.85"'
        bar.append(f'<rect x="{bx:.1f}" y="14" width="{w:.1f}" height="{H}" rx="{H/2}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>'
                   f'<text x="{bx+PADX:.1f}" y="{14+H/2+FS*0.36:.1f}" font-family="Arial" font-size="{FS}" font-weight="700" fill="{tcol}"{op}>{esc(label)}</text>')
        bx+=w+GAP
    barW=bx+6; barH=64; fy_cap=barH+18; fy=barH+26; FH=34
    fx=16; fpl=[]
    for label,color,on in fields:
        inner=("✓ " if on else "○ ")+label; w=textw(inner,14)+2*PADX
        if on: fill=color; stroke="none"; tcol=WHITE
        else:  fill=WHITE; stroke=LINE; tcol=DARK
        fpl.append(f'<rect x="{fx:.1f}" y="{fy}" width="{w:.1f}" height="{FH}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
                   f'<text x="{fx+PADX:.1f}" y="{fy+FH/2+5:.1f}" font-family="Arial" font-size="13.5" font-weight="700" fill="{tcol}">{esc(inner)}</text>')
        fx+=w+GAP
    W=int(max(barW,fx+6)); Htot=int(fy+FH+12)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Htot}" viewBox="0 0 {W} {Htot}">'
            f'<rect x="0" y="0" width="{W}" height="{barH}" fill="{DARK}"/>'
            f'<rect x="0" y="{barH}" width="{W}" height="{Htot-barH}" fill="{BG}"/>'
            + "".join(bar)
            + f'<text x="16" y="{fy_cap}" font-family="Arial" font-size="12.5" fill="#7a7a7a">Diese Felder erscheinen:</text>'
            + "".join(fpl) + '</svg>')

# ---------- 5) Ausführer-Badge (Kopf, oben rechts) ----------
def ausf_badge():
    W=560; H=74; name="0994.20 Bergisch Gladbach Mensa GGS"; badge="🏢 GTS"
    bw=textw(badge,15)+26; bx=W-16-bw
    p=[f'<rect width="{W}" height="{H}" fill="{DARK}"/>',
       f'<text x="{W-16}" y="30" text-anchor="end" font-family="Arial" font-size="13.5" fill="#cfcac4">{esc(name)}</text>',
       f'<rect x="{bx:.1f}" y="42" width="{bw:.1f}" height="26" rx="13" fill="none" stroke="{ACCENT}" stroke-width="1.5"/>',
       f'<text x="{bx+bw/2:.1f}" y="60" text-anchor="middle" font-family="Arial" font-size="14" font-weight="700" fill="{ACCENT}">{esc(badge)}</text>']
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'+"".join(p)+'</svg>'

# ---------- 6) Ausführer-Dialog ----------
def ausf_dialog():
    W=520; ih=34
    s1,s2=62,79; r1=110; i1=r1+12; r2=i1+ih+26; i2=r2+12; by=i2+ih+24; bh=34; H=by+bh+18
    p=[f'<rect width="{W}" height="{H}" rx="14" fill="#ffffff" stroke="{LINE}" stroke-width="1"/>',
       f'<text x="24" y="42" font-family="Arial" font-size="18" font-weight="700" fill="{DARK}">Ausführer wählen</text>',
       f'<text x="24" y="{s1}" font-family="Arial" font-size="12.5" fill="{ACC2}">Wird bei jedem Häkchen mitgespeichert – für die Zuordnung zu</text>',
       f'<text x="24" y="{s2}" font-family="Arial" font-size="12.5" fill="{ACC2}">Firmen bzw. eigenen Monteuren.</text>',
       f'<circle cx="34" cy="{r1}" r="7" fill="#fff" stroke="{ACC2}" stroke-width="2"/>',
       f'<text x="50" y="{r1+5}" font-family="Arial" font-size="15" font-weight="700" fill="{DARK}">👷 Eigene Monteure</text>',
       f'<rect x="50" y="{i1}" width="{W-74}" height="{ih}" rx="8" fill="#fff" stroke="{LINE}" stroke-width="1"/>',
       f'<text x="62" y="{i1+22}" font-family="Arial" font-size="14" fill="{DARK}">Max Mustermann</text>',
       f'<circle cx="34" cy="{r2}" r="7" fill="{BRAUN}" stroke="{BRAUN}" stroke-width="2"/>',
       f'<circle cx="34" cy="{r2}" r="2.6" fill="#fff"/>',
       f'<text x="50" y="{r2+5}" font-family="Arial" font-size="15" font-weight="700" fill="{DARK}">🏢 Fremdfirma</text>',
       f'<rect x="50" y="{i2}" width="{W-74}" height="{ih}" rx="8" fill="#fff" stroke="{BRAUN}" stroke-width="1.5"/>',
       f'<text x="62" y="{i2+22}" font-family="Arial" font-size="14" font-weight="700" fill="{DARK}">GTS</text>',
       f'<rect x="{W-220}" y="{by}" width="96" height="{bh}" rx="8" fill="#fff" stroke="{LINE}" stroke-width="1"/>',
       f'<text x="{W-172}" y="{by+22}" font-family="Arial" font-size="14" fill="{DARK}" text-anchor="middle">Abbrechen</text>',
       f'<rect x="{W-114}" y="{by}" width="96" height="{bh}" rx="8" fill="{ACCENT}"/>',
       f'<text x="{W-66}" y="{by+22}" font-family="Arial" font-size="14" font-weight="700" fill="{DARK}" text-anchor="middle">Übernehmen</text>']
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'+"".join(p)+'</svg>'

def write(name, svg):
    path=os.path.join(OUT,name+".svg"); open(path,"w",encoding="utf-8").write(svg)
    print("svg:",path)

write("filter_all", filterbar(None))
write("filter_M", filterbar('M'))
write("filter_E", filterbar('E'))
write("filter_S", filterbar('S'))
write("statusbar", statusbar())
write("position", position_card())
write("gewerk_M", gewerk_composite('M', [("Geliefert",GREEN,True),("Montiert",GREEN,True)]))
write("gewerk_E", gewerk_composite('E', [("Elektroanschluss",C_EA,True),("Inbetriebnahme",C_IB,False),("Einweisung",C_EW,False)]))
write("gewerk_S", gewerk_composite('S', [("Sanitäranschluss",C_SA,True),("Dichtigkeitsprüfung",C_DP,False)]))
write("ausf_badge", ausf_badge())
write("ausf_dialog", ausf_dialog())
print("fertig.")
