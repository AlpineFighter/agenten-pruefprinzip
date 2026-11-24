import json
import pathlib
import subprocess
import sys

import beleg_waechter as bw

SKRIPT = pathlib.Path(__file__).parent / "beleg_waechter.py"
# Geheimnisse zur Laufzeit zusammengesetzt, damit kein Scanner die Testdatei meldet.
FALSCHES_TOKEN = "gh" + "p_" + "A1b2" * 9


def transkript(tmp_path, texte):
    """Transkript in der echten Form: je Inhaltsblock eine Zeile, Typ user/assistant."""
    zeilen = [{"type": "user", "message": {"role": "user", "content": "Bitte pruefen"}}]
    zeilen.append({"type": "assistant", "message": {"role": "assistant",
                   "content": [{"type": "thinking", "thinking": "...", "signature": "x"}]}})
    for t in texte:
        zeilen.append({"type": "assistant", "message": {"role": "assistant",
                       "content": [{"type": "text", "text": t}]}})
    p = tmp_path / "t.jsonl"
    p.write_text("\n".join(json.dumps(z) for z in zeilen), encoding="utf-8")
    return p


def hook(ereignis):
    r = subprocess.run([sys.executable, str(SKRIPT)], input=json.dumps(ereignis),
                       capture_output=True, text=True, timeout=30)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout) if r.stdout.strip() else None


def test_erledigt_ohne_beleg_wird_abgewiesen(tmp_path):
    p = transkript(tmp_path, ["Das Problem ist behoben."])
    out = hook({"hook_event_name": "Stop", "transcript_path": str(p), "stop_hook_active": False})
    assert out["decision"] == "block"
    assert "Beleg" in out["reason"]


def test_erledigt_mit_beleg_geht_durch(tmp_path):
    text = "Behoben, gemessen 14:32:\n$ systemctl is-active dienst\nactive"
    p = transkript(tmp_path, ["Erster Absatz.", text])
    assert hook({"hook_event_name": "Stop", "transcript_path": str(p)}) is None


def test_geheimnis_wird_abgewiesen_und_nicht_wiederholt(tmp_path):
    p = transkript(tmp_path, ["Zugang: " + FALSCHES_TOKEN])
    out = hook({"hook_event_name": "Stop", "transcript_path": str(p)})
    assert out["decision"] == "block"
    assert FALSCHES_TOKEN not in out["reason"]


def test_ohne_behauptung_und_ohne_geheimnis_geht_durch():
    assert bw.beurteile("Ich lese zuerst die Konfiguration.") == (False, "")


def test_schleifenschutz(tmp_path):
    p = transkript(tmp_path, ["Alles erledigt."])
    assert hook({"hook_event_name": "Stop", "transcript_path": str(p), "stop_hook_active": True}) is None


def test_letzte_antwort_zaehlt_nicht_die_vorherige(tmp_path):
    p = tmp_path / "t.jsonl"
    alt = {"type": "assistant", "message": {"content": [{"type": "text", "text": "Alles erledigt."}]}}
    neu_user = {"type": "user", "message": {"content": "weiter"}}
    neu = {"type": "assistant", "message": {"content": [{"type": "text", "text": "Ich schaue nach."}]}}
    p.write_text("\n".join(json.dumps(z) for z in (alt, neu_user, neu)), encoding="utf-8")
    assert hook({"transcript_path": str(p)}) is None
