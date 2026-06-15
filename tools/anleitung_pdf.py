#!/usr/bin/env python3
"""
KPC – Anleitung für Monteure (gestaltetes PDF im Corporate Design, mit App-Abbildungen).

Kopfbalken mit KPC-Logo, Titelblock, Grundlagen-Checkliste, Beispiel-Position,
Status-Filter und je eine farbige Karte pro Gewerk (Montage/Elektro/Sanitär) mit
eingebetteter Abbildung der Gewerk-Filterleiste.

Abbildungen vorher erzeugen:  python tools/mockups.py  + Render-Schritt (siehe README)
VORAUSSETZUNG:                pip install fpdf2
VERWENDUNG:                   python tools/anleitung_pdf.py [ziel.pdf]
"""
import os, sys, struct
from fpdf import FPDF

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonts", "RobotoCondensedLight.ttf")
LOGO = os.path.join(HERE, "kpc_logo.png")
IMG  = os.path.join(HERE, "img")

BROWN=(137,85,0); BEIGE=(215,193,174); INK=(45,38,32); GREY=(150,150,150)
G_M=(107,122,138); G_E=(184,134,11); G_S=(63,122,138); LINE=(212,205,198)
MARGIN=16; DOC_TITLE="Anleitung für Monteure"

GRUNDLAGEN=[
 ("App öffnen","kpcgmbh.github.io/Montagefortschritt – am besten als Lesezeichen anlegen oder zum Startbildschirm hinzufügen."),
 ("Anmelden","„Mit Microsoft anmelden\" mit deinem KPC-Konto, Adresse nachname@kpc-project.net – dein Name wird automatisch übernommen und bei jedem Häkchen mitgespeichert, so ist nachvollziehbar, wer was gemacht hat."),
 ("Baustelle wählen","In der Liste antippen. Über das Suchfeld nach Nummer oder Ort filtern."),
 ("Zurechtfinden","Oben: Geschoss-/Bereichsreiter, Suchfeld und die Gewerk-Filter Alle · Montage · Elektro · Sanitär."),
 ("Status abhaken","An der Position das passende Feld antippen – es wird grün mit Uhrzeit und deinem Namen. Nochmal tippen macht es rückgängig."),
 ("Foto & Notizen","„Foto\" antippen, dann Kamera aufnehmen oder aus der Galerie wählen. Protokoll als PDF, Anmerkungsfeld für Notizen, offene Punkte in die Restarbeiten-Liste."),
 ("Speichern & Sync","Oben steht „Synchron\", wenn alles hochgeladen ist. Bei „Offline – N ausstehend\" in der App bleiben bzw. online gehen, bis „Synchron\" erscheint."),
]
GEWERKE=[
 ("MONTAGE",G_M,"Filter oben: Montage","gewerk_M.png",[
   ("Geliefert","sobald das Gerät bzw. Teil auf der Baustelle angeliefert ist."),
   ("Montiert","sobald es aufgestellt, montiert oder eingebaut ist."),
   ("Foto","vom montierten Gerät anhängen."),
   ("Mängel / Fehlteile","als Restarbeit oder Anmerkung erfassen."),
 ]),
 ("ELEKTRO",G_E,"Filter oben: Elektro","gewerk_E.png",[
   ("Elektroanschluss","sobald das Gerät elektrisch angeschlossen ist."),
   ("Inbetriebnahme","abhaken, sobald das Gerät in Betrieb genommen ist."),
   ("Einweisung","abhaken, sobald Kunde bzw. Personal eingewiesen wurde."),
   ("Protokoll","im Zuge der Einweisung ablegen: über die „Protokoll\"-Schaltfläche das Einweisungsprotokoll als PDF an die Position hängen."),
   ("Foto","vom Anschluss anhängen."),
   ("Mängel / fehlender Anschluss","als Restarbeit oder Anmerkung erfassen."),
 ]),
 ("SANITÄR",G_S,"Filter oben: Sanitär","gewerk_S.png",[
   ("Sanitäranschluss","sobald Wasser bzw. Abwasser am Gerät angeschlossen ist."),
   ("Dichtigkeitsprüfung","eigenes Häkchen – kann auch später nachgezogen werden; mit Foto/Anmerkung belegen."),
   ("Foto","vom Anschluss anhängen."),
   ("Mängel / fehlender Anschluss","als Restarbeit oder Anmerkung erfassen."),
 ]),
]

