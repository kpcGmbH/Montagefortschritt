# Microsoft-365-Backend einrichten (SharePoint + Graph)

Ziel: Daten bleiben im KPC-Tenant. SharePoint-Liste = Datenbank,
Dokumentbibliothek = Foto-/PDF-Speicher, Zugriff per Microsoft Graph,
Anmeldung per MSAL (KPC-Microsoft-Konto).

---

## Phase 1 – Entra-ID-App registrieren

1. <https://entra.microsoft.com> → **Identity → Applications → App registrations**
   → **New registration**.
2. **Name:** `Montagefortschritt`
3. **Supported account types:** *Accounts in this organizational directory only*
   (Single tenant).
4. **Redirect URI:** Plattform **Single-page application (SPA)** wählen, URI:
   `http://localhost:5173`  (Dev-URL; Produktiv-URL fügen wir in Phase 5 dazu).
5. **Register** klicken.
6. Auf der Übersichtsseite notieren (brauche ich):
   - **Application (client) ID**
   - **Directory (tenant) ID**

### API-Berechtigungen
7. Links **API permissions → Add a permission → Microsoft Graph →
   Delegated permissions**. Hinzufügen:
   - `User.Read`  (meist schon da)
   - `Sites.ReadWrite.All`
   - `Files.ReadWrite.All`
8. **Grant admin consent for KPC** klicken (Häkchen müssen grün werden).

> Strenger geht es später mit `Sites.Selected` (Zugriff nur auf genau eine
> Site) – dafür ist ein Extra-Schritt nötig. Für den Start nehmen wir
> `Sites.ReadWrite.All`.

---

## Phase 2 – SharePoint vorbereiten

### a) Site
Eine SharePoint-**Team-Site** verwenden oder neu anlegen, z.B.
`https://<kpc>.sharepoint.com/sites/Montagefortschritt`.
Den vollständigen Site-Pfad notieren (brauche ich).

### b) Liste „Positionen"
Neue **Blank-Liste** mit Namen **Positionen** und nur **2** zusätzlichen
Spalten (Titel-Spalte bleibt, wird nicht genutzt):

| Spaltenname | Typ                              | Inhalt |
|-------------|----------------------------------|--------|
| `pos`       | Einzelne Textzeile               | Positionsnummer (Schlüssel) |
| `data`      | Mehrere Textzeilen (**Nur-Text**) | gesamter Status als JSON: `{g,m,a,sa,ea,ib,ew,note,fotos,pdfs,restarbeiten,ts,usr}` |
| `projekt`   | Einzelne Textzeile               | Baustellen-ID (für Mehrprojekt-Betrieb). **Idealerweise indizieren.** |

> Die System-Spalte `Modified` dient als „zuletzt bearbeitet" — keine eigene
> Spalte nötig. SharePoint vergibt für „pos"/„data" die internen Namen `pos`
> bzw. `data`. Falls SharePoint stattdessen etwas wie `pos0`/`field_1`
> vergibt: interne Namen kurz mitteilen, dann mappe ich sie im Code.

### c) Bibliothek „Fotos"
Neue **Dokumentbibliothek** namens **Fotos** auf derselben Site. Hier landen
hochgeladene Bilder und PDF-Protokolle.

---

## Was ich von dir brauche (Phase 1+2 erledigt)
1. **Application (client) ID**
2. **Directory (tenant) ID**
3. **Site-URL** (z.B. `https://kpc.sharepoint.com/sites/Montagefortschritt`)
4. Bestätigung, dass Liste **Positionen** + Bibliothek **Fotos** existieren

Damit verdrahte ich die App (Phase 3) und wir testen gemeinsam.
