# Lernwoerter-App
A self-hosted "Leitner-box" spelling trainer (Lernwörter-App) . Designed for private, non-commercial educational use

## Versionierung
Die Versionsnummer wird manuell am Anfang von `Lernwoerter-app.html` im Meta-Feld `app-version` gepflegt. Ändere dort zum Beispiel `1.1.0` auf `1.1.1`, wenn du die Patch-Version erhöhen möchtest. Fehlerkorrekturen erhöhen üblicherweise die letzte Zahl, neue rückwärtskompatible Funktionen die mittlere Zahl und inkompatible Änderungen die erste Zahl.

Der GitHub-Workflow erzeugt beim Push auf `dev` automatisch `build-info.json` mit Commit-Titel, Kurz-Hash und Build-Zeitpunkt. Die App zeigt den Commit-Titel zusätzlich zur manuell gesetzten Version an. GitHub-Releases und Tags sind für die Versionsanzeige oder die Synchronisierung nach `main/dev` nicht erforderlich.

# Betrieb & Datenspeicherung
Die Anwendung erkennt beim Start automatisch, ob ein Backend-Server erreichbar ist, und passt die Datenspeicherung entsprechend an.

## App-Icon & Startbildschirm
Das Web-App-Manifest und die Icon-Verweise in `Lernwoerter-app.html` verwenden `Momo_Maus.png`. Das Manifest kennzeichnet das Symbol auch als „maskable“, damit Android es für den runden Startbildschirm-Kreis bis zum Rand darstellen kann. Bei einer Bereitstellung über HTTPS können Browser das Motiv als Favicon und beim Hinzufügen der App zum Startbildschirm verwenden. Auf iPhone und iPad geht das über „Zum Home-Bildschirm“ in Safari; auf Android über die Browserfunktion zum Installieren oder Hinzufügen. Das Manifest allein erzeugt keine frei konfigurierbaren Smartphone-Widgets. Bei einer Bereitstellung muss `manifest.webmanifest` erreichbar sein und vom Webserver als Manifest-Datei ausgeliefert werden.

## Server-Modus (z. B. Raspberry Pi im Heimnetz)
Funktionsweise:
Beim Laden der Seite fragt die App den Endpunkt GET /api/words ab. Ist dieser erreichbar, wechselt die App in den Server-Modus (grünes Status-Badge).
Speicherung: Jede Änderung am Wörterbuch oder Lernstand wird per POST /api/words direkt an den Server gesendet und dort zentral gespeichert.
Vorteil: Lernstände und Wörterlisten sind geräteübergreifend (Tablet, Smartphone, PC) im gesamten Netzwerk synchron.
## 2. Lokal-Modus (Standalone im Browser)
Funktionsweise: Wird kein Server gefunden (z. B. beim direkten Öffnen der index.html als Datei oder auf einem statischen Webhost), schaltet die App automatisch in den Lokal-Modus (gelbes Status-Badge).
Speicherung: Alle Wörter und Lernstände werden im localStorage des jeweiligen Browsers abgelegt.

# Datensicherung: 
Über den Tab „Daten & Info“ lässt sich der gesamte Bestand jederzeit als JSON-Datei exportieren und auf anderen Geräten wieder importieren.
Der Web-Import lädt `lernwoerter-blank.json` aus demselben Verzeichnis wie die App; die Datei muss dort bereitgestellt werden. Lernstände lassen sich separat zurücksetzen. Im Server-Modus wirkt sich das auf alle verbundenen Geräte aus. Das Leeren des Wörterbuchs ist nur im Lokal-Modus möglich und wird mehrfach bestätigt.
Im Tab „Wörterbuch“ filtert das Suchfeld live nach Wort, Artikel und Plural; Sortierung und Gruppierung bleiben dabei erhalten.
# Lernlogik (Leitner-Karteikasten)
Das System basiert auf dem Prinzip der verteilten Wiederholung (Spaced Repetition). Neue Wörter liegen zunächst im Wörterspeicher (Box 0). Die Lernboxen funktionieren so:
Wörterspeicher (Box 0): Warteschlange für neue Wörter; richtige Antworten verschieben ein Wort noch nicht in Box 1.
Der Wörterspeicher ist über einen eigenen Navigationspunkt erreichbar. Pfeile neben den Wörtern ändern dauerhaft ihre Reihenfolge; das oberste wartende Wort rückt zuerst nach.
Box 1: 0 Tage Wartezeit (sofort wieder fällig)
Box 2: 2 Tage Wartezeit
Box 3: 7 Tage Wartezeit
Box 4: 14 Tage Wartezeit
Box 5: 30 Tage Wartezeit
Schatztruhe (Box 6): Dauerhaft gemeistert (wird im Standard-Filter nicht mehr abgefragt)
# Auswahl & Bewertung
Filter „Alle (Aktiv)“: Es werden nur fällige Wörter aus Box 1 bis 5 abgefragt. Wörter aus dem Wörterspeicher werden erst gelernt, wenn sie bei freiem Platz nach Box 1 nachrücken. Niedrigere Lernboxen sind im Zufallspool höher gewichtet, sodass unsichere Wörter häufiger geübt werden.
Direkter Box-Filter (Box 1–5 oder Schatztruhe): Die Zeitregel wird ausgesetzt. Alle Wörter der gewählten Box können jederzeit gezielt wiederholt werden.
Box 1: Aus dem Wörterspeicher werden Wörter nachgerückt, solange weniger als 15 Wörter in Box 1 liegen. Ein korrektes Wort rückt von Box 1 nach Box 2; danach wird der Speicher bei Bedarf bis auf 15 Wörter aufgefüllt. Rückläufer aus höheren Boxen können Box 1 über 15 Wörter anwachsen lassen; dann wird nichts aus dem Speicher nachgezogen.
Richtige Antwort: Das Wort rückt ab Box 1 eine Box weiter (Ausnahme: Wurde zuvor die „1s Hilfe“ genutzt, bleibt es in seiner aktuellen Box). Wörter im Wörterspeicher bleiben dort, bis ein Platz in Box 1 frei wird.
Falsche Antwort: Wörter aus Box 2 oder höher fallen zurück in Box 1. Wörter in Box 1 beziehungsweise im Wörterspeicher bleiben in ihrer aktuellen Box.

# Intensivmodus (🔥)
Der Intensivmodus dient zur gezielten Vorbereitung auf Diktate oder zum Üben besonders schwieriger Lernwörter, ohne den regulären Langzeit-Lernstand zu verfälschen.
Markierung: Wörter lassen sich im Wörterbuch oder direkt auf der Lernkarte mit dem Stern-/Feuer-Symbol für das Intensivtraining markieren.
Sofortige Verfügbarkeit: Im Filter „🔥 Intensiv“ greifen keine Wartezeiten – alle markierten Wörter stehen ohne Pause zur Wiederholung bereit.
Neutraler Lernstand: Während im Intensiv-Filter geübt wird, werden keine Box-Änderungen vorgenommen. Weder rücken Wörter bei richtiger Antwort auf, noch fallen sie bei einem Fehler in Box 1 zurück.
