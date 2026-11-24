# Rueckfrage mit Empfehlung

**Pruefprinzip:** Ein Agent fragt den Menschen nie offen "Was soll ich tun?", sondern legt ein
Optionset vor. Die erste Option ist die Empfehlung. Jede Frage nennt die **Praemisse** (was gilt,
mit gemessener Uhrzeit und Messinstrument), die **Wirkung** und die **Klasse** (reversibel,
aufwendig, unumkehrbar). Der Validator weist Fragen ohne Empfehlung oder ohne Praemisse ab, bevor
der Mensch sie sieht.

Aufruf: `python3 rueckfrage.py < beispiel.json` (Exit 1 und Klartext bei einer unzulaessigen Frage).
Test: `python3 -m pytest rueckfrage`. Keine externen Abhaengigkeiten ausser pytest.

## English summary
An agent never asks an open question. It submits an option set with the recommendation first, the
premise (with measured time and instrument), the impact and a class. The validator rejects
questions without a recommendation or a premise before a human sees them.

## Rotprobe
Wird die Pruefung der Empfehlung (Marke `KERNPRUEFUNG-EMPFEHLUNG`) entfernt, wird
`test_ohne_empfehlung_abgewiesen` rot. Reproduzierbar mit `python3 rotprobe.py` im Wurzelverzeichnis.
