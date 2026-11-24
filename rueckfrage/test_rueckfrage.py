import copy
import json
import pathlib

import pytest

import rueckfrage

BEISPIEL = json.loads((pathlib.Path(__file__).parent / "beispiel.json").read_text(encoding="utf-8"))


def test_gueltige_frage_wird_gerendert():
    text = rueckfrage.darstellen(BEISPIEL)
    zeilen = text.splitlines()
    assert zeilen[1].endswith("(Empfehlung)")
    for kopf in ("Praemisse:", "Wirkung:", "Klasse:"):
        assert sum(1 for z in zeilen if z.startswith(kopf)) == 1


def test_ohne_empfehlung_abgewiesen():
    f = copy.deepcopy(BEISPIEL)
    f["optionen"][0]["empfehlung"] = False
    assert any("Empfehlung" in x for x in rueckfrage.pruefe(f))
    with pytest.raises(ValueError):
        rueckfrage.darstellen(f)


def test_empfehlung_nicht_an_erster_stelle_abgewiesen():
    f = copy.deepcopy(BEISPIEL)
    f["optionen"].reverse()
    assert rueckfrage.pruefe(f)


def test_ohne_praemisse_oder_messzeit_abgewiesen():
    f = copy.deepcopy(BEISPIEL)
    del f["praemisse"]
    assert rueckfrage.pruefe(f)
    g = copy.deepcopy(BEISPIEL)
    g["praemisse"]["gemessen_um"] = "gestern"
    assert any("gemessen_um" in x for x in rueckfrage.pruefe(g))


def test_unbekannte_klasse_abgewiesen():
    f = copy.deepcopy(BEISPIEL)
    f["klasse"] = "egal"
    assert rueckfrage.pruefe(f)
