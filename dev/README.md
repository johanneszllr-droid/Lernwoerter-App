# Lernwörter-App

Eine selbst gehostete Rechtschreib-Lernapp mit digitalem und Papier-Lernmodus, Leitner-Karteikasten, Wörterbuch und Wörterspeicher. Die App ist für private und nicht kommerzielle Bildungszwecke vorgesehen.

## Überblick

Die App besteht aus vier Bereichen, die über das ☰-Menü geöffnet werden:

- **🎯 Lernen:** Lernkarten, Lernmodi und Wortfilter.
- **📖 Wörterbuch:** Wörter hinzufügen, suchen, bearbeiten, markieren und löschen.
- **📦 Wörterspeicher:** Wartende Wörter suchen und ihre Reihenfolge für das Nachrücken festlegen.
- **⚙️ Settings:** Ton, Tagesziel, Backup, Import und Zurücksetzen.

## Betrieb und Datenspeicherung

Beim Start versucht die App, `GET /api/words` aufzurufen.

- **Server-Modus:** Wenn der Endpunkt erreichbar ist, werden Wörter und Lernstände über `POST /api/words` zentral gespeichert. Änderungen am gemeinsamen Wörterbuch und das Zurücksetzen der Lernstände gelten für alle Geräte, die denselben Server verwenden. Die Anzeige zeigt 🟢.
- **Lokal-Modus:** Wenn kein Server erreichbar ist, speichert die App die Daten unter `leitner_words` im `localStorage` dieses Browsers. Andere Browser und Geräte haben einen getrennten Datenbestand. Die Anzeige zeigt 🟡.

Die Server- und Lokal-Modi verwenden also unterschiedliche Speicherorte. Ein Webserver, der nur die HTML-Datei bereitstellt, ist noch kein Datenspeicher-Backend; ohne erreichbares `/api/words` verwendet die App den lokalen Speicher.

Wird weder ein gespeicherter Bestand noch ein Serverbestand gefunden, legt die App drei Beispielwörter an. Die vollständige Start-Wortliste kann über **Settings → Web-Import** aus `lernwoerter-blank.json` geladen werden.

### Bereitstellung als Web-App

`manifest.webmanifest` und die Icon-Verweise verwenden `Momo_Maus.png`. Bei Bereitstellung über HTTPS können Browser die App zum Startbildschirm hinzufügen oder installieren. Auf iPhone und iPad erfolgt das in Safari über „Zum Home-Bildschirm“, auf Android über die Installations- oder Hinzufügen-Funktion des Browsers. Das Manifest erzeugt keine Smartphone-Widgets.

## Leitner-Lernlogik

| Bereich | Bedeutung | Wiederholung |
| --- | --- | --- |
| **Wörterspeicher (Box 0)** | Warteschlange neuer oder zurückgestellter Wörter; wird im Filter „Alle“ nicht abgefragt. | Kein Zeitintervall |
| **Box 1** | Aktive Wörter, die häufig wiederholt werden. | Sofort fällig |
| **Box 2** | Sicherer beantwortete Wörter. | Nach 2 Tagen |
| **Box 3** | Weiter gefestigte Wörter. | Nach 7 Tagen |
| **Box 4** | Langfristig geübte Wörter. | Nach 14 Tagen |
| **Box 5** | Fast gemeisterte Wörter. | Nach 30 Tagen |
| **Schatztruhe (Box 6)** | Gemeisterte Wörter. | Nicht im Filter „Alle“ enthalten |

Die Fälligkeit wird anhand der vergangenen Zeit seit der letzten Prüfung ermittelt. Wörter ohne Prüfungsdatum sind fällig.

### Nachrücken aus dem Wörterspeicher

- Box 1 wird beim Öffnen des Lernbereichs und nach einem richtigen Wechsel aus Box 1 aus dem Wörterspeicher aufgefüllt, bis sie 15 Wörter enthält.
- Dabei rückt immer das oberste wartende Wort nach.
- Ein Wort aus Box 1 rückt bei richtiger Antwort nach Box 2; danach wird bei Bedarf aufgefüllt.
- Wörter, die aus höheren Boxen wegen einer falschen Antwort nach Box 1 zurückfallen, dürfen die Anzahl in Box 1 über 15 erhöhen. Solange mindestens 15 Wörter in Box 1 liegen, rücken keine neuen Wörter aus dem Speicher nach.
- Neu im Wörterbuch angelegte Wörter starten in Box 0. Auch importierte Wörter ohne übernommenen Lernfortschritt starten im Wörterspeicher.
- Das Zurücksetzen setzt die ersten 15 Wörter der aktuellen Wörterliste auf Box 1 und alle übrigen auf Box 0.