def png_size(p):
    with open(p,"rb") as f:
        f.read(16); w,h=struct.unpack(">II", f.read(8)); return w,h

class PDF(FPDF):
    doc_title = DOC_TITLE
    def header(self):
        self.set_fill_color(*BEIGE); self.rect(0,0,self.w,15,"F")
        self.set_fill_color(*BROWN); self.rect(0,15,self.w,1.0,"F")
        try: self.image(LOGO,x=MARGIN,y=3.2,h=8.6)
        except Exception: pass
        self.set_text_color(*BROWN); self.set_font("RC","",9.5)
        self.set_xy(-110-self.r_margin,5); self.cell(110,6,self.doc_title,align="R")
        self.set_y(23)
    def footer(self):
        self.set_y(-12); self.set_font("RC","",8); self.set_text_color(*GREY)
        self.cell(0,8,"KPC GmbH  ·  Montagefortschritt  ·  Seite %s"%self.page_no(),align="C")

def heading(pdf,text):
    pdf.ln(2); pdf.set_font("RC","",16); pdf.set_text_color(*BROWN)
    pdf.cell(0,9,text,new_x="LMARGIN",new_y="NEXT")
    y=pdf.get_y(); pdf.set_draw_color(*BEIGE); pdf.set_line_width(0.5)
    pdf.line(MARGIN,y,pdf.w-MARGIN,y); pdf.ln(3)

def image_block(pdf,name,w,x=None,border=True):
    path=os.path.join(IMG,name); iw,ih=png_size(path); h=w*ih/iw
    if pdf.get_y()+h>pdf.h-16: pdf.add_page()
    if x is None: x=MARGIN
    y=pdf.get_y(); pdf.image(path,x=x,y=y,w=w)
    if border:
        pdf.set_draw_color(*LINE); pdf.set_line_width(0.2); pdf.rect(x,y,w,h)
    pdf.set_y(y+h)

def caption(pdf,text):
    pdf.set_font("RC","",9.5); pdf.set_text_color(*GREY)
    pdf.set_x(MARGIN); pdf.multi_cell(0,4.8,text); pdf.ln(1)

def numbered(pdf,i,title,desc):
    if pdf.get_y()>pdf.h-40: pdf.add_page()
    y=pdf.get_y(); r=3.3
    pdf.set_fill_color(*BROWN); pdf.ellipse(MARGIN,y,2*r,2*r,"F")
    pdf.set_text_color(255,255,255); pdf.set_font("RC","",10)
    pdf.set_xy(MARGIN,y+0.7); pdf.cell(2*r,5.2,str(i),align="C")
    colL=MARGIN+11; pdf.set_left_margin(colL); pdf.set_xy(colL,y)
    pdf.set_text_color(*BROWN); pdf.set_font("RC","",11.5); pdf.write(5.6,title+" – ")
    pdf.set_text_color(*INK); pdf.write(5.6,desc); pdf.ln(6.4)
    pdf.set_left_margin(MARGIN); pdf.set_x(MARGIN); pdf.ln(2.4)

