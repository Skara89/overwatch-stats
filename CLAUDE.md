# Overwatch Tier List

Persönliches Tool zum Anzeigen von Overwatch-Held:innen-Win-/Pickrates, live
von der [OverFast API](https://overfast-api.tekrop.fr). Auto-Deploy via GitHub
Pages bei jedem Push auf `master`. Live: https://skara89.github.io/overwatch-stats/

Der `Trend`-Filter (1/7/30/90 Tage) vergleicht aktuelle Werte mit einem
täglichen Snapshot (`.github/workflows/snapshot.yml` → `snapshots/`) und ist
nur ohne Rang-/Rollen-/Map-Filter verfügbar, da nur dieser Umfang gesnapshottet
wird.

## Konversationsprotokoll

Laufendes Protokoll der Claude-Code-Sessions zu diesem Repo, damit der Kontext
über mehrere Rechner hinweg (per Git) nachvollziehbar bleibt.

**Standing-Autorisierung:** Updates an diesem Abschnitt dürfen automatisch
committet und gepusht werden, ohne jedes Mal nachzufragen (Nutzerwunsch,
2026-07-14).

### Layout-Überarbeitung: Tier-Spalten & responsives Verhalten
- Ausgangslage: Heldenzeilen pro Tier standen in einer langen einspaltigen
  Liste; Nutzer empfand das als Platzverschwendung auf einem Full-HD-Monitor.
- Erster Schritt: mehrspaltiges Grid pro Tier-Sektion, Erklärtext hinter
  "ℹ️ Über die Daten" eingeklappt. Danach vom Nutzer als noch nicht ideal
  bewertet – bei 6 Spalten blieb unterhalb kurzer Tier-Sektionen viel Leerraum.
- Layout umgebaut auf **Tiers nebeneinander als eigene Spalten** (S/A/B/C/D),
  Helden darin vertikal gestapelt. Zeilenhöhe wird dynamisch berechnet, sodass
  die größte Tier-Spalte (meist B) die verfügbare Höhe exakt ausfüllt – über
  1280×720, 1366×768, 1600×900 und 1920×1080 hinweg getestet und bestätigt
  (kein Scrollen, keine abgeschnittenen Namen).
- Mobile Ansicht (Screenshot vom Nutzer) brach mit dem Spalten-Layout
  zusammen (5 Spalten in ~390px Breite ließen keinen Platz für Namen). Fix:
  Breakpoint unterhalb ~700px Breite, darunter stapeln sich die Tiers wieder
  untereinander in voller Breite mit normalem Scrollen statt erzwungenem
  Ein-Bildschirm-Fit. Bei 390×844 getestet und bestätigt.