### Auswahl und Bewertung

Im Lernbereich gibt es diese Filter:

- **Alle:** Zufällige Auswahl aus fälligen Wörtern der Boxen 1 bis 5. Box 1 wird stärker gewichtet als höhere Boxen, damit unsichere Wörter häufiger vorkommen.
- **🔥 Intensiv:** Auswahl aus allen als intensiv markierten Wörtern, unabhängig von Box und Fälligkeit. Innerhalb einer Runde werden die markierten Wörter möglichst jeweils einmal ausgewählt und direkt aufeinanderfolgende Wiederholungen vermieden, wenn Alternativen bestehen.
- **Schatztruhe:** Auswahl aus Box 6, unabhängig von Fälligkeiten.

Einzelne Boxen 1 bis 5 haben derzeit keinen eigenen Filterknopf. Die Boxzugehörigkeit steht auf jeder Karte und im Wörterbuch.

- **Richtig:** Ab Box 1 rückt das Wort eine Box weiter. Eine richtige Antwort in Box 5 verschiebt es in die Schatztruhe. Wörter aus Box 0 bleiben im Speicher.
- **Falsch:** Wörter aus Box 2 bis 6 fallen nach Box 1 zurück. Wörter aus Box 1 oder Box 0 bleiben dort.
- **„Tipp“ verwendet:** Wird danach richtig geantwortet, rückt das Wort nicht weiter. Bei einer falschen Antwort gilt weiterhin die normale Rückstufung.
- **Intensivfilter:** Die Box wird weder bei richtiger noch bei falscher Antwort geändert. Das Prüfungsdatum wird dennoch aktualisiert; damit kann sich auch der nächste Fälligkeitszeitpunkt im normalen Filter verschieben.
- Nach jeder bewerteten Antwort wird das Prüfungsdatum aktualisiert. Das Feld `fehlerZaehler` wird in Datensätzen und Backups mitgeführt und beim Zurücksetzen geleert, aber von den aktuellen Antwortfunktionen nicht hochgezählt.

### Lernmodi

**✍️ Stift & Papier**

1. Das Wort wird vorgelesen; die lernende Person schreibt es selbst auf.
2. **Lösung anzeigen** blendet das Wort ein.
3. Rechtschreib-Merkstellen wie Doppelkonsonanten, `ie`, `ck`, `tz`, Dehnungs-h und Auslautverhärtung können im Lösungswort markiert sein.
4. Mit **Leider falsch** oder **Richtig! Weiter** wird die Antwort bewertet.

Der Button **Tipp** blendet das Wort eine Sekunde ein. Wird danach richtig geantwortet, wird es nicht in die nächste Box befördert.

**⌨️ Digital**

1. Das Wort wird vorgelesen und in das Eingabefeld geschrieben.
2. Bei der Prüfung wird die Eingabe mit dem Zielwort verglichen. Ein fehlender führender Artikel (`der`, `die`, `das`, `ein`, `eine`) wird akzeptiert; ein falscher Artikel, eine andere Schreibweise oder Groß-/Kleinschreibung gilt als Fehler.
3. Das Ergebnis zeigt die Lösung, bei richtiger Eingabe „Richtig!“ und bei Fehlern Hinweise zur Schreibweise.
4. **Weiter** bestätigt das Ergebnis und bewertet die Karte.

In beiden Modi wird ein hinterlegter Beispielsatz vor der Auflösung mit `_____` maskiert, wenn das Lernwort oder sein Plural darin erkannt wird. Der Artikel bleibt sichtbar. Beim Auflösen wird der Satz vollständig gezeigt und das erkannte Lernwort grün hervorgehoben. Ist kein Beispielsatz hinterlegt, zeigt die Karte einen entsprechenden Hinweis.

### Vorlesen und Audio

Die Vorlesefunktion nutzt die deutsche Sprachsynthese des Browsers (`de-DE`). Neue Karten werden beim normalen Lernablauf automatisch nach kurzer Verzögerung vorgelesen; **Vorlesen** startet die Wiedergabe erneut. Nach Import, Wortlöschung und Zurücksetzen der Lernstände wird keine Karte automatisch vorgelesen.

Der Ton-Schalter steuert die erzeugten Erfolgs-, Fehler- und Tagesziel-Töne. Das Vorlesen über die Sprachsynthese ist davon unabhängig.

## Intensivtraining

Mit **🔥** im Wörterbuch oder **☆ / ⭐ Intensiv** auf der Lernkarte lässt sich ein Wort für das Intensivtraining markieren. Im Filter **🔥 Intensiv** werden markierte Wörter unabhängig von Box und Fälligkeit abgefragt.

