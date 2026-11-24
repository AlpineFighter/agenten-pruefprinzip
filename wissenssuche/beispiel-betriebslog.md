# Betriebslog (erfundenes Beispiel)

## 2026-03-02 09:15 Sicherung schlaegt nachts fehl
Der naechtliche Sicherungslauf brach ab, weil das Zielvolume voll war. Alte Staende wurden nach
Aufbewahrungsregel entfernt, danach lief die Sicherung durch. Pruefung: Lauf um 02:00 am Folgetag gruen.

## 2026-03-09 14:40 Zertifikat laeuft in sieben Tagen ab
Die automatische Erneuerung des Zertifikats war wegen eines geaenderten DNS-Tokens stumm gescheitert.
Token ersetzt, Erneuerung manuell ausgeloest, neue Laufzeit 90 Tage gemessen.

## 2026-03-17 11:05 Webdienst antwortet langsam
Antwortzeiten stiegen auf mehrere Sekunden. Ursache war ein Speicherleck im Zwischenspeicher; ein
Neustart des Containers half, das Speicherlimit wurde gesetzt und der Gesundheitscheck verlaengert.

## 2026-03-24 16:20 Festplatte zeigt Fehler im SMART-Wert
Ein Laufwerk meldete wachsende Sektorfehler. Ersatz bestellt, Daten vorsorglich auf das zweite
Laufwerk gespiegelt, Austausch am Wochenende.

## 2026-04-01 08:50 Mailversand der Benachrichtigungen ausgefallen
Der Mailserver lehnte Verbindungen wegen eines abgelaufenen Anwendungspassworts ab. Neues Passwort im
Tresor hinterlegt, Testmail zugestellt.

## 2026-04-08 13:10 Netzwerk-Laufwerk nach Neustart nicht eingehaengt
Nach dem Neustart des Hosts blieb das Netzwerk-Laufwerk leer, Dienste schrieben ins lokale
Verzeichnis. Einhaengen mit Abhaengigkeit vom Netzwerk korrigiert, Waechter fuer den Mountpunkt ergaenzt.
