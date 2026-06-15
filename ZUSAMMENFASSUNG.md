# Projekt Montagefortschritt – Zusammenfassung

## Ziel
Nachbau und Weiterentwicklung der KPC-Leistungsfeststellungs-App
(Original: https://carpedings-cpu.github.io/KPC-Berlin-Upbeat/) – mit Umzug
des Backends in den **KPC-Microsoft-365-Tenant** und festem Hosting.

## Was die App ist
Montagefortschritt-/Leistungsfeststellungs-App für Baustellen. Pro Position
abhaken (Geliefert, Montiert, Sanitär, Elektro, Inbetriebnahme, Eingewiesen),
Fotos, Notizen, Restarbeiten, PDF-Protokolle mit Stift-Editor, Berichte/
Exporte (Kundenbericht, Tagesbericht, ZIP). Eine einzige `index.html`,
Bibliotheken (pdf.js, jsPDF, JSZip, MSAL, SheetJS) per CDN.

## Verlauf / Meilensteine

1. **1:1-Kopie** der Original-App als `index.html` erstellt (byte-identisch).
2. **Backend-Entscheidung:** Daten sollen im KPC-Tenant bleiben → Umstieg von
   Supabase auf **SharePoint-Liste + Microsoft Graph** (statt OneDrive, das
   kein Multi-User-Schreiben kann).
3. **Entra-App registriert** (Single-Tenant, SPA), Graph-Rechte
   `User.Read`, `Sites.ReadWrite.All`, `Files.ReadWrite.All` + Admin-Consent.
4. **SharePoint** eingerichtet: Site `…/sites/Montagefortschritt`, Liste
   **Positionen** (Spalten `pos`, `data`, `projekt`), Bibliothek **Fotos**.
5. **Datenschicht umgebaut:** Login via MSAL, Speichern/Laden über Graph,
   Fotos/PDFs in die Bibliothek, Anzeige via Token→Blob.
6. **Mehrprojekt + Stücklisten-Import:** Baustellen-Auswahl, Import-Assistent
   (Excel-Vorlage oder PDF) erzeugt neue Baustellen – jeder kann selbst eine
   Baustelle aus einer Stückliste anlegen.
7. **Echtdaten migriert** aus der alten Supabase-App: **192 Positionen,
   228 Fotos, 16 Notizen, 11 Restarbeiten** (verifiziert über den Zähler
   „Teilweise: 187").
8. **Statuszähler** erweitert: Vollständig / Teilweise / Offen / Gesamt
   (je als Klick-Filter).
9. **Mobiler Zugang** bestätigt (Redirect-Login statt Popup für Handys).
10. **Härtung & Hosting:** eingebettete Stückliste + Migrationscode aus dem
    Quelltext entfernt; veröffentlicht auf **GitHub Pages**.
11. **Offline-Fähigkeit (PWA):** Service Worker + IndexedDB + Outbox/Auto-Sync;
    installierbar als Homescreen-App (Details unten).
12. **Gewerk-Ansicht:** Umschalter Montage/Elektro/Sanitär, gespeist aus neuer
    Spalte `Gewerk` der Stückliste (Details unten).
13. **Corporate Design:** echtes kpc-Logo (Wort-Bildmarke/Volllogo als SVG),
    CD-Farben (Ocker `#895500`, Tan `#d7c1ae`, CD-Grautöne), Schrift durchgängig
    **Roboto Condensed Light** (Details unten).
14. **Mehrprojekt-Feinschliff:** hartkodiertes „Berlin Upbeat“ entfernt – Titel,
    Berichte, Dok.-Nr. und ZIP-Namen nutzen den **aktuellen Projektnamen**.
15. **Benutzername aus Anmeldung:** statt Kürzel der echte Name aus dem
    Microsoft-Konto (voll in Berichten/Kopf, kompakt „Max M.“ in der Liste).
16. **Hell-/Dunkel-Modus:** folgt automatisch dem Geräte-Modus, plus manueller
    Umschalter Auto/Hell/Dunkel im Kopf (Details unten).
17. **Anschlussarbeiten aus Installationsplänen:** Gewerk M/S/E für Upbeat aus den
    PDF-Etagenplänen abgeleitet, geprüft und in die Stückliste übernommen – **alle
    Etagen** (388 Positionen) klassifiziert (Details unten).
18. **Ausführer-Zuordnung:** pro Sitzung wählbar **eigene Monteure** (Name) oder
    **Fremdfirma** (z.B. GTS); wird je Häkchen mitgestempelt. Bestehende Upbeat-
    Anschlussarbeiten einmalig der Fa. **GTS** zugeschrieben (Details unten).
19. **Foto-/Protokoll-Ablage in Ordnern:** neue Dateien automatisch nach
    **Baustelle / Etage / Anlage**; Altbestand per einmaliger Migration einsortierbar
    (Details unten).

## Aktueller Stand: PRODUKTIV ✅
- **Live-URL:** https://kpcgmbh.github.io/Montagefortschritt/  (großes „M",
  Adresse ist case-sensitive)
- Login (Microsoft, nur KPC-Konten) + Datenzugriff funktionieren auf
  **Desktop und Handy**.
- Der Trupp braucht nur diese URL – kein localhost, kein Tunnel.

## Wichtige Eckdaten
- **Entra-App:** „Montagefortschritt“, Client-ID `68f89557-eef9-4481-b45c-29919ed7b55d`,
  Tenant-ID `cba1b1fc-4a80-4da1-a7f1-e3e4614056eb`.
- **Redirect-URIs (Entra → Authentifizierung → SPA):**
  `https://kpcgmbh.github.io/Montagefortschritt/` (produktiv); optional
  `http://localhost:5173` (Entwicklung).
- **SharePoint:** Site `https://kpcfulda.sharepoint.com/sites/Montagefortschritt`,
  Liste „Positionen“, Bibliothek „Fotos“.
- **GitHub:** Repo `kpcgmbh/Montagefortschritt` (public), Dateien `index.html`,
  `sw.js`, `manifest.webmanifest`.

## Offline-Fähigkeit (PWA) ✅
Die App funktioniert auf der Baustelle auch **ohne/mit schlechtem Netz** und ist
als **Icon auf dem Homescreen** installierbar (Standalone, ohne Browser-Leiste).
- **Service Worker (`sw.js`):** cacht App-Shell + CDN-Bibliotheken → App startet
  offline. Graph/Login/SharePoint werden NIE gecacht (immer live).
- **Lokaler Speicher (IndexedDB):** letzter Stand (Positionen, Stückliste, Fotos)
  bleibt offline lesbar.
- **Offline erfassen + Auto-Sync:** Häkchen, Notizen, Restarbeiten, **Fotos** und
  Protokolle werden offline lokal gespeichert und in eine **Warteschlange (Outbox)**
  gelegt. Sobald Netz da ist, lädt die App alles automatisch zu SharePoint hoch
  (last-write-wins pro Position). Status im Kopf: „✓ Synchron“ / „↻ N wird
  synchronisiert“ / „⚠ Offline · N ausstehend“.
- **Update der Cache-Version:** bei jeder Veröffentlichung mit SW-/Shell-Änderung in
  `sw.js` die Konstante `CACHE` hochzählen (aktuell `kpc-montage-v7`), sonst sehen
  Geräte u.U. die alte Shell. Beim nächsten Online-Aufruf aktualisiert sich der Cache
  automatisch.

## Gewerk-Ansicht (Montage / Elektro / Sanitär) ✅
Oben im Kopf ein Umschalter **Alle | 🔧 Montage | ⚡ Elektro | 🚿 Sanitär**.
- Filtert die Liste auf das gewählte Gewerk (z.B. Elektro-Trupp sieht nur seine
  Positionen); leere Anlagen-Blöcke werden ausgeblendet, die Zähler
  (Vollständig/Teilweise/Offen/Gesamt) beziehen sich auf das Gewerk.
- Jede Position zeigt kleine **Gewerk-Badges**.
- **Datenquelle:** neue Spalte **`Gewerk`** in der Stückliste (`Vorlage_Stueckliste.xlsx`).
  Werte frei, mehrere möglich, z.B. `Montage, Sanitär` / `Montage, Elektro` / `Montage`.
  Erkennung über Schlüsselwörter (montag→M, elektr/strom→E, sanit/wasser→S; auch
  Kürzel `M`/`E`/`S`).
- **Der Umschalter erscheint nur**, wenn die Baustelle Gewerk-Daten hat.
- **Berlin Upbeat ist vollständig klassifiziert** (alle 388 Positionen, alle Etagen) –
  siehe Abschnitt „Anschlussarbeiten aus Installationsplänen".

## Anschlussarbeiten aus Installationsplänen (Upbeat) ✅
Quelle: KPC-Installationspläne je Etage (`Montagefortschritt1/Installationspläne/`,
PDFs `HANKUE_8HC_GTO_<Etage>_…`). Daraus wurde das Gewerk je Position abgeleitet:
- **Sanitär (S):** Wasser-/Abwasser-Übergabepunkte (TWk/TWw/AW) → KPC schließt das Gerät an.
- **Elektro (E):** Elektroanschluss **mit kW-Angabe** = Geräteanschluss; **Möbel-SD /
  Unterverteilung** (KPC liefert+schließt an); **PA-Dose** (KPC erdet). Arbeitssteckdosen
  **ohne** kW werden vernachlässigt. Daten-/Telefondose = bauseits/Fremd, ignoriert.
- **Montage (M):** immer.
- Workflow: Pläne ausgelesen → Excel `Upbeat_Stueckliste_mit_Anschluessen.xlsx` (Spalten
  Gewerk/Quelle) → von Johannes geprüft/korrigiert → in `LV_berlin-upbeat.json` (Feld `gew`)
  übernommen → in SharePoint hochgeladen. **Häkchen blieben erhalten** (Zustand liegt
  getrennt in der Liste „Positionen"; LV nur **in place** ersetzt, kein Neu-Import).
- **Grenze:** Die Pläne setzen Anschlüsse über Bezugslinien ab (Text weit vom Symbol) und
  sind uneinheitlich beschriftet → eine *automatische* Detail-Zuordnung „welcher Anschluss
  zu welcher Position" ist nicht zuverlässig. Verlässlich ist die **Gewerk-Einstufung** (für
  den Filter); Detail-Anschlüsse bei Bedarf manuell.

## Ausführer-Zuordnung: Firma / eigene Monteure ✅
Über den Namen oben rechts wählbar (Dialog „Ausführer wählen"):
- **👷 Eigene Monteure** (Name) oder **🏢 Fremdfirma** (z.B. GTS) – wird bei **jedem
  Häkchen** als Ausführer (`by`) mitgestempelt; in der Liste z.B. „GTS · Datum".
- Badge zeigt 🏢 Firma bzw. ✎ Monteur. Firmen-Erkennung via Liste (Default `GTS`);
  Speicherung in `localStorage` (`kpc_user`, `kpc_user_typ`, `kpc_firmen`).
- Login setzt Standard = MS-Name (eigener Monteur); für Fremdfirma einmal umschalten.
- **Altbestand Upbeat:** die bereits abgehakten **Anschlussarbeiten** (nur Sanitär+Elektro)
  wurden einmalig der Fa. **GTS** zugeordnet (Konsolen-Funktion `gtsAltbestand()`,
  idempotent, nur leere Ausführer; Montage/Lieferung/IBN/Einweisung unberührt).

## Foto-/Protokoll-Ablage in Ordnern (Baustelle / Etage / Anlage) ✅
- **Neue** Fotos, Restarbeiten-Fotos und Protokolle landen automatisch in
  `Baustelle / Etage / Anlage /` (Etage+Anlage aus der Positionsnummer; unzulässige
  Zeichen → „-", Umlaute bleiben). Datei-Referenz kann jetzt ein **Pfad** sein.
- **Altbestand migrieren** (einmalig, online, Konsole): `bilderEinordnen(true)` = Vorschau
  (zeigt was wohin), `bilderEinordnen(false,1)` = Test mit 1 Datei, `bilderEinordnen()` = alle.
  Idempotent, pro Datei fehlertolerant (verschiebt Datei **und** passt internen Verweis an).
- Alte (flache) und neue (Pfad-)Fotos werden beide korrekt geladen.

## Erscheinungsbild / Corporate Design ✅
Angelehnt an den KPC-Styleguide (abgelegt unter
`OneDrive/Dokumente/Corporate Design/kpc_styleguide`).
- **Logo:** echtes kpc-Logo statt Text – Volllogo + Claim auf Login/Projektauswahl,
  kompakte Wort-Bildmarke im Kopf. Als SVG-Data-URI eingebettet (scharf, offline-fähig,
  Negativ-/Weiß-Version auf dunklem Grund).
- **Farben (CD):** Ocker `#895500`, Tan `#d7c1ae`, CD-Grautöne `#676c6e`/`#a8a8a8`/
  `#424242`. Funktionale Status-/Gewerk-Farben (grün/blau/ocker) bleiben erhalten.
- **Schrift:** durchgängig **Roboto Condensed Light** (Google Fonts, per Service
  Worker offline gecacht; global per `*{font-weight:300}` erzwungen). Bodoni Moda
  wurde bewusst wieder entfernt.
- **Hell-/Dunkel-Modus:** automatisch nach Geräte-Einstellung (`prefers-color-scheme`),
  zusätzlich **manueller Umschalter im Kopf** (🌓 Auto / ☀️ Hell / 🌙 Dunkel),
  Wahl pro Gerät gespeichert (`localStorage 'kpc_theme'`); ein Inline-Script im
  `<head>` setzt die Wahl vor dem Rendern (kein Aufblitzen). Umgesetzt über
  semantische CSS-Variablen (`--page/--surface/--text/--line/…`); die „Chrome“-
  Elemente (Kopf, Tabs, Leisten, Overlays) sind in beiden Modi dunkel/markentreu.
- **Benutzername:** kommt automatisch aus der Microsoft-Anmeldung (kein Kürzel-
  Schritt mehr); voll in Berichten/Kopf, kompakt „Max M.“ in der engen Liste;
  über den Namen oben rechts manuell änderbar. Alt-Daten mit Kürzeln bleiben.

## Betrieb & Wartung
- **Neue Baustelle:** einloggen → „➕ Neue Baustelle aus Stückliste“ →
  `Vorlage_Stueckliste.xlsx` (oder PDF) hochladen → Vorschau → anlegen.
  Spalte `Gewerk` ausfüllen, damit der Gewerk-Umschalter greift.
- **App aktualisieren:** `index.html` (und bei SW-Änderungen `sw.js` mit erhöhter
  `CACHE`-Version) lokal ändern → im GitHub-Repo neu hochladen (ersetzen) →
  GitHub Pages baut automatisch neu. `manifest.webmanifest` nur bei Icon-/Namens-
  änderungen erneut hochladen.
- **Datentrennung:** alle Baustellen in einer Liste, Spalte `projekt` trennt
  sie; jede Stückliste liegt als `LV_<projekt>.json` in der Fotos-Bibliothek.
- **Ausführer im Alltag:** vor dem Abhaken oben rechts den Ausführer prüfen/wählen
  (eigener Monteur oder Fremdfirma) – wird je Häkchen gespeichert.
- **Einmalige Admin-Funktionen (Browser-Konsole, eingeloggt + Baustelle offen):**
  `gtsAltbestand()` (Altbestand-Anschlussarbeiten einer Firma zuordnen),
  `bilderEinordnen(true|false[,limit])` (Fotos in Ordner migrieren – erst Vorschau/Test).
- **Stückliste nachträglich um Gewerk erweitern:** korrigierte Excel → `LV_<projekt>.json`
  neu erzeugen → in SharePoint **überschreiben** (Häkchen bleiben). Niemals als neue
  Baustelle importieren (würde den Abhak-Stand löschen).

## Sicherheit
- Im öffentlichen Code stehen **keine Geheimnisse** (Client-/Tenant-ID sind
  öffentlich). Alle Daten sind durch **Microsoft-Login + SharePoint-
  Berechtigungen** geschützt; ohne KPC-Konto kein Zugriff.
- Stücklisten neuer Baustellen liegen in SharePoint, nicht im Quelltext.

## Nur lokal (NICHT ins öffentliche Repo)
`cloudflared`, `mobil-test.command`, `*-setup.md`, `supabase-setup.sql`,
`Vorlage_Stueckliste.xlsx`, `_seed-berlin-upbeat.json` (LV-Backup),
Ordner `Montagefortschritt1/Installationspläne/` (Etagenpläne + Arbeitsdateien
`Upbeat_Stueckliste_mit_Anschluessen.xlsx`, generierte `LV_berlin-upbeat.json`).

## Offene optionale Erweiterungen
- Offline: Anlegen einer **neuen Baustelle** funktioniert weiterhin nur online
  (Stücklisten-Upload). Erfassen/Ändern in bestehenden Baustellen ist offline-fähig.
- Detail-Anschlüsse je Position (TWk/AW, Steckdosentypen) bei Bedarf manuell pflegen
  (automatische Plan-Zuordnung ist nicht zuverlässig – siehe Grenze oben).
- Ausführer/Migration als Buttons statt Konsole (auf Wunsch).
- Baustelle umbenennen/löschen.
- Eigene Domain statt github.io.
- Anzeige-Feinschliff (deutsches Dezimalkomma).

## Stolpersteine (für später)
- App nur über `http(s)`-URL öffnen, nie als Datei (`file://` → AADSTS500111).
- Jede neue Login-Adresse muss als SPA-Redirect-URI in Entra stehen
  (AADSTS50011 sonst).
- GitHub-Pages-URLs sind case-sensitive (großes „M“).
- Handy: Redirect-Login statt Popup (sonst `block_nested_popups`).
