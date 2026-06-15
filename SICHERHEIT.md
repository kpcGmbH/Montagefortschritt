# Sicherheit – Montagefortschritt

Stand: 2026-06-15

## Überblick

- **Anmeldung:** Microsoft 365 / Azure AD (MSAL, PKCE, kein Client-Secret).
  Single-Tenant (`tenantId cba1b1fc-4a80-4da1-a7f1-e3e4614056eb`) → nur KPC-Konten.
- **Daten:** ausschließlich in SharePoint `/sites/Montagefortschritt`
  (Liste „Positionen" + Bibliothek „Fotos"). Zugriffskontrolle = SharePoint-Rechte.
- **Übertragung:** durchgehend HTTPS. Keine echten Geheimnisse im Code
  (`clientId`/`tenantId` sind bei SPA-Logins öffentlich und unkritisch).
- **Code:** Single-File-PWA auf öffentlichem GitHub Pages → Quelltext einsehbar.
  Ohne gültiges KPC-Konto + Site-Berechtigung jedoch wertlos (Daten bleiben geschützt).
  Fremde Domain kann den Login nicht abschließen (Redirect-URI in Azure fixiert).

## Erledigt (2026-06-15)
- Alter Supabase-anon-Key + `migrateMensa()` + `dataURItoBlob()` aus `index.html`
  entfernt (Mensa-Migration war abgeschlossen). Irreführenden Kommentar bereinigt.

## ✅ ERLEDIGT (2026-06-15): Graph-Berechtigungen auf Sites.Selected eingeengt
- `GRAPH_SCOPES` in index.html = `['User.Read','Sites.Selected']` (deployed).
- Azure: App `68f89557-…` mit delegiertem `Sites.Selected` + Admin-Zustimmung.
- Site-Freigabe (write) nur für `/sites/Montagefortschritt` gesetzt (Graph
  `POST /sites/{id}/permissions`, 201). Site-ID:
  `kpcfulda.sharepoint.com,cc689847-31ac-45ab-9013-1ccdb9a270a0,7402b249-9a82-4250-a85e-4475ba31cb60`.
- `Sites.ReadWrite.All` + `Files.ReadWrite.All` aus konfigurierten Berechtigungen
  entfernt. Funktionstest (Liste/Häkchen/Foto/PDF) bestanden.
- Optional offen: die zwei `.All`-Grants unter „Weitere gewährte" endgültig widerrufen.

## (Historie) Empfehlung Graph-Berechtigungen einengen — umgesetzt s. o.

**Ist-Zustand** (`index.html`, Zeile ~1528):
```js
const GRAPH_SCOPES = ['User.Read','Sites.ReadWrite.All','Files.ReadWrite.All'];
```
→ Token darf *alle* SharePoint-Sites und Dateien, die der Nutzer erreichen kann.
Die App braucht aber nur **eine** Site.

**Ziel:** `Sites.Selected` (delegiert) — Token kann nur Sites berühren, für die die
App-Registrierung ausdrücklich freigeschaltet wurde. Effektiver Zugriff =
Schnittmenge aus App-Freigabe (nur diese Site) UND Nutzer-Rechten in SharePoint.

### Cutover-Reihenfolge (Azure ZUERST, dann Code) — sonst 403

1. **Azure – API-Berechtigung hinzufügen**
   - Azure Portal → App-Registrierungen → App `68f89557-eef9-4481-b45c-29919ed7b55d`
     → *API-Berechtigungen* → *Berechtigung hinzufügen* → Microsoft Graph →
     **Delegiert** → `Sites.Selected` → **Administratorzustimmung erteilen**.
   - `User.Read` behalten. `Sites.ReadWrite.All` + `Files.ReadWrite.All` (vorerst
     noch nicht entfernen — erst nach erfolgreichem Test, siehe Schritt 4).

2. **App für genau diese eine Site freischalten** (einmalig, durch Admin).
   PnP PowerShell:
   ```powershell
   Connect-PnPOnline -Url https://kpcfulda.sharepoint.com/sites/Montagefortschritt -Interactive
   Grant-PnPAzureADAppSitePermission `
     -AppId 68f89557-eef9-4481-b45c-29919ed7b55d `
     -DisplayName "Montagefortschritt" `
     -Site https://kpcfulda.sharepoint.com/sites/Montagefortschritt `
     -Permissions Write
   ```
   Alternativ per Graph: `POST /sites/{siteId}/permissions` mit Rolle `write`
   und der App als `grantedToIdentities`.

3. **Code umstellen** (`index.html`, Zeile ~1528):
   ```js
   const GRAPH_SCOPES = ['User.Read','Sites.Selected'];
   ```
   Deployen (index.html). Drive-/Listenzugriff über `/sites/{id}/...` funktioniert
   unter `Sites.Selected` weiter, da die Bibliothek zur Site gehört.

4. **Testen**, dann aufräumen: Liste laden, Häkchen setzen, Foto hochladen/öffnen,
   PDF erzeugen. Wenn alles läuft → in Azure `Sites.ReadWrite.All` und
   `Files.ReadWrite.All` aus den API-Berechtigungen **entfernen** (Least Privilege).

### Rollback
Bei Problemen `GRAPH_SCOPES` zurück auf die drei alten Scopes setzen, redeployen;
die `.All`-Berechtigungen in Azure bestehen ja noch bis Schritt 4.

## Weitere mögliche Härtung (optional)
- **Rollen in der App:** aktuell hat jeder mit Site-Zugang Vollschreibrecht.
  Feinsteuerung über SharePoint-Berechtigungsgruppen (Lesen vs. Schreiben).
- **Privates Repo** für den Quelltext (GitHub Pages aus privatem Repo benötigt
  GitHub Team/Enterprise). Daten sind nicht im Repo, also nur Code-Sichtbarkeit.
