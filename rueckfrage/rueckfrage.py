"""Rueckfrage als Optionset: Ein Agent darf den Menschen nur fragen, wenn die
Frage eine Empfehlung, eine gemessene Praemisse, die Wirkung und eine Klasse
traegt. Der Validator weist alles andere ab.

Question-as-option-set: an agent may only ask the human when the question has a
recommendation, a measured premise, its impact and a class.
"""
import json
import re
import sys

KLASSEN = ("reversibel", "aufwendig", "unumkehrbar")
ZEIT = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


def pruefe(frage):
    """Gibt eine Liste von Fehlern zurueck; leer heisst: Frage ist zulaessig."""
    fehler = []
    if not str(frage.get("titel", "")).strip():
        fehler.append("titel fehlt")
    optionen = frage.get("optionen") or []
    if len(optionen) < 2:
        fehler.append("mindestens zwei Optionen noetig")
    # KERNPRUEFUNG-EMPFEHLUNG
    if not optionen or optionen[0].get("empfehlung") is not True:
        fehler.append("erste Option muss die Empfehlung sein")
    if sum(1 for o in optionen if o.get("empfehlung") is True) > 1:
        fehler.append("genau eine Empfehlung erlaubt")
    prae = frage.get("praemisse") or {}
    # KERNPRUEFUNG-PRAEMISSE
    if not str(prae.get("text", "")).strip():
        fehler.append("praemisse.text fehlt")
    if not ZEIT.match(str(prae.get("gemessen_um", ""))):
        fehler.append("praemisse.gemessen_um muss HH:MM sein")
    if not str(prae.get("instrument", "")).strip():
        fehler.append("praemisse.instrument fehlt")
    if not str(frage.get("wirkung", "")).strip():
        fehler.append("wirkung fehlt")
    if frage.get("klasse") not in KLASSEN:
        fehler.append("klasse muss eine von %s sein" % ", ".join(KLASSEN))
    return fehler


def darstellen(frage):
    """Rendert eine geprueftes Optionset als Text, je Feld eine eigene Zeile."""
    fehler = pruefe(frage)
    if fehler:
        raise ValueError("; ".join(fehler))
    zeilen = [frage["titel"]]
    for i, o in enumerate(frage["optionen"], 1):
        marke = " (Empfehlung)" if o.get("empfehlung") is True else ""
        zeilen.append("%d. %s%s" % (i, o["label"], marke))
    p = frage["praemisse"]
    zeilen.append("Praemisse: %s (gemessen %s, %s)" % (p["text"], p["gemessen_um"], p["instrument"]))
    zeilen.append("Wirkung: %s" % frage["wirkung"])
    zeilen.append("Klasse: %s" % frage["klasse"])
    return "\n".join(zeilen)


def main():
    frage = json.load(sys.stdin)
    fehler = pruefe(frage)
    if fehler:
        print("ABGEWIESEN: " + "; ".join(fehler), file=sys.stderr)
        return 1
    print(darstellen(frage))
    return 0


if __name__ == "__main__":
    sys.exit(main())
