from services.ameli_api import AmeliAPI
import pytest
A0 = AmeliAPI()

# ─────────────────────────────────────────────
#  get_effectifs
# ─────────────────────────────────────────────

def test_get_effectifs_retourne_une_liste():
    res = A0.get_effectifs("Médecins généralistes", "75", 2022)
    assert isinstance(res, list)

def test_get_effectifs_profession_inexistante():
    res = A0.get_effectifs("ProfessionQuiNExistePas", "75", 2022)
    assert res == []

def test_get_effectifs_departement_inexistant():
    res = A0.get_effectifs("Médecins généralistes", "999", 2022)
    assert res == []

def test_get_effectifs_annee_inexistante():
    res = A0.get_effectifs("Médecins généralistes", "75", 1800)
    assert res == []

def test_get_effectifs_contient_les_bonnes_cles():
    res = A0.get_effectifs("Dermatologues", "75", 2022)
    assert len(res) > 0
    assert "annee" in res[0]
    assert "effectif" in res[0]
    assert "densite" in res[0]

# ─────────────────────────────────────────────
#  get_evolution_effectifs
# ─────────────────────────────────────────────

def test_get_evolution_effectifs_retourne_une_liste():
    res = A0.get_evolution_effectifs("Médecins généralistes", "75")
    assert isinstance(res, list)

def test_get_evolution_effectifs_triee_par_annee():
    res = A0.get_evolution_effectifs("Médecins généralistes", "75")
    annees = [r["annee"] for r in res]
    assert annees == sorted(annees)

def test_get_evolution_effectifs_profession_inexistante():
    res = A0.get_evolution_effectifs("Professionquinexistepas", "75")
    assert res == []

def test_get_evolution_effectifs_contient_les_bonnes_cles():
    res = A0.get_evolution_effectifs("Anesthésistes-réanimateurs", "75")
    assert len(res) > 0
    assert "annee" in res[0]
    assert "effectif" in res[0]
    




    