def gewerk_card(pdf,title,color,filt,img,items):
    iw,ih=png_size(os.path.join(IMG,img)); imgW=120; imgH=imgW*ih/iw
    need=12+imgH+4+len(items)*7.4+8
    if pdf.get_y()+need>pdf.h-16: pdf.add_page()
    x,w=MARGIN,pdf.w-2*MARGIN; top=pdf.get_y()
    pdf.set_fill_color(*color); pdf.rect(x,top,w,9,"F")
    pdf.set_xy(x+4,top+1.4); pdf.set_text_color(255,255,255); pdf.set_font("RC","",13.5)
    pdf.cell(w-8,6,title,align="L")
    pdf.set_font("RC","",9.5); pdf.set_xy(x,top+1.9); pdf.cell(w-5,6,filt,align="R")
    pdf.set_y(top+12)
    body_top=pdf.get_y()
    image_block(pdf,img,imgW,x=x+6); pdf.ln(3)
    colL,colR=x+6,MARGIN+2; sq,txtL=2.2,x+6+5.0
    for kw,desc in items:
        y=pdf.get_y()
        pdf.set_fill_color(*color); pdf.rect(colL,y+1.7,sq,sq,"F")
        pdf.set_left_margin(txtL); pdf.set_right_margin(colR); pdf.set_xy(txtL,y)
        pdf.set_text_color(*color); pdf.set_font("RC","",11.5); pdf.write(5.6,kw+" ")
        pdf.set_text_color(*INK); pdf.set_font("RC","",11); pdf.write(5.6,"– "+desc); pdf.ln(7.4)
    pdf.set_left_margin(MARGIN); pdf.set_right_margin(MARGIN)
    pdf.set_fill_color(*color); pdf.rect(x,body_top-1,1.6,pdf.get_y()-(body_top-1),"F")
    pdf.ln(5)

def note_box(pdf,title,items):
    if pdf.get_y()+16+len(items)*7>pdf.h-16: pdf.add_page()
    x=MARGIN; top=pdf.get_y()
    pdf.set_font("RC","",13); pdf.set_text_color(*BROWN)
    pdf.set_xy(x+5,top); pdf.cell(0,7,title,new_x="LMARGIN",new_y="NEXT")
    colL,colR=x+5,MARGIN+2; sq,txtL=2.2,x+5+5.0
    for kw,desc in items:
        y=pdf.get_y()
        pdf.set_fill_color(*BROWN); pdf.rect(colL,y+1.7,sq,sq,"F")
        pdf.set_left_margin(txtL); pdf.set_right_margin(colR); pdf.set_xy(txtL,y)
        pdf.set_text_color(*BROWN); pdf.set_font("RC","",11); pdf.write(5.6,kw+" ")
        pdf.set_text_color(*INK); pdf.write(5.6,"– "+desc); pdf.ln(6.8)
    pdf.set_left_margin(MARGIN); pdf.set_right_margin(MARGIN)
    pdf.set_fill_color(*BEIGE); pdf.rect(x,top-1,1.6,pdf.get_y()-(top-1),"F")

def new_pdf(title):
    if not os.path.exists(FONT): sys.exit("Schrift fehlt: "+FONT)
    pdf=PDF(format="A4"); pdf.doc_title=title
    pdf.set_top_margin(23); pdf.set_auto_page_break(True,margin=16)
    pdf.set_left_margin(MARGIN); pdf.set_right_margin(MARGIN); pdf.add_font("RC","",FONT)
    pdf.add_page()
    return pdf

def title_block(pdf,title,subtitle):
    pdf.set_font("RC","",24); pdf.set_text_color(*BROWN)
    pdf.cell(0,11,title,new_x="LMARGIN",new_y="NEXT")
    pdf.set_font("RC","",11.5); pdf.set_text_color(*GREY)
    pdf.multi_cell(0,5.6,subtitle); pdf.ln(3)

def build_monteur(out):
    pdf=new_pdf("Anleitung für Monteure")
    title_block(pdf,"Anleitung für Monteure","Kurzanleitung zur Montagefortschritt-App – gemeinsame Grundlagen und je ein Abschnitt für Montage, Elektro und Sanitär.")
    heading(pdf,"Für alle – Grundlagen")
    for i,(t,d) in enumerate(GRUNDLAGEN,1): numbered(pdf,i,t,d)
    heading(pdf,"So sieht eine Position aus")
    caption(pdf,"Jede Position zeigt die für ihr Gewerk relevanten Status-Schalter (antippen = grün mit Uhrzeit und Name), dazu Foto/Protokoll und ein Anmerkungsfeld. Beispiel: ein Sanitär-Gerät – Montage + Sanitär-Anschluss + Dichtigkeitsprüfung. Ein Gewerk-Filter zeigt genau diese Felder (siehe unten).")
    image_block(pdf,"position.png",125); pdf.ln(4)
    heading(pdf,"Status-Filter (oben)")
    caption(pdf,"Die Zähler oben sind Klick-Filter: z. B. „Offen\" antippen, um nur noch offene Positionen zu sehen.")
    image_block(pdf,"statusbar.png",150); pdf.ln(4)
    heading(pdf,"Nach Gewerk")
    caption(pdf,"Sobald du oben ein Gewerk wählst, zeigt jede Position nur die für dich relevanten Auswahlfelder:")
    for title,color,filt,img,items in GEWERKE: gewerk_card(pdf,title,color,filt,img,items)
    pdf.output(out); print("PDF erstellt:",out,"(%d Bytes)"%os.path.getsize(out))

