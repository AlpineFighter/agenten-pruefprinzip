"""Rotprobe: Je Beispiel wird die Kernpruefung in einer KOPIE entfernt (reine Textersetzung,
kein Prozess-, Loesch- oder Netzbefehl). Der Test muss rot werden. Das Original bleibt unberuehrt.
Aufruf: python3 rotprobe.py   (Exit 0 nur, wenn alle sieben Mutanten rot sind)"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

HIER = pathlib.Path(__file__).parent
MUTANTEN = [
    ("rueckfrage", "rueckfrage.py",
     'if not optionen or optionen[0].get("empfehlung") is not True:', "if False:"),
    ("beleg-waechter", "beleg_waechter.py", "if BEHAUPTUNG.search(text):", "if False:"),
    ("wissenssuche", "wissenssuche.py", "treffer.sort(key=lambda x: -x[0])", "pass"),
    ("rueckfrage", "rueckfrage.py", 'if not str(prae.get("text", "")).strip():', "if False:"),
    ("rueckfrage", "rueckfrage.py", 'for o in optionen if o.get("empfehlung") is True) > 1:',
     'for o in optionen if o.get("empfehlung") is True) > 99:'),
    ("beleg-waechter", "beleg_waechter.py", "ZEITSTEMPEL.search(text) and BEFEHL_ODER_AUSGABE", "ZEITSTEMPEL.search(text) or BEFEHL_ODER_AUSGABE"),
    ("wissenssuche", "wissenssuche.py", "text.lower().translate(UMLAUTE)", "text.lower()"),
]

ok = True
for ordner, datei, alt, neu in MUTANTEN:
    with tempfile.TemporaryDirectory() as tmp:
        ziel = pathlib.Path(tmp) / ordner
        shutil.copytree(HIER / ordner, ziel, ignore=shutil.ignore_patterns("__pycache__"))
        quelle = ziel / datei
        text = quelle.read_text(encoding="utf-8")
        assert alt in text, "Mutation findet ihre Stelle nicht: %s" % datei
        quelle.write_text(text.replace(alt, neu), encoding="utf-8")
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(ziel)],
                           capture_output=True, text=True)
        rot = r.returncode != 0
        print("%-15s %-22s Mutant %s" % (ordner, alt[:22], "ROT (gut)" if rot else "GRUEN (Pruefung wirkungslos!)"))
        print("   " + (r.stdout.strip().splitlines() or [""])[-1])
        ok = ok and rot
sys.exit(0 if ok else 1)
