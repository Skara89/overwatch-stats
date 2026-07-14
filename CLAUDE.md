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

### Entstehung: Referenzseite war zu langsam
Wunsch war ein privates Tool für Overwatch-Heldenstatistiken, analog zu einer
vom Nutzer gezeigten Referenzseite, die zu langsam lief. Zentrale Vorfrage:
woher kommen die Rohdaten, da es keine offizielle Blizzard-API dafür gibt.
Die [OverFast API](https://overfast-api.tekrop.fr) (inoffiziell, spiegelt
Blizzards eigene Werte) lieferte Win-/Pick-Rate pro Held, filterbar nach
Plattform, Region, Rolle, Map, Rang und Modus, mit offenem CORS
(`Access-Control-Allow-Origin: *`) – also direkt im Browser nutzbar, ganz ohne
eigenen Server.

### Aufbau als eigenes Projekt
Auf Nachfrage, ob dafür ein neues Projekt angelegt werden muss: ja, eigener
Ordner `overwatch-stats`, getrennt vom PR-Übungsrepo. Auf Wunsch mit
`git init` versioniert. Ergebnis: eine einzelne `index.html` ohne Framework/
Build-Schritt, lädt Live-Daten direkt von der API. Filter (Region, Plattform,
Modus, Rang, Rolle, Map) werden 1h im `localStorage` gecacht. Tier-Einstufung
S–D aus Win-Rate, gewichtet nach Pick-Rate-Konfidenz. Ban-Rate gibt es in der
API nicht, daher weggelassen.

