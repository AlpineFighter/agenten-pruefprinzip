"""Beleg-Waechter als Claude-Code-Stop-Hook.

Liest das Hook-Ereignis als JSON von stdin. Das Ereignis traegt `transcript_path`
(JSONL-Transkript); optional `last_assistant_message` (Text) und `stop_hook_active`.
Weist die letzte Agentenantwort ab (JSON {"decision": "block", "reason": ...}), wenn
sie
  1. "erledigt" o. ae. meldet, ohne gemessenen Beleg (Uhrzeit HH:MM plus Befehl/Ausgabe), oder
  2. ein Geheimnis-Muster enthaelt.
Das Geheimnis selbst wird in der Begruendung nie wiederholt.

Stop hook: blocks a final agent answer that claims "done" without a measured proof
(time plus command/output) or that contains a secret pattern.
"""
import json
import re
import sys

BEHAUPTUNG = re.compile(
    r"\b(erledigt|fertig|abgeschlossen|behoben|umgesetzt|done|completed|fixed)\b", re.I)
ZEITSTEMPEL = re.compile(r"\b([01]\d|2[0-3]):[0-5]\d(:[0-5]\d)?\b")
BEFEHL_ODER_AUSGABE = re.compile(r"(^\$ |^Befehl:|^Ausgabe:|^```)", re.M)
GEHEIMNISSE = [
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{20,}"),
    re.compile(r"(?i)\b(passwort|password|token|secret|api[_-]?key)\b\s*[:=]\s*[^\s<]{8,}"),
]


def antwort_aus_transkript(pfad):
    """Text der letzten Agentenantwort: alle Textbloecke der Assistenten-Zeilen
    nach der letzten Benutzer-Zeile. Das Transkript schreibt je Inhaltsblock
    (thinking, text, tool_use) eine eigene Zeile."""
    texte = []
    with open(pfad, encoding="utf-8") as f:
        for zeile in f:
            try:
                e = json.loads(zeile)
            except ValueError:
                continue
            if e.get("type") == "user":
                texte = []
            elif e.get("type") == "assistant":
                inhalt = (e.get("message") or {}).get("content")
                if isinstance(inhalt, str):
                    texte.append(inhalt)
                for block in inhalt or []:
                    if isinstance(block, dict) and block.get("type") == "text":
                        texte.append(block.get("text", ""))
    return "\n".join(texte)


def beurteile(text):
    """Gibt (abweisen, grund) zurueck."""
    for muster in GEHEIMNISSE:
        if muster.search(text):
            return True, "Die Antwort enthaelt ein Geheimnis-Muster. Entfernen, durch <REDACTED> ersetzen."
    # KERNPRUEFUNG-BELEG
    if BEHAUPTUNG.search(text):
        if not (ZEITSTEMPEL.search(text) and BEFEHL_ODER_AUSGABE.search(text)):
            return True, ("Erledigt ohne Beleg gemeldet. Belegen: gemessene Uhrzeit (HH:MM) "
                          "und Befehl oder Ausgabe, die den Vollzug zeigt.")
    return False, ""


def main():
    ereignis = json.load(sys.stdin)
    if ereignis.get("stop_hook_active"):
        return 0  # Schleifenschutz: nach einer Abweisung nicht erneut abweisen
    text = ereignis.get("last_assistant_message")
    if not isinstance(text, str):
        text = antwort_aus_transkript(ereignis["transcript_path"])
    abweisen, grund = beurteile(text)
    if abweisen:
        print(json.dumps({"decision": "block", "reason": grund}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
