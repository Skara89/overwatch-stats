# Overwatch Tier List — Nutzung auf einem anderen PC

Das Tool ist eine einzelne Datei (`index.html`) ohne Installation, ohne Build-Schritt und ohne Zugangsdaten. Es lädt die Heldenstatistiken live über das Internet von der [OverFast API](https://overfast-api.tekrop.fr) — auf dem anderen PC wird also **eine Internetverbindung**, aber **kein GitHub-Zugang** benötigt.

## Option A: Über GitHub

Das Repo liegt (privat) unter [github.com/Skara89/overwatch-stats](https://github.com/Skara89/overwatch-stats). Auf dem anderen PC, mit installiertem [Git](https://git-scm.com/downloads) und einmaligem Login (`gh auth login` oder Git-Anmeldedaten):

```
git clone https://github.com/Skara89/overwatch-stats.git
```

Spätere Änderungen holst du dir mit `git pull` im geklonten Ordner. Dann direkt zu „Tool öffnen“ unten springen.

## Option B: Datei manuell kopieren

### 1. Datei übertragen

Kopiere die Datei `index.html` (aus diesem Ordner `overwatch-stats`) auf den anderen PC. Beliebiger Weg:

- **USB-Stick**: Datei drauf kopieren, am Zielrechner wieder herunterkopieren
- **Cloud-Speicher** (OneDrive, Google Drive, Dropbox): Datei hochladen, am Zielrechner herunterladen
- **E-Mail an dich selbst**: Datei als Anhang senden
- **Netzwerkfreigabe**: falls beide PCs im selben Netzwerk sind, direkt per Windows-Dateifreigabe kopieren

Der Ordnername ist egal — es reicht die eine `.html`-Datei.

## Tool öffnen (beide Optionen)

**Einfachster Weg:** Doppelklick auf `index.html` — sie öffnet sich im Standardbrowser und lädt die Daten direkt.

**Falls das nicht funktioniert** (manche Browser blockieren Live-Datenabfragen von lokal geöffneten Dateien, erkennbar an einer leeren Seite oder einer Fehlermeldung „Fehler beim Laden“):

1. Python installieren, falls nicht vorhanden: [python.org/downloads](https://www.python.org/downloads/) (bei der Installation „Add python.exe to PATH“ anhaken)
2. Eingabeaufforderung/PowerShell im Ordner mit `index.html` öffnen
3. Folgenden Befehl ausführen:
   ```
   python -m http.server 8420
   ```
4. Im Browser öffnen: `http://localhost:8420`

## Hinweise

- Es werden keine Zugangsdaten oder Accounts benötigt — die API ist öffentlich.
- Filter-Einstellungen werden pro Browser 1 Stunde lokal zwischengespeichert (`localStorage`), für schnelleres Umschalten. Das ist rein lokal auf dem jeweiligen PC und muss nicht synchronisiert werden.
- Änderungen am Tool selbst (Code) müssen erneut kopiert werden — es gibt keine automatische Aktualisierung zwischen den PCs.