### Nutzung auf einem zweiten PC & GitHub-Repo
Erst eine Anleitung zum manuellen Kopieren der `index.html` (USB/Cloud/E-Mail,
Doppelklick-Start, Fallback `python -m http.server` falls der Browser
`file://` blockiert). Danach auf Wunsch zusätzlich als **privates** GitHub-Repo
angelegt ([github.com/Skara89/overwatch-stats](https://github.com/Skara89/overwatch-stats)),
README um Klon-Anleitung ergänzt (Git-Klon als zweite Option neben manuellem
Kopieren).

### Datenvalidierung gegen Blizzards offizielle Seite
Stichprobenvergleich mit `overwatch.blizzard.com/en-us/rates` verlangt.
Wichtiger Fund dabei: `rq=0` in der Referenz-URL bedeutet "Quick Play – Role
Queue", nicht Competitive (`rq=1`). Beide Modi einzeln mit OverFast
gegengeprüft: **alle 52 Helden, Win-/Pick-Rate exakt bis zur Nachkommastelle
identisch** in beiden Fällen. Fazit: OverFast liefert keine eigenen/
geschätzten Werte, sondern spiegelt Blizzards Live-Daten 1:1 (nur Ban-Rate
fehlt).

### Tier-Sortierung erklärt & erste Anpassungen
Nutzerfrage, warum ein Held mit niedrigerer Win-Rate über einem mit höherer
liegen kann. Erklärung: Score = `winrate × (0,55 + 0,45 × min(pickrate/15,1))`
– ab 15 % Pick-Rate zählt die volle Win-Rate, darunter wird sie wegen kleiner/
unsicherer Stichprobe abgewertet. Tiers = feste Perzentil-Bänder (Top 8 % S,
bis 30 % A, bis 60 % B, bis 85 % C, Rest D) relativ zur aktuellen Filteransicht.

Daraufhin zwei Wünsche umgesetzt:
- **Schalter "Nur Win-Rate"**: deaktiviert die Pick-Rate-Gewichtung, sortiert
  sofort ohne neuen API-Call (localStorage-gespeicherte Einstellung).
- **Map-Filter bereinigt**: nur Maps im Dropdown, die tatsächlich Daten
  liefern. Erste Zählung ergab 37 von 57 (später bei genauerer Prüfung 29 von
  57 valide – frühere Zahl war eigenes Zählfehler). Beim ersten Testlauf
  aller 57 Maps parallel löste das ein API-Rate-Limit aus (`429`) – behoben
  durch gedrosselte Anfragen (max. 4 gleichzeitig) mit automatischem Retry.

### Gewichtungsformel überarbeitet (Wilson-/IMDB-Shrinkage)
Nutzer empfand die Bestrafung niedriger Pick-Raten als zu hart und fragte nach
wissenschaftlichem Hintergrund. Erklärt: die alte Formel war eine willkürliche
lineare Kurve; einschlägig ist "Ranking by average rating with few
observations" (Evan Millers Wilson-Score-Artikel, IMDB-Weighted-Rating:
`score = n/(n+m) × winrate + m/(n+m) × baseline`) – zieht bei wenig Daten
sanft Richtung Basiswert statt hartem Cutoff.

Nutzer-Einwand: da nur die *relative* Pick-Rate vorliegt und Overwatch sehr
viele Spieler hat, dürfte die absolute Stichprobe selbst bei niedriger
Pick-Rate schon groß genug für stabile Werte sein. Antwort: im Kern richtig –
Sample-Size-Korrekturen lohnen sich vor allem, wenn (a) gefilterte Ansichten
(Rang+Map+Rolle kombiniert) die effektive Stichprobe stark schrumpfen lassen,
oder (b) Selection Bias durch One-Trick-Spieler bei Nischenhelden vorliegt
(systematische, nicht zufällige Verzerrung – dafür gibt es ohne echte
Skill-Daten keine saubere Korrektur). Ergebnis: deutlich schwächere Korrektur
umgesetzt (IMDB-Shrinkage mit `SHRINK_M = 3` in
[index.html:216](C:\Claude Code\overwatch-stats\index.html:216)) – bei 0 %
Pick-Rate volle Rückführung auf 50 %, ab ca. 10–15 % Pick-Rate fast
vernachlässigbarer Effekt. Konstante ist jederzeit nachjustierbar.

### Datenzeitraum & Trend-Feature
Nutzerfrage nach dem Zeitraum der Daten: laut Blizzards eigenem FAQ sind es
kumulative Werte seit Patch-Start (kein rollierendes Fenster), Update braucht
bis zu einen Tag zum Nachziehen.

Nutzer verwies auf `owherostats.com`, die echte Zeitfenster (1d/7d/30d/90d/
all) anbietet. Durch Analyse des dortigen JS-Bundles (Chrome-Zugriff war nicht
verbunden, daher direkt im heruntergeladenen HTML/JS gesucht) festgestellt:
das ist nur mit einer eigenen, selbst geführten Zeitreihen-Datenbank möglich
(Blizzard/OverFast liefern nur kumulative Snapshots, keine rohen
zeitgestempelten Match-Daten) – wie die Seite an ihre Rohdaten kommt, war von
außen nicht sicher feststellbar (spekulativ: eigenes Crawling oder
Datenabkommen).

Auf Wunsch, "aus der Veränderung verschiedener Snapshots Rückschlüsse zu
ziehen", eigenes Snapshot-System gebaut, mit zwei offen gelegten
Einschränkungen: (1) aus zwei kumulierten Werten lässt sich kein echtes
"Win-Rate nur der letzten 7 Tage" zurückrechnen (fehlende Unbekannte:
Gesamt-Spielvolumen) – gezeigt wird stattdessen die *Veränderung* seit einem
Snapshot vor N Tagen (z. B. "▲ +1,2 Pp WR (7T)"), nicht ein exaktes Zeitfenster.
(2) Repo musste dafür öffentlich sein, da `raw.githubusercontent.com` bei
privaten Repos ohne Auth 404 liefert – **Sichtbarkeit ändern ist eine
Repo-Einstellung, die bewusst nicht automatisiert wurde**, Nutzer hat das
selbst in den GitHub-Settings gemacht.

Umsetzung: täglicher GitHub-Actions-Workflow (`snapshot.yml`) zieht Snapshots
für 12 Basis-Kombinationen (3 Regionen × 2 Plattformen × 2 Modi, ungefiltert
nach Rang/Rolle/Map) nach `snapshots/`. End-to-end getestet inkl. manuell
ausgelöstem Workflow-Lauf (Fetch, Commit, Push mit Standard-`GITHUB_TOKEN`
funktionierte ohne weiteres Zutun). Trend-Dropdown im Frontend nur aktiv ohne
Rang-/Rollen-/Map-Filter, da nur dafür Snapshots existieren. Nach Freischaltung
(Repo öffentlich) kurzzeitig CDN-Cache-Verzögerung bei `raw.githubusercontent.com`
(404 trotz `curl` 200) – nach kurzer Wartezeit von selbst behoben, Trend-Anzeige
danach vollständig bestätigt funktionsfähig.

**Offener Punkt, noch nicht entschieden:** Trend pro Filter-Kombination (Rang/
Rolle/Map) wurde als nicht praktikabel eingestuft (alle Filter kombiniert =
11.520 Kombinationen/Tag → ~1–2 Std. Laufzeit, ~29 MB/Tag Repo-Wachstum,
statistisches Rauschen bei engen Filtern). Als Mittelweg wurde vorgeschlagen,
nur **Rolle** zusätzlich ins Snapshot-Raster aufzunehmen (48 Kombinationen,
weiterhin Sekunden-Laufzeit) – die Rückfrage dazu ("Soll ich Rolle (und/oder
Rang) hinzufügen?") wurde vom Nutzer noch nicht beantwortet, das Gespräch ging
stattdessen zum Design-Thema über.

### Hosting via GitHub Pages
Wunsch nach einfachem Hosting mit direkter Verbindung (kein Kopieren zwischen
PCs). GitHub Pages vorgeschlagen (kein neuer Account/Server, Auto-Deploy bei
jedem Push, feste URL) – als Repo-Einstellungsänderung explizit zur
Bestätigung vorgelegt, vom Nutzer bestätigt und aktiviert. Live seither unter
[skara89.github.io/overwatch-stats](https://skara89.github.io/overwatch-stats/).

### README gekürzt
Auf Wunsch komplett neu geschrieben: Englisch, deutlich kürzer (48 → 5 Zeilen),
keine Installationsschritte mehr nötig, da die alten "Datei auf anderen PC
kopieren"-Hinweise durch das Hosting via GitHub Pages obsolet waren.

### Design-Überarbeitung
Nutzer fand das Design zu ähnlich zur ursprünglichen Referenzseite, wollte
aber das dunkle Thema generell beibehalten. Mit der `dataviz`-Skill neu
gestaltet: Tabellenzeilen statt Karten-Grid; geordnete Blau-Skala für Tiers
(hell = S, dunkel = D) statt Ampelfarben, um Rangfolge statt "gut/schlecht"
auszudrücken; divergierender Win-Rate-Balken pro Held (zentriert bei 50 %,
fester Maßstab) statt reinem Text; schlichte beschriftete Dropdowns statt
dunkler Pill-Buttons; normale Systemschrift statt fetter Display-Font. Farben
und Funktion (Filter, Trend, Win-Rate-Schalter) einzeln im Browser
gegengeprüft, bevor committet wurde.

### Platznutzung: Spalten-Layout & dynamische Zeilenhöhe
Rückmeldung: das neue Tabellen-Layout zwang zum Scrollen, viel Bildschirm
blieb leer. Erst auf mehrspaltiges Grid pro Tier-Sektion umgebaut (Erklärtext
hinter "ℹ️ Über die Daten" eingeklappt), dann – da bei 6 Spalten trotzdem
Leerraum unter kurzen Tier-Sektionen blieb – komplett umgestellt auf **Tiers
nebeneinander als eigene Spalten** (S/A/B/C/D), Helden darin vertikal
gestapelt, mit dynamisch berechneter Zeilenhöhe, sodass die größte
Tier-Spalte (meist B) die verfügbare Höhe exakt ausfüllt. Über 1280×720,
1366×768, 1600×900 und 1920×1080 hinweg getestet und bestätigt (kein
Scrollen, keine abgeschnittenen Namen).

### Mobile-Fix
Vom Nutzer per Screenshot gemeldet: das Spalten-Layout brach auf Mobilgeräten
zusammen (5 Spalten in ~390px Breite ließen keinen Platz für Namen). Fix:
Breakpoint unterhalb ~700px Breite, darunter stapeln sich die Tiers wieder
untereinander in voller Breite mit normalem Scrollen statt erzwungenem
Ein-Bildschirm-Fit (der auf Desktop-Monitoren sinnvoll ist, auf einem
Handy-Bildschirm aber nicht). Bei 390×844 getestet und vom Nutzer bestätigt.
