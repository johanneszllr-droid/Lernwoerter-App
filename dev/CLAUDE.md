# Hinweise für Claude

## Projekt

Lernwörter-App: Rechtschreib-Lernapp für Grundschulkinder (Leitner-Karteikasten, Diktat auf Papier oder digital). Alles steckt in **einer Datei**, `Lernwoerter-app.html` (HTML, CSS und JavaScript). Die Start-Wörterliste liegt in `lernwoerter-blank.json`. Die Bedienung und Lernsystematik für Eltern ist in `README.md` erklärt.

Veröffentlicht wird über GitHub Pages ohne eigenen Server. Gespeichert wird im `localStorage` des Browsers.

## Arbeitsweise (bitte einhalten)

- **Antworten auf Deutsch** und für Nicht-Programmierer verständlich erklären, mit Beispielen.
- **Immer auf dem Branch `dev` arbeiten.** `main` ist die veröffentlichte Version und wird nur per Pull Request aus `dev` aktualisiert.
- **Erst committen, wenn der Nutzer ausdrücklich zustimmt.** Vorher zeigen, was geändert wurde und wie man es testet.
- **Jede inhaltliche Änderung als eigener Commit** mit deutscher, aussagekräftiger Nachricht (z. B. „Fix: …“). Nicht mehrere Themen in einen Commit packen.
- Ein Push auf `dev` veröffentlicht automatisch die Testversion unter
  `https://johanneszllr-droid.github.io/Lernwoerter-App/dev/Lernwoerter-app.html`.
- Die Versionsnummer steht im Meta-Feld `app-version` am Anfang von `Lernwoerter-app.html` und wird nur auf Wunsch angehoben.

## Testen

- Die App **nicht per `file://` öffnen** (sonst funktionieren Web-Import und Speichern nicht). Stattdessen im Projektordner
  `python3 -m http.server 8000` starten und `http://localhost:8000/Lernwoerter-app.html` öffnen.
- Für automatische Tests eignet sich Chrome headless (`google-chrome --headless=new --dump-dom …`). Node.js ist nicht installiert.
- Nach Änderungen an der Wörterliste: `python3 .claude/scripts/check_wordlist.py` muss ohne Probleme durchlaufen.

## Wörterliste (`lernwoerter-blank.json`)

- Neue Wörter mit dem Agenten **`lernwort-ergaenzer`** ergänzen (`.claude/agents/lernwort-ergaenzer.md`). Dort stehen alle Regeln für Wortart, Artikel, Plural, Emoji und Beispielsatz.
- Wichtigste Regel: Das Lernwort muss **genau in seiner Form** im Beispielsatz stehen, also nicht gebeugt, nicht als Teil eines zusammengesetzten Worts und mit gleicher Groß-/Kleinschreibung. Sonst kann die App es im Satz nicht ausblenden.
- Beim Schreiben das Format erhalten: `json.dumps(daten, indent=2, ensure_ascii=False)` ohne abschließenden Zeilenumbruch.

## Aufbau von `Lernwoerter-app.html`

Das JavaScript ist in Module gegliedert:
`StorageModule` (Laden/Speichern, Import/Export), `EmojiModule` (automatische Emoji-Vorschläge), `FreschModule` (Rechtschreib-Analyse und Hinweise, nutzt Wiktionary), `LeitnerModule` (Boxen und Auswahl), `AudioModule` (Töne), `DailyLearningModule` (Tagesziel), `UIController` (Oberfläche und App-Zustand).

Text, der von außen kommt (Eingaben des Kindes, Wiktionary, importierte Dateien), immer mit `escapeHtml()` bzw. `esc()` absichern, bevor er per `innerHTML` angezeigt wird.

## Bekannte offene Punkte

- `EmojiModule.getForWord` erkennt Wortanfänge zu großzügig (z. B. „hundert“ → 🐕).
- `fehlerZaehler` wird gespeichert, aber nicht hochgezählt.
- Der Lernstand wird nicht zwischen Geräten synchronisiert (nur Backup/Import per JSON).
