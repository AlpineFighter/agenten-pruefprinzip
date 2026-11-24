import pathlib

import wissenssuche as ws

LOG = pathlib.Path(__file__).parent / "beispiel-betriebslog.md"
EINTRAEGE = ws.eintraege_lesen(LOG.read_text(encoding="utf-8"))


def erster(frage):
    t = ws.suche(frage, EINTRAEGE, backend="tfidf")
    return t[0][1] if t else None


def test_log_wird_in_sechs_eintraege_geteilt():
    assert len(EINTRAEGE) == 6


def test_beste_treffer_je_frage():
    assert "Sicherung" in erster("Warum scheiterte die Sicherung in der Nacht?")
    assert "Zertifikat" in erster("Zertifikat Erneuerung")
    assert "Mailversand" in erster("Mails kommen nicht an, Passwort abgelaufen")
    assert "Netzwerk-Laufwerk" in erster("Mount nach Neustart leer")


def test_wortformen_werden_gefunden():
    assert "Sicherung" in erster("Sicherungen")


def test_rangfolge_absteigend():
    t = ws.suche("Neustart Laufwerk", EINTRAEGE, backend="tfidf", k=6)
    scores = [s for s, _, _ in t]
    assert len(scores) >= 2
    assert scores == sorted(scores, reverse=True)


def test_unverwandte_frage_liefert_nichts():
    assert ws.suche("Pizza Rezept Tomaten", EINTRAEGE, backend="tfidf") == []
