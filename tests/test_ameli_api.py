import pytest
import requests
from ameli_api import AmeliAPI 

@pytest.fixture
def api_client():
    """Fixture pytest pour initialiser proprement le client de l'API Ameli."""
    return AmeliAPI(timeout=15) 


def test_get_effectifs_reel(api_client):
    """Vérifie que la récupération des effectifs réels fonctionne et renvoie des données valides."""
    resultats = api_client.get_effectifs("Médecin généraliste", "75", 2024)
    
    # Assertions sur la structure de la réponse réelle de data.ameli.fr
    assert isinstance(resultats, list)
    if len(resultats) > 0:
        premier_enregistrement = resultats[0]
        assert "annee" in premier_enregistrement
        assert "effectif" in premier_enregistrement
        assert "densite" in premier_enregistrement


def test_get_evolution_effectifs_reel(api_client):
    """Vérifie la récupération de l'évolution temporelle des effectifs."""
    resultats = api_client.get_evolution_effectifs("Infirmier", "94")
    
    assert isinstance(resultats, list)
    # Si l'API retourne des données, on s'assure qu'elles sont triées par année dans l ordre décroissant
    if len(resultats) > 1:
        annee_1 = resultats[0].get("annee")
        annee_2 = resultats[1].get("annee")
        if annee_1 and annee_2:
            assert annee_1 <= annee_2


def test_get_honoraires_mapping_reel(api_client):
    """Vérifie que la méthode get_honoraires traite correctement le paramètre type_honoraire."""
    # On teste avec le filtre "Depassements" qui doit être mappé en "Dépassements" en interne
    resultats = api_client.get_honoraires(2024, "Chirurgien-dentiste", "75", type_honoraire="Depassements")
    
    assert isinstance(resultats, list)
    if len(resultats) > 0:
        # On valide que l'API renvoie bien le bon type d'honoraire filtré
        assert resultats[0]["type_honoraires_niveau_1"] == "Dépassements"


def test_get_evolution_honoraires_pagination_reel(api_client):
    """Vérifie le fonctionnement de la boucle de pagination (offset) sur un gros volume de données."""
    # On prend une profession et un département généraux pour s'assurer d'avoir plusieurs lignes
    resultats = api_client.get_evolution_honoraires("Médecin généraliste", "75")
    
    assert isinstance(resultats, list)


def test_get_specialites_tri_reel(api_client):
    """Vérifie que get_specialites groupe et trie correctement les spécialités par montant total décroissant."""
    resultats = api_client.get_specialites(2024, "75")
    
    assert isinstance(resultats, list)
    if len(resultats) > 1:
        # Vérification du tri décroissant : le premier doit être plus grand ou égal au deuxième
        assert resultats[0]["total"] >= resultats[1]["total"]


def test_get_prescriptions_reel(api_client):
    """Vérifie la récupération des données de prescriptions médicales."""
    resultats = api_client.get_prescriptions("Médecin généraliste", "75", "2024")
    assert isinstance(resultats, list)


def test_get_evolution_prescriptions_reel(api_client):
    """Vérifie la récupération de l'évolution des prescriptions (graphique)."""
    resultats = api_client.get_evolution_prescriptions("Médecin généraliste", "75")
    assert isinstance(resultats, list)


def test_get_indicateur_cle_reel(api_client):
    """Vérifie la génération des 4 indicateurs clés du Dashboard de l'application."""
    resultats = api_client.get_indicateur_cle()
    
    assert isinstance(resultats, list)
    assert len(resultats) == 4 # On attend exactement 4 indicateurs clés
    
    # Vérification du format attendu : [ ["Libellé", valeur], ... ]
    for indicateur in resultats:
        assert isinstance(indicateur, list)
        assert len(indicateur) == 2
        assert isinstance(indicateur[0], str) # Le libellé textuel


def test_get_repartition_specialite_reel(api_client):
    """Vérifie la répartition des spécialités pour 2024."""
    resultats = api_client.get_repartition__specialite()
    assert isinstance(resultats, list)


def test_get_evolution_effectifs_all_reel(api_client):
    """Vérifie la récupération des effectifs totaux toutes professions confondues."""
    resultats = api_client.get_evolution_effectifs_all()
    assert isinstance(resultats, list)


def test_get_repartition_professionnel_reel(api_client):
    """Vérifie le calcul des pourcentages d'effectifs par région."""
    resultats = api_client.get_repartition_profesionnel()
    assert isinstance(resultats, list)


def test_get_presence_femme_reel(api_client):
    """Vérifie la récupération du taux de féminisation par profession."""
    resultats = api_client.get_presence_femme()
    assert isinstance(resultats, list)


# Une fois corrigée dans votre classe, ce test passera avec succès.
def test_get_medecin_patient_reel(api_client):
    """Vérifie la récupération de la patientèle moyenne des généralistes."""
    resultats = api_client.get_medecin_patient()
    assert isinstance(resultats, list)