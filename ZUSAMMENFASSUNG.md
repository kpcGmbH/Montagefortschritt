# Projekt Montagefortschritt – Zusammenfassung

Stand: 2026-06-15

## Ziel
Nachbau und Weiterentwicklung der KPC-Leistungsfeststellungs-App
(Original: https://carpedings-cpu.github.io/KPC-Berlin-Upbeat/) – mit Umzug
des Backends in den **KPC-Microsoft-365-Tenant** und festem Hosting.

## Was die App ist
Montagefortschritt-/Leistungsfeststellungs-App für Baustellen. Pro Position
abhaken (Geliefert, Montiert, Sanitäranschluss, Dichtigkeitsprüfung,
Elektroanschluss, Inbetriebnahme, Einweisung), Fotos, Notizen, Restarbeiten,
PDF-Protokolle mit Stift-Editor, Berichte/Exporte (Kundenbericht, Tagesbericht,
ZIP). Eine einzige `index.html`, Bibliotheken (pdf.js, jsPDF, JSZip, MSAL,
SheetJS) per CDN. Offline-fähige PWA mit SharePoint/Microsoft-Graph-Backend.

## Aktueller Stand: PRODUKTIV ✅
- **Live-URL:** https://kpcgmbh.github.io/Montagefortschritt/ (großes „M“,
  Adresse ist case-sensitive)
- Login (Microsoft, nur KPC-Konten) + Datenzugriff auf **Desktop und Handy**.
- Der Trupp braucht nur diese URL – kein localhost, kein Tunnel.
- **Service-Worker-Cache aktuell:** `kpc-montage-v22`.

## Projekte (einheitliches Namensschema „Nummer Ort Objekt“)
- **`0908.20 Berlin Upbeat`** – 388 Positionen, alle Gewerke klassifiziert,
  Anschlussarbeiten der Fa. GTS zugeordnet, Echtdaten migriert.
- **`0994.20 Bergisch Gladbach Mensa GGS`** – aus altem Tool migriert
  (Fortschritt + Fotos); Fotos in den neuen Ordner konsolidiert.
- **`1038.20 Göttingen Kita Montessori`** – aus Stückliste angelegt.
- **`1037.20 Frankfurt Kirkland & Ellis FOUR`** (18 Pos), **`1062.20 Korbach
  Berliner Schule`** (31 Pos), **`0959.20 Kassel Bildungscampus Waldau Kita`**
  (46 Pos), **`0831.20 Wiesbaden BKA`** (49 Pos) – aus den alten
  carpedings/Supabase-Apps migriert (Fortschritt, Fotos, Protokolle, Restarbeiten;
  ohne Gewerk = Montage). Migrationscode war temporär und wurde nach Abschluss entfernt.

## Anmeldung
- „Mit Microsoft anmelden“ mit dem KPC-Konto im Format **`nachname@kpc-project.net`**.
- Der Bearbeitername wird **automatisch aus dem Login** abgeleitet (keine
  Kürzel-Eingabe). Danach direkt zur Baustellen-Auswahl.

## Baustellen-Auswahl
- **Durchsuchbare Liste** (Suchfeld filtert live nach Nummer/Ort/Objekt,
  Mehrwort-UND-Suche), scrollbar.
- Je Kachel: Name, **letzte Änderung** (Datum) und ✏️ zum **Umbenennen**.
  Sortierung nach letzter Änderung (zuletzt bearbeitet oben).
  Der Ersteller wird nicht mehr angezeigt.
- **Neue Baustelle:** „➕ Neue Baustelle aus Stückliste“ → Excel/PDF hochladen →
  Vorschau → anlegen. Der Projektname **muss** dem Schema „Nummer Ort Objekt“
  folgen (z. B. `0908.20 Berlin Upbeat`); wird beim Anlegen erzwungen.

## Statusfelder & Logik je Gewerk
Sieben Statusfelder; je Position mit Zeitstempel + Ausführer gestempelt:
**Geliefert, Montiert, Sanitäranschluss, Dichtigkeitsprüfung, Elektroanschluss,
Inbetriebnahme, Einweisung.**

- **Filterabhängige Anzeige:** Wählt man oben ein Gewerk, zeigt jede Position nur
  die relevanten Felder. In „Alle“ erscheinen pro Position genau die Felder ihrer
  Gewerke (deckungsgleich mit den Filtern **und** mit der „Vollständig“-Logik).
  - **Montage** → Geliefert · Montiert
  - **Elektro** → Elektroanschluss · Inbetriebnahme · Einweisung
  - **Sanitär** → Sanitäranschluss · Dichtigkeitsprüfung
