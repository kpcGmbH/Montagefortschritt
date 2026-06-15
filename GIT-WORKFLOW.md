# Git-Kurzanleitung – Montagefortschritt

Für die Zusammenarbeit am Code. **Goldene Regel: erst ziehen, dann schieben.**
Repo: `kpcgmbh/Montagefortschritt` · Live: https://kpcgmbh.github.io/Montagefortschritt/

---

## Einmalig: Repo holen (Setup)

**Mit GitHub Desktop (empfohlen, ohne Kommandozeile):**
1. GitHub Desktop installieren und mit dem KPC-GitHub-Konto anmelden.
2. *File → Clone repository →* `kpcgmbh/Montagefortschritt` wählen.
3. Als lokalen Ordner **NICHT** den OneDrive-Ordner nehmen – z. B.
   `C:\Projekte\Montagefortschritt` (Windows) bzw. `~/Projekte/Montagefortschritt` (Mac).

**Mit Kommandozeile (Alternative):**
```bash
git clone https://github.com/kpcgmbh/Montagefortschritt.git
```

---

## Jedes Mal, wenn du etwas änderst

### 1. ZIEHEN – aktuellen Stand holen (immer zuerst!)
- GitHub Desktop: oben **„Fetch origin"** → falls Änderungen da sind, **„Pull origin"**.
- CLI: `git pull`

> Damit hast du die letzten Änderungen der/des anderen. Ohne diesen Schritt
> überschreibst du beim Hochladen womöglich ihre/seine Arbeit.

### 2. ÄNDERN
- Datei(en) bearbeiten (auch wenn Claude das für dich macht – die lokale Datei
  muss vorher auf dem neuesten Stand sein, siehe Schritt 1).

### 3. SCHIEBEN – Änderung hochladen
- GitHub Desktop: Änderung links sehen → unten **kurze Beschreibung** eintippen →
  **„Commit to main"** → oben **„Push origin"**.
- CLI:
  ```bash
  git add -A
  git commit -m "Kurz: was geändert wurde"
  git push
  ```

Nach dem Push deployt GitHub Pages **automatisch** – nach ~1 Min ist es live.

---

## Bei größeren Änderungen: über einen Branch + Pull Request
Damit `main` (= live) nie kaputt ist und der/die andere kurz drüberschauen kann:
1. Neuen Branch anlegen (GitHub Desktop: *Current Branch → New Branch*, z. B. `feature/xyz`).
2. Ändern, committen, **„Publish branch"** / `git push -u origin feature/xyz`.
3. Auf GitHub **Pull Request** öffnen → der/die andere klickt *Approve* → **Merge**.

Kleine, unkritische Fixes dürfen direkt auf `main` – aber **immer vorher ziehen** (Schritt 1).

---

## Alte Stände wiederherstellen (Versionierung)

Git speichert jeden Commit als **vollständigen Schnappschuss** – nichts geht verloren.
Da GitHub Pages aus `main` deployt, wird ein zurückgerollter Stand automatisch wieder live.

**Einzelne fehlerhafte Änderung zurücknehmen (der sichere Weg):**
- GitHub (Web): den Commit bzw. Pull Request öffnen → **„Revert"**. Das erzeugt einen
  neuen Commit, der die Änderung sauber rückgängig macht – die Historie bleibt erhalten,
  nichts wird gelöscht.
- GitHub Desktop: *History* → Rechtsklick auf den Commit → *Revert*.
- Nach ~1 Minute ist der alte Zustand wieder live.

**Stabile Versionen klar benennen – Releases/Tags:**
Nach jedem erfolgreich getesteten Deploy auf GitHub: **„Releases" → „Create a new release"**
→ Tag z. B. `v1.3` + kurze Notiz. So springt ihr im Notfall gezielt auf eine benannte
stabile Version zurück, statt euch durch Commit-Kennungen zu suchen.

**Tipp:** Aussagekräftige Commit-Beschreibungen (z. B. „IBN-Regel Sanitär/Elektro") machen
das Wiederfinden alter Stände viel einfacher als „Add files via upload".

## Wenn es mal hakt
- **„Konflikt" beim Pull/Merge:** Ihr habt beide *dieselbe* Stelle geändert. GitHub
  Desktop zeigt die Datei an; die markierten Stellen (`<<<<<<<` … `>>>>>>>`) bereinigen,
  dann committen. Im Zweifel kurz abstimmen, wessen Version gilt.
- **Versehentlich Falsches committet:** noch nicht gepusht? Letzten Commit rückgängig
  (GitHub Desktop: *Undo*). Schon gepusht? Sag Bescheid – das holen wir sauber zurück.
- **Versehentlich `cloudflared`/PDF o. Ä. committet:** gehört per `.gitignore` raus;
  einmalig entfernen mit `git rm --cached <datei>`, dann commit/push.

---

**Merksatz:** *Fetch/Pull → Ändern → Commit → Push.* Nie ohne den ersten Schritt anfangen.
