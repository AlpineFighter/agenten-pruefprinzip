"""Suche ueber ein Betriebslog. Rangfolge nach Kosinus-Aehnlichkeit.

Backend "tfidf": reine Standardbibliothek, laeuft offline. Zeichen-4-Gramme machen die Suche
robust gegen deutsche Wortformen ("Sicherung" findet "Sicherungslauf").
Backend "embedding": optional, nutzt sentence-transformers, falls installiert
(`pip install sentence-transformers`, laedt beim ersten Mal ein Modell). "auto" waehlt
embedding nur, wenn das Paket vorhanden ist, sonst tfidf.

Search over an operations log, ranked by cosine similarity. TF-IDF over character 4-grams
works offline; sentence-transformers is an optional upgrade.
"""
import math
import re
import sys
from collections import Counter

MINDESTSCORE = 0.15  # darunter nur zufaellige Zeichen-Gramm-Treffer
UMLAUTE = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"})


def eintraege_lesen(text):
    """Teilt ein Markdown-Log an '## '-Ueberschriften in (titel, inhalt)."""
    teile = re.split(r"^## ", text, flags=re.M)[1:]
    out = []
    for t in teile:
        titel, _, rest = t.partition("\n")
        out.append((titel.strip(), rest.strip()))
    return out


def merkmale(text):
    wörter = re.findall(r"[a-z0-9]+", text.lower().translate(UMLAUTE))
    m = Counter()
    for w in wörter:
        w = "_%s_" % w
        if len(w) <= 4:
            m[w] += 1
        for i in range(len(w) - 3):
            m[w[i:i + 4]] += 1
    return m


def _tfidf_vektoren(dokumente, frage):
    docs = [merkmale(d) for d in dokumente]
    n = len(docs)
    df = Counter()
    for d in docs:
        df.update(d.keys())
    idf = {k: math.log((1 + n) / (1 + v)) + 1 for k, v in df.items()}

    def vektor(m):
        v = {k: (1 + math.log(c)) * idf[k] for k, c in m.items() if k in idf}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {k: x / norm for k, x in v.items()}

    return [vektor(d) for d in docs], vektor(merkmale(frage))


def _kosinus(a, b):
    return sum(x * b.get(k, 0.0) for k, x in a.items())


def _scores_tfidf(dokumente, frage):
    vs, q = _tfidf_vektoren(dokumente, frage)
    return [_kosinus(v, q) for v in vs]


def _scores_embedding(dokumente, frage):
    from sentence_transformers import SentenceTransformer  # optional
    modell = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    e = modell.encode(dokumente + [frage], normalize_embeddings=True)
    return [float(sum(x * y for x, y in zip(v, e[-1]))) for v in e[:-1]]


def suche(frage, eintraege, backend="auto", k=3):
    """Liefert bis zu k Treffer [(score, titel, inhalt)], beste zuerst. Score unter MINDESTSCORE faellt weg."""
    dokumente = ["%s\n%s" % (t, i) for t, i in eintraege]
    if backend == "auto":
        try:
            import sentence_transformers  # noqa: F401
            backend = "embedding"
        except ImportError:
            backend = "tfidf"
    scores = _scores_embedding(dokumente, frage) if backend == "embedding" else _scores_tfidf(dokumente, frage)
    treffer = [(s, t, i) for s, (t, i) in zip(scores, eintraege) if s > MINDESTSCORE]
    # KERNPRUEFUNG-RANG
    treffer.sort(key=lambda x: -x[0])
    return treffer[:k]


def main(argv):
    if len(argv) < 3:
        print("Aufruf: wissenssuche.py LOGDATEI FRAGE...", file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as f:
        eintraege = eintraege_lesen(f.read())
    for score, titel, _ in suche(" ".join(argv[2:]), eintraege):
        print("%.2f  %s" % (score, titel))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
