# Wissenssuche über ein Betriebslog

**Prüfprinzip:** Vor einem Urteil wird nachgeschlagen, was früher schon gemessen wurde. Das Beispiel
durchsucht ein **erfundenes** Betriebslog (`beispiel-betriebslog.md`) und rankt die Einträge nach
Kosinus-Ähnlichkeit.

- Standard: TF-IDF über Zeichen-4-Gramme, nur Standardbibliothek, kein Download, läuft offline
  (daher auch der Test).
- Optional: `sentence-transformers` (mehrsprachiges Modell, lädt beim ersten Mal). `backend="auto"`
  nimmt es, wenn installiert, sonst TF-IDF.

Aufruf: `python3 wissenssuche.py beispiel-betriebslog.md Sicherung schlaegt fehl`
Test: `python3 -m pytest wissenssuche`

Ehrliche Grenze: TF-IDF findet Wortverwandtes, keine Synonyme. Dafür ist das Embedding-Backend da.

## English summary
Searches a fictional operations log. Default backend: TF-IDF over character 4-grams (stdlib only,
offline). Optional backend: sentence-transformers. Synonyms need the embedding backend.

## Rotprobe
Wird die Sortierung nach Score (Marke `KERNPRUEFUNG-RANG`) entfernt, wird
`test_rangfolge_absteigend` rot. Reproduzierbar mit `python3 rotprobe.py`.
