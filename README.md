# Lernwoerter-App
A self-hosted "Leitner-box" spelling trainer (Lernwörter-App) . Designed for private, non-commercial educational use

# Betrieb & Datenspeicherung
Die Anwendung erkennt beim Start automatisch, ob ein Backend-Server erreichbar ist, und passt die Datenspeicherung entsprechend an.

## App-Icon & Startbildschirm
Das Web-App-Manifest und die Icon-Verweise in `Lernwoerter-app.html` verwenden `Momo_Maus.png`. Bei einer Bereitstellung über HTTPS können Browser das Motiv als Favicon und beim Hinzufügen der App zum Startbildschirm verwenden. Auf iPhone und iPad geht das über „Zum Home-Bildschirm“ in Safari; auf Android über die Browserfunktion zum Installieren oder Hinzufügen. Das Manifest allein erzeugt keine frei konfigurierbaren Smartphone-Widgets. Bei einer Bereitstellung muss `manifest.webmanifest` erreichbar sein und vom Webserver als Manifest-Datei ausgeliefert werden.

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
# Lernlogik (Leitner-Karteikasten)
Das System basiert auf dem Prinzip der verteilten Wiederholung (Spaced Repetition). Jedes Wort durchläuft sechs Stufen:
Box 1: 0 Tage Wartezeit (sofort wieder fällig)
Box 2: 2 Tage Wartezeit
Box 3: 7 Tage Wartezeit
Box 4: 14 Tage Wartezeit
Box 5: 30 Tage Wartezeit
Box 6 (Archiv): Dauerhaft gemeistert (wird im Standard-Filter nicht mehr abgefragt)
# Auswahl & Bewertung
Filter „Alle (Aktiv)“: Es werden ausschließlich Wörter aus den Boxen 1 bis 5 abgefragt, deren Wartezeit abgelaufen ist. Niedrigere Boxen sind im Zufallspool höher gewichtet (Box 1 fünffach bis Box 5 einfach), sodass unsichere Wörter häufiger geübt werden.
Direkter Box-Filter (Box 1–5 oder Archiv): Die Zeitregel wird ausgesetzt. Alle Wörter der gewählten Box können jederzeit gezielt wiederholt werden.
Richtige Antwort: Das Wort rückt eine Box weiter nach vorn (Ausnahme: Wurde zuvor die „1s Hilfe“ genutzt, bleibt das Wort in seiner aktuellen Box).
Falsche Antwort: Das Wort fällt zurück in Box 

# Intensivmodus (🔥)
Der Intensivmodus dient zur gezielten Vorbereitung auf Diktate oder zum Üben besonders schwieriger Lernwörter, ohne den regulären Langzeit-Lernstand zu verfälschen.
Markierung: Wörter lassen sich im Wörterbuch oder direkt auf der Lernkarte mit dem Stern-/Feuer-Symbol für das Intensivtraining markieren.
Sofortige Verfügbarkeit: Im Filter „🔥 Intensiv“ greifen keine Wartezeiten – alle markierten Wörter stehen ohne Pause zur Wiederholung bereit.
Neutraler Lernstand: Während im Intensiv-Filter geübt wird, werden keine Box-Änderungen vorgenommen. Weder rücken Wörter bei richtiger Antwort auf, noch fallen sie bei einem Fehler in Box 1 zurück.