BL_GRUND=[
 ("App öffnen","kpcgmbh.github.io/Montagefortschritt – am besten als Lesezeichen anlegen."),
 ("Anmelden","„Mit Microsoft anmelden\" mit deinem KPC-Konto, Adresse nachname@kpc-project.net – danach öffnet sich die Baustellen-Auswahl."),
 ("Baustelle wählen","In der Liste antippen bzw. über das Suchfeld nach Nummer oder Ort filtern."),
]
BL_AUSF=[
 ("Badge antippen","Oben rechts neben dem Baustellennamen auf den aktuellen Ausführer tippen."),
 ("Fremdfirma","Für externe Arbeit „Fremdfirma\" wählen und den Firmennamen eintragen (z. B. GTS)."),
 ("Eigene Monteure","Für eigene Leute „Eigene Monteure\" wählen und den Namen eintragen."),
 ("Übernehmen","Ab jetzt wird jedes Häkchen diesem Ausführer + Uhrzeit zugeschrieben. Wechselt der Trupp/die Firma, vorher erneut umstellen."),
]
BL_NACH=[
 ("Gewerk-Filter wählen","Oben Montage / Elektro / Sanitär antippen – die Position zeigt dann nur die passenden Felder."),
 ("Position finden","Über das Suchfeld (Pos-Nr. oder Bezeichnung) oder über die Geschoss-/Bereichsreiter."),
 ("Schritte abhaken","Die erledigten Felder antippen – sie werden grün mit Uhrzeit und dem eingestellten Ausführer."),
 ("Belege","Bei Bedarf Foto/Protokoll anhängen und offene Punkte als Restarbeit erfassen."),
 ("Sync abwarten","Oben muss „Synchron\" stehen – dann ist alles in SharePoint gespeichert."),
]
BL_FOTO=[
 ("Foto","über „Foto\" antippen, dann Kamera aufnehmen oder aus der Galerie wählen; das Bild hängt dann an der Position."),
 ("Protokoll","über „Protokoll\" als PDF ablegen – insbesondere das Einweisungsprotokoll im Zuge der Einweisung (Elektro)."),
 ("Restarbeiten","offene Punkte je Position in der Restarbeiten-Liste erfassen (auch mit Foto möglich)."),
]
BL_BERICHT=[
 ("Kundenbericht","Gesamtstand je Position – wahlweise ohne oder mit Fotos (Schaltflächen „Bericht\" bzw. „+ Fotos\")."),
 ("Tagesbericht","Datum wählen; zeigt, wer (Firma/Monteur) an dem Tag welche Schritte erledigt hat."),
 ("Restarbeitenliste","alle offenen und erledigten Restarbeiten als PDF."),
 ("ZIP-Export","alle Fotos bzw. alle Protokolle der Baustelle gesammelt als ZIP herunterladen."),
]
BL_VERWALT=[
 ("Neue Baustelle","„Neue Baustelle aus Stückliste\": Excel/PDF hochladen, Vorschau prüfen, anlegen. Name im Format „Nummer Ort Objekt\"."),
 ("Umbenennen","in der Baustellen-Auswahl auf das Stift-Symbol der Kachel tippen."),
 ("Foto-Ordner aufräumen","nach dem Umbenennen bietet die App beim Öffnen an, vorhandene Fotos/Protokolle in den neuen Ordner zu verschieben – mit „Ja\" bestätigen."),
]

