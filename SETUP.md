# Eigenes Supabase-Backend einrichten

Die App ([index.html](index.html)) ist eine 1:1-Kopie. Sie zeigt aktuell noch auf
das Backend des Originals. Mit diesen Schritten bekommt sie ein **eigenes,
unabhängiges Backend** (eigene Daten, getrennt vom Original).

## Schritt 1 – Supabase-Projekt anlegen
1. Auf <https://supabase.com> kostenlos registrieren / einloggen.
2. **New project** → Name (z.B. `montagefortschritt`), Datenbank-Passwort
   vergeben, Region **Central EU (Frankfurt)** wählen → **Create**.
3. Warten, bis das Projekt bereit ist (~2 Min).

## Schritt 2 – Datenbank & Storage einrichten
1. Links im Menü **SQL Editor** → **New query**.
2. Inhalt von [supabase-setup.sql](supabase-setup.sql) komplett hineinkopieren.
3. **Run** klicken. Es legt die Tabelle `positionen`, den Storage-Bucket
   `fotos` und alle Zugriffsregeln an.

## Schritt 3 – Zugangsdaten kopieren
Links **Settings** → **API**. Dort findest du:
- **Project URL**  (z.B. `https://abcdxyz.supabase.co`)
- **anon public** Key (langer Token unter „Project API keys")

Diese beiden Werte brauche ich – dann trage ich sie in `index.html` ein
(`SB_URL` und `SB_KEY`, Zeile 1076/1077).

## Schritt 4 – Daten
Die Tabelle ist anfangs leer. Die App füllt sie automatisch beim Abhaken von
Positionen (Upsert pro Position). Das Leistungsverzeichnis selbst steckt fest
in der App (`DATA` in index.html) und muss nicht in die Datenbank.

> Hinweis: Der anon-Key ist die einzige Zugangskontrolle. Wer den Link + Key
> hat, kann lesen/schreiben. Für ein internes Bautrupp-Tool ist das üblich.
> Soll es strenger sein, können wir später Login (Supabase Auth) ergänzen.
