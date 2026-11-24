# Wissenssuche ueber ein Betriebslog

**Pruefprinzip:** Vor einem Urteil wird nachgeschlagen, was frueher schon gemessen wurde. Das Beispiel
durchsucht ein **erfundenes** Betriebslog (`beispiel-betriebslog.md`) und rankt die Eintraege nach
Kosinus-Aehnlichkeit.

- Standard: TF-IDF ueber Zeichen-4-Gramme, nur Standardbibliothek, kein Download, laeuft offline
  (daher auch der Test).
- Optional: `sentence-transformers` (mehrsprachiges Modell, laedt beim ersten Mal). `backend="auto"`
  nimmt es, wenn installiert, sonst TF-IDF.

Aufruf: `python3 wissenssuche.py beispiel-betriebslog.md Sicherung schlaegt fehl`
Test: `python3 -m pytest wissenssuche`

Ehrliche Grenze: TF-IDF findet Wortverwandtes, keine Synonyme. Dafuer ist das Embedding-Backend da.

## English summary
Searches a fictional operations log. Default backend: TF-IDF over character 4-grams (stdlib only,
offline). Optional backend: sentence-transformers. Synonyms need the embedding backend.

## Rotprobe
Wird die Sortierung nach Score (Marke `KERNPRUEFUNG-RANG`) entfernt, wird
`test_rangfolge_absteigend` rot. Reproduzierbar mit `python3 rotprobe.py`.