- **Vollständig** (`GEW_FIELDS`): M = Geliefert+Montiert · S = Sanitäranschluss+
  Dichtigkeitsprüfung · E = Elektroanschluss+Inbetriebnahme+Einweisung.
- **Dichtigkeitsprüfung** ist ein eigenes Häkchen (oft später nachzuziehen) und
  zählt zum Sanitär-Gewerk.
- **Statuszähler** (zugleich Klick-Filter): Vollständig / Teilweise / Angeschlossen /
  Offen / Gesamt.
- Technisch (`index.html`): `GEW_FIELDS`, `POSGEW`, `relFields()`, `ist(pos,ctx)`,
  `applyFieldVisibility()`, feste Labels im Markup.

## Ausführer-Zuordnung: Firma / eigene Monteure
Oben rechts der Ausführer-Badge → Dialog „Ausführer wählen“:
- **👷 Eigene Monteure** (Name) oder **🏢 Fremdfirma** (z. B. GTS) – wird bei
  **jedem Häkchen** als Ausführer (`by`) + Uhrzeit mitgestempelt.
- Bauleiter tragen so den Fortschritt **externer** und eigener Monteure korrekt nach
  (vor dem Abhaken den richtigen Ausführer wählen, bei Wechsel umstellen).
- Speicherung in `localStorage`; Login-Standard = eigener Monteur.

## Fotos, Protokolle, Berichte
- **Foto:** je Position „Foto“ → Auswahl **Kamera aufnehmen** oder **Aus Galerie
  wählen** (zuverlässig auch auf Android dank `capture`-Attribut).
- **Protokoll:** PDF je Position; bei **Elektro** insbesondere das
  **Einweisungsprotokoll im Zuge der Einweisung**.
- **Ablage in Ordnern** `Baustelle / Etage / Anlage`; Datei-Referenz ist ein Pfad.
- **Berichte:** Kundenbericht (ohne/mit Fotos), **Tagesbericht mit Datumsauswahl**
  (zeigt je Tag, wer – Firma/Monteur – was erledigt hat; Schnellauswahl aktiver
  Tage), Restarbeitenliste, ZIP-Export (alle Fotos / alle Protokolle).

## Offline-Fähigkeit (PWA)
- **Service Worker (`sw.js`):** cacht App-Shell + CDN-Bibliotheken; Graph/Login/
  SharePoint nie gecacht. Bei jeder Veröffentlichung mit Shell-Änderung die
  `CACHE`-Konstante hochzählen (aktuell `kpc-montage-v22`).
- **IndexedDB + Outbox/Auto-Sync:** Häkchen, Notizen, Restarbeiten, Fotos, Protokolle
  werden offline gespeichert und bei Netz automatisch hochgeladen. Kopf-Status:
  „✓ Synchron“ / „↻ N wird synchronisiert“ / „⚠ Offline · N ausstehend“.
- Installierbar als Homescreen-App (Standalone).

## Ordner konsolidieren nach Umbenennen
- Foto-/Protokoll-Ordner heißen wie der **Anzeigename** der Baustelle. Nach einem
  Umbenennen bietet die App beim Öffnen an, vorhandene Dateien in den neuen Ordner
  zu verschieben **und die gespeicherten Pfade anzugleichen** (`ordnerKonsolidieren`).
- **Wichtig:** SharePoint-Ordner nie von Hand umbenennen (sonst verlieren alte Fotos
  ihre Verknüpfung) – immer über diese Funktion; leere Alt-Ordner danach löschen.

## Erscheinungsbild / Corporate Design
- Echtes kpc-Logo (SVG), CD-Farben (Ocker `#895500`, Tan `#d7c1ae`, CD-Grautöne),
  Schrift **Roboto Condensed Light**.
- **Hell-/Dunkel-Modus** automatisch nach Geräteeinstellung, plus manueller
  Umschalter (Auto/Hell/Dunkel) im Kopf.

## Anleitungen (für die Praxis)
Erzeugt im KPC-Design über `tools/anleitung_pdf.py` (Mockups: `tools/mockups.py`,
Bilder in `tools/img/`):
- **`Anleitung-Monteure.pdf`** – Grundlagen, Beispiel-Position, Status-Filter, je
  Gewerk „Filter setzen → diese Felder erscheinen“.
