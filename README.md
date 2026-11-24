# agenten-pruefprinzip

Drei kleine, eigenständig lauffähige Python-Beispiele dazu, wie ein KI-Agent im Betrieb kontrolliert
wird. Alle Daten sind erfunden, keine externen Dienste nötig (ausser `pytest` zum Testen).

## Das Prüfprinzip in vier Punkten

1. **Belegen statt behaupten.** "Erledigt" gilt erst mit gemessener Uhrzeit und Ausgabe, die den Vollzug zeigt.
2. **Der Mensch entscheidet, der Agent empfiehlt.** Fragen kommen als Optionset: Empfehlung zuerst, mit Prämisse, Wirkung, Klasse.
3. **Nachschlagen vor dem Urteil.** Früher Gemessenes wird gesucht, bevor eine Ursache behauptet wird.
4. **Jede Prüfung muss rot werden können.** Ein Test ohne Rotprobe zählt nicht; Geheimnisse werden abgefangen, bevor sie in einer Ausgabe landen.

| Beispiel | Punkt | Inhalt |
|---|---|---|
| [`rueckfrage/`](rueckfrage) | 2 | Validator für Rückfragen als Optionset |
| [`beleg-waechter/`](beleg-waechter) | 1, 4 | Stop-Hook: weist "erledigt" ohne Beleg und Geheimnisse ab |
| [`wissenssuche/`](wissenssuche) | 3 | Suche über ein erfundenes Betriebslog, offline lauffähig |

Tests: `python3 -m pytest`. Rotprobe: `python3 rotprobe.py` (entfernt je Beispiel die Kernprüfung in einer
Kopie, der Test muss rot werden).

## English summary
Three small, self-contained Python examples of keeping an AI agent under control: (1) proof instead of
claims, (2) the human decides and the agent recommends, (3) look up before judging, (4) every check must be
able to fail. Fictional data, no external services. Run `python3 -m pytest` and `python3 rotprobe.py`.

Lizenz / License: MIT