def build_bauleiter(out):
    pdf=new_pdf("Anleitung für Bauleiter")
    title_block(pdf,"Anleitung für Bauleiter","Überblick und Bedienung der Montagefortschritt-App – Schwerpunkt: Fortschritte für externe Firmen und eigene Monteure korrekt nachtragen.")

    heading(pdf,"Was die App macht")
    caption(pdf,"Die App bildet den Montage-/Leistungsfortschritt je Position ab: abhaken (Geliefert, Montiert, Anschlüsse, Dichtigkeitsprüfung, Inbetriebnahme, Einweisung), Fotos und Protokolle anhängen, Restarbeiten führen und Berichte erzeugen. Alle Daten liegen im KPC-SharePoint; jede Änderung wird mit Uhrzeit und Ausführer gespeichert und automatisch synchronisiert (auch offline-fähig).")

    heading(pdf,"Grundlagen")
    for i,(t,d) in enumerate(BL_GRUND,1): numbered(pdf,i,t,d)

    heading(pdf,"Aufbau der App")
    caption(pdf,"Kopfbereich: links das Logo, rechts die aktive Baustelle und darunter der Ausführer (antippbar). Darunter die Geschoss-/Bereichsreiter, das Suchfeld, die Gewerk-Filter und die Status-Zähler (zugleich Klick-Filter).")
    image_block(pdf,"filter_all.png",150); pdf.ln(3)
    image_block(pdf,"statusbar.png",150); pdf.ln(4)

    heading(pdf,"Ausführer festlegen – wer hat die Arbeit gemacht?")
    caption(pdf,"Jedes Häkchen wird mit dem aktuell eingestellten Ausführer und der Uhrzeit gespeichert. Deshalb VOR dem Nachtragen den richtigen Ausführer wählen – nicht dich selbst, sondern die Firma bzw. den Monteur, der die Arbeit ausgeführt hat.")
    caption(pdf,"Oben rechts steht der aktuelle Ausführer – antippen zum Ändern:")
    image_block(pdf,"ausf_badge.png",150); pdf.ln(3)
    image_block(pdf,"ausf_dialog.png",120); pdf.ln(4)
    for i,(t,d) in enumerate(BL_AUSF,1): numbered(pdf,i,t,d)

    heading(pdf,"Fortschritt nachtragen")
    for i,(t,d) in enumerate(BL_NACH,1): numbered(pdf,i,t,d)
    pdf.ln(1); image_block(pdf,"position.png",125); pdf.ln(4)

    heading(pdf,"Felder je Gewerk")
    caption(pdf,"Je nach Gewerk-Filter erscheinen genau diese Felder:")
    image_block(pdf,"gewerk_M.png",120); pdf.ln(2)
    image_block(pdf,"gewerk_E.png",120); pdf.ln(2)
    image_block(pdf,"gewerk_S.png",120); pdf.ln(4)

    heading(pdf,"Fotos & Protokolle")
    for i,(t,d) in enumerate(BL_FOTO,1): numbered(pdf,i,t,d)

    heading(pdf,"Berichte & Auswertung")
    for i,(t,d) in enumerate(BL_BERICHT,1): numbered(pdf,i,t,d)

    heading(pdf,"Baustellen verwalten")
    for i,(t,d) in enumerate(BL_VERWALT,1): numbered(pdf,i,t,d)

    pdf.ln(1)
    note_box(pdf,"Extern vs. eigene Monteure",[
      ("Externe Firma","Ausführer auf die Fremdfirma stellen und deren erledigte Schritte nachtragen."),
      ("Eigene Monteure","Name als Ausführer setzen – oder die Monteure tragen selbst ein (siehe Monteur-Anleitung)."),
    ])
    pdf.output(out); print("PDF erstellt:",out,"(%d Bytes)"%os.path.getsize(out))

if __name__=="__main__":
    base=os.path.dirname(HERE)
    which=sys.argv[1].lower() if len(sys.argv)>1 else "both"
    if which in ("monteur","both"): build_monteur(os.path.join(base,"Anleitung-Monteure.pdf"))
    if which in ("bauleiter","both"): build_bauleiter(os.path.join(base,"Anleitung-Bauleiter.pdf"))
