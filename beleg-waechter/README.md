# Beleg-Wächter (Stop-Hook)

**Prüfprinzip:** "Erledigt" ohne Wirkungsnachweis ist eine Vermutung. Der Hook liest das
Claude-Code-Stop-Ereignis (JSON auf stdin mit `transcript_path`, optional `last_assistant_message`
und `stop_hook_active`), nimmt die letzte Agentenantwort und weist sie ab, wenn sie

1. "erledigt", "behoben", "fertig" o. ä. meldet, aber keine gemessene Uhrzeit (HH:MM) **und** keinen
   Befehl oder Ausgabe (`$ ...`, `Befehl:`, `Ausgabe:` oder Codeblock) zeigt, oder
2. ein Geheimnis-Muster enthält (Zugangsschlüssel, Token, privater Schlüssel, `password: ...`).

Die Abweisung ist `{"decision": "block", "reason": ...}` auf stdout, Exit 0. Das Geheimnis wird in
der Begründung nie wiederholt. `stop_hook_active` verhindert Endlosschleifen.

Einbindung in `.claude/settings.json`:

    {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "python3 /pfad/beleg_waechter.py"}]}]}}

Test: `python3 -m pytest beleg-waechter`. Die Testdaten folgen der echten Transkriptform (je
Inhaltsblock eine Zeile), Inhalte sind erfunden.

## English summary
A Claude Code Stop hook. It blocks a final answer that claims "done" without a measured time and a
command or output, or that contains a secret pattern. The secret is never echoed in the reason.

## Rotprobe
Wird die Beleg-Prüfung (Marke `KERNPRUEFUNG-BELEG`) entfernt, wird
`test_erledigt_ohne_beleg_wird_abgewiesen` rot. Reproduzierbar mit `python3 rotprobe.py`.