Eine richtige oder falsche Antwort im Intensivfilter ändert die Box nicht. Das Prüfungsdatum wird gespeichert. Die Intensiv-Markierung bleibt bestehen, bis sie wieder ausgeschaltet wird. Die reguläre Boxenverteilung wird in der Statistik nicht durch eine Intensiv-Antwort verändert.

## Tägliche Lerneinheit

- Das Tagesziel ist in **Settings** einstellbar; der Standardwert beträgt fünf Karten.
- Jede abgeschlossene Karte zählt, egal ob die Antwort richtig oder falsch war.
- Der Zähler verwendet das lokale Kalenderdatum des Geräts und beginnt an einem neuen Tag wieder bei null.
- Einstellungen, Fortschritt und der Status der täglichen Feier werden lokal im Browser gespeichert, auch wenn Wörter im Server-Modus verwaltet werden.
- Wird das Tagesziel erreicht, erscheint einmal pro Tag für fünf Sekunden eine Erfolgsmeldung mit Ballons und Konfetti. Bei eingeschaltetem Ton wird dazu ein Erfolgston abgespielt.

## Wörterbuch und Wörterspeicher

### Wörterbuch

- **＋ Hinzufügen:** Erstellt einen neuen Eintrag im Wörterspeicher. Für bekannte Wörter schlägt die App ein passendes Emoji vor; es kann im Bearbeitungsmodus geändert werden. Wird ein Wort mit gleichem Namen bereits gefunden, fragt die App nach einer Bestätigung und aktualisiert dessen Schreibweise.
- Suche durchsucht Wort, Artikel und Plural. Die Sortierung ist alphabetisch oder nach Box; Gruppen lassen sich einzeln oder alle gemeinsam auf- und zuklappen.
- **🔥:** Intensiv-Markierung ein- oder ausschalten.
- **📥:** Ein Wort aus Box 1 in den Wörterspeicher verschieben.
- **↑1:** Ein Wort aus dem Wörterspeicher an die erste Stelle setzen.
- **Edit:** Stammdaten bearbeiten. Über **＋ Mehr** beziehungsweise **− Weniger** werden Artikel, Wortart, Plural, Beispielsatz und Besonderheiten geöffnet oder geschlossen. Während eines Eintrags bearbeitet wird, sind Aktionen anderer Einträge deaktiviert.
- **Löschen:** Entfernt einen Eintrag nach Bestätigung.

Bei falschen digitalen Eingaben markiert die Rechtschreibhilfe erkannte Fehlerstellen und zeigt kurze Hinweise, zum Beispiel zu Großschreibung, Doppelkonsonanten oder `ie`. Für Hinweise zum Verlängern oder Ableiten kann sie Wiktionary abfragen; wenn keine passende Information verfügbar ist, wird ein allgemeiner Hinweis angezeigt.

### Reihenfolge im Wörterspeicher

Die Pfeile **↑** und **↓** verschieben ein wartendes Wort um eine Position; **↑1** setzt es an den Anfang. Die Reihenfolge wird gespeichert und bestimmt, welches Wort beim nächsten Auffüllen nach Box 1 rückt. Die Suche filtert nach Wort, Artikel und Plural, ohne die gespeicherte Reihenfolge zu ändern.

## Settings: Backup, Import und Zurücksetzen

### JSON-Backup

**Backup erstellen** lädt die vollständige Wörterliste einschließlich Stammdaten und Lernfortschritt als JSON-Datei herunter. Der Dateiname lautet `Lernwoerter-Export-JJJJ-MM-TT.json`.

Ein Wortdatensatz enthält typischerweise:

- `id`: eindeutige Kennung
- `stammdaten`: Wort, Artikel, Wortart, Plural, Emoji, Beispielsatz und Besonderheiten
- `userdaten`: Box, letzte Prüfung, Fehlerzähler und Intensiv-Markierung

### Import

Die App nimmt eine JSON-Datei mit einer Wortliste als Array entgegen; ein Objekt mit einem `words`-Array wird ebenfalls akzeptiert.

- **Hinzufügen / Aktualisieren:** Neue Wörter werden ergänzt; gleiche Wörter aktualisieren vorhandene Stammdaten. Vorhandener Lernfortschritt bleibt bestehen, sofern die Importdatei ihn nicht ausdrücklich mitbringt und **Lernfortschritt übernehmen** ausgewählt ist.
- **Komplett ersetzen:** Der vorhandene Wörterbestand wird durch den Import ersetzt.
- Ist **Lernfortschritt übernehmen** nicht markiert, starten importierte Wörter in Box 0 und ohne Intensiv-Markierung.
- Die Start-Wortliste kann über **Web-Import** aus `lernwoerter-blank.json` im selben Verzeichnis wie die App geladen werden.