- **`Anleitung-Bauleiter.pdf`** – umfassende Bedienreferenz; Schwerpunkt
  Fortschritt **nachtragen** (Ausführer setzen), plus App-Aufbau, Felder je Gewerk,
  Fotos/Protokolle, Berichte, Baustellen verwalten.
- Bauen: `python3 tools/anleitung_pdf.py both` (bzw. `monteur` / `bauleiter`).

## Wichtige Eckdaten
- **Entra-App:** „Montagefortschritt“, Client-ID `68f89557-eef9-4481-b45c-29919ed7b55d`,
  Tenant-ID `cba1b1fc-4a80-4da1-a7f1-e3e4614056eb`.
- **Redirect-URIs (Entra → SPA):** `https://kpcgmbh.github.io/Montagefortschritt/`
  (produktiv); optional `http://localhost:5173`.
- **SharePoint:** Site `https://kpcfulda.sharepoint.com/sites/Montagefortschritt`,
  Liste „Positionen“ (Spalten `pos`, `data`, `projekt`), Bibliothek „Fotos“.
  Projekt-Registry `__projects.json`, Stücklisten `LV_<pid>.json` (in „Fotos“).
- **GitHub:** Repo `kpcgmbh/Montagefortschritt` (public), Dateien `index.html`,
  `sw.js`, `manifest.webmanifest`.

## Betrieb & Wartung
- **App aktualisieren:** `index.html` (und bei SW-Änderungen `sw.js` mit erhöhter
  `CACHE`-Version) im GitHub-Repo ersetzen → Pages baut automatisch. `manifest`
  nur bei Icon-/Namensänderungen.
- **Datentrennung:** alle Baustellen in einer Liste, Spalte `projekt`; Stückliste je
  Baustelle als `LV_<pid>.json`.
- **Stückliste um Gewerk erweitern:** korrigierte Excel → `LV_<pid>.json` neu erzeugen →
  in SharePoint **überschreiben** (Häkchen bleiben). Nie als neue Baustelle importieren.
- **Einmalige Admin-Funktionen (Konsole, eingeloggt + Baustelle offen):**
  `gtsAltbestand()`, `bilderEinordnen(true|false[,limit])`, `ordnerKonsolidieren(true|false)`.

## Sicherheit (Details: `SICHERHEIT.md`)
- Keine Geheimnisse im öffentlichen Code; Schutz über Microsoft-Login + SharePoint-
  Berechtigungen. **Least Privilege:** Graph-Rechte `User.Read` + **`Sites.Selected`**
  (nur die Montagefortschritt-Site). Supabase-Key/Migrationscode entfernt.

## Zusammenarbeit (Git ist die gemeinsame Quelle)
- Gearbeitet wird über das **GitHub-Repo**, nicht über OneDrive. Ablauf: `git pull` →
  Branch → ändern/testen → Pull Request → Merge nach `main` (= live).
  Details: `GIT-WORKFLOW.md`, Onboarding/Architektur: `UEBERGABE-ENTWICKLUNG.md`.
- **PDF-Branding:** `tools/md2pdf_kpc.py` erzeugt aus jeder `.md` ein KPC-PDF.

## Was wo liegt
- **Im Repo** (public): `index.html`, `sw.js`, `manifest.webmanifest`,
  `Vorlage_Stueckliste.xlsx`, alle `*.md`, `tools/`, `.gitignore`.
- **Nur lokal / OneDrive (`.gitignore`):** `cloudflared`, `*.command`, generierte
  `*.pdf`, `supabase-setup.sql`, `_seed-*.json`, `Montagefortschritt1/`
  (Installationspläne, Stücklisten, Quell-Pläne der Projekte).

## Offene optionale Erweiterungen
- Baustelle **löschen** (Umbenennen gibt es bereits).
- Eigene Domain statt github.io.
- Anzeige-Feinschliff (deutsches Dezimalkomma).
- Detail-Anschlüsse je Position (TWk/AW, Steckdosentypen) bei Bedarf manuell.

## Stolpersteine (für später)
- App nur über `http(s)`-URL öffnen, nie als Datei (`file://` → AADSTS500111).
- Jede neue Login-Adresse muss als SPA-Redirect-URI in Entra stehen (AADSTS50011).
- GitHub-Pages-URLs sind case-sensitive (großes „M“).
- Handy: Redirect-Login statt Popup (sonst `block_nested_popups`).
- SharePoint-Foto-Ordner nie manuell umbenennen (Verknüpfungen brechen) – nur über
  Umbenennen + `ordnerKonsolidieren`.