### Zurücksetzen und Löschen

- **Lernstände zurücksetzen:** Setzt Boxen, letzte Prüfungsdaten und Fehlerzähler zurück; die ersten 15 Wörter der aktuellen Liste kommen in Box 1, alle weiteren in den Wörterspeicher. Im Server-Modus betrifft das alle Geräte. Die Intensiv-Markierung wird dabei nicht entfernt. Die Aktion erfordert zwei Bestätigungen.
- **Lokales Wörterbuch leeren:** Löscht den Bestand dieses Browsers nach zwei Bestätigungen. Im Server-Modus ist diese Funktion deaktiviert.
- Ein einzelnes Wort kann weiterhin im Wörterbuch gelöscht werden.

## Statistik und Statusanzeigen

Unter der Lernkarte zeigt die Statistik die Gesamtzahl sowie die Anzahl der Wörter in Wörterspeicher, Boxen 1 bis 5 und Schatztruhe. In Settings wird zusätzlich die Anzahl der Intensiv-Markierungen angezeigt.

## Symbolverzeichnis

| Symbol | Bedeutung |
| --- | --- |
| **☰ / ×** | Navigation öffnen oder schließen |
| **🎯** | Lernbereich |
| **📖** | Wörterbuch |
| **📦** | Wörterspeicher |
| **⚙️** | Settings |
| **✍️** | Stift-&-Papier-Modus |
| **⌨️** | Digitaler Eingabemodus |
| **☆ / ⭐** | Intensivtraining aus / an |
| **🔥** | Intensiv-Markierung oder Intensivfilter |
| **↑ / ↓** | Wort im Wörterspeicher nach oben oder unten sortieren |
| **↑1** | Wort an die erste Stelle des Wörterspeichers setzen |
| **＋ / −** | Details oder Wortgruppen auf- beziehungsweise zuklappen; beim Hinzufügen steht **＋** für einen neuen Eintrag |
| **📥** | Wort in den Wörterspeicher verschieben oder Daten importieren (abhängig vom Bereich) |
| **📤** | JSON-Backup exportieren |
| **🛡️** | Hinweis zum Schutz und Speicherort des Lernstands |
| **🗑️** | Bereich zum Zurücksetzen oder Löschen |
| **🟢 / 🟡** | Server-Modus / Lokal-Modus |
| **✅ / ❌** | Richtige / falsche Antwort |
| **🎈 🎉 ⭐** | Ballons, Konfetti und Dekoration bei erreichtem Tagesziel |
| **📝** | Allgemeines Ersatzsymbol, wenn für ein Wort kein passendes Emoji gefunden wurde |
| **Wort-Emoji** | Veranschaulicht das Lernwort. Die App ermittelt für bekannte Begriffe automatisch ein Motiv; das Emoji lässt sich im Wörterbuch bearbeiten. |

Die Lernkarten-Aktionsbilder sind **Vorlesen** (`momo-vorlesen.webp`), **Tipp** (`momo-tipp_1.png`), **Lösung anzeigen** (`momo-ergebnis.png`), **Leider falsch** (`momo-fehler-1.png`), **Richtig! Weiter** (`momo-richtig.png`) und im digitalen Ergebnis **Weiter** (`maus_weiter_512-1.webp`).

## Versionierung und Veröffentlichung

Die Versionsnummer wird manuell im Meta-Feld `app-version` am Anfang von `Lernwoerter-app.html` gepflegt. Üblicherweise erhöht eine Fehlerkorrektur die letzte Zahl, eine rückwärtskompatible neue Funktion die mittlere Zahl und eine inkompatible Änderung die erste Zahl.

Der GitHub-Workflow erzeugt beim Push auf `dev` automatisch `build-info.json` mit Commit-Titel, Kurz-Hash und Build-Zeitpunkt. Die App zeigt den Commit-Titel zusammen mit der manuell gepflegten Version an. Für diese Anzeige sind keine GitHub-Releases oder Tags erforderlich.

## Rechtlicher Hinweis

Entwickelt von Johannes Zöllner. Die App ist ein kostenloses Lernprojekt für private und bildungsbezogene Zwecke. Kommerzielle Nutzung, gewerblicher Weiterverkauf oder ungenehmigte Weiterverbreitung des Codes beziehungsweise veränderter Versionen sind laut App-Lizenzhinweis nicht gestattet.

Die Software wird ohne ausdrückliche oder stillschweigende Gewährleistung bereitgestellt. Die Nutzung erfolgt auf eigene Gefahr; der Entwickler übernimmt laut App-Hinweis keine Haftung für Schäden, Datenverluste oder Funktionsfehler.
