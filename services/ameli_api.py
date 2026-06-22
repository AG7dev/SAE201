# ==================================================
#   SAÉ 2.01 - Développement d'une application WEB
# ==================================================

"""
Service d'accès à l'API externe data.ameli.fr.

Ce module encapsule les appels HTTP vers l'API Ameli afin de :
- récupérer les effectifs de professionnels de santé ;
- obtenir l'évolution des effectifs dans le temps ;
- centraliser la logique de requêtage et la gestion des erreurs.
"""

# Import des requests pour les appels à l'API ameli
import requests

class AmeliAPI:
    """
    Client d'accès à l'API data.ameli.fr.

    Cette classe gère les requêtes HTTP et fournit des méthodes
    spécialisées pour récupérer les données métier liées aux
    professionnels de santé.
    """
    
    # URL de base de l'API Ameli
    BASE_URL = "https://data.ameli.fr/api/explore/v2.1/catalog/datasets"
    
    def __init__(self, timeout=10):
        """
        Initialise le client API.

        Args:
            timeout (int): délai maximal d'attente des requêtes HTTP.
        """
        self._timeout = timeout
        self._session = requests.Session()
    
    def get_effectifs(self, profession, departement_code, annee):
        """
        Récupère les effectifs pour une profession, un département et une année.

        Args:
            profession (str): libellé de la profession.
            departement_code (str): code du département.
            annee (int): année de référence.

        Returns:
            list: liste de dictionnaires contenant année, effectif et densité.
        """
        where = (
        f"profession_sante=\"{profession}\" AND "
        f"departement=\"{departement_code}\" AND "
        f"year(annee)={annee} AND "
        f"libelle_classe_age=\"Tout âge\" AND "
        f"libelle_sexe=\"tout sexe\""
        )
        return self._requete(
        "demographie-effectifs-et-les-densites",
        {"select": "annee,effectif,densite", "where": where, "limit": 100},
        )
    
    def get_evolution_effectifs(self, profession, departement_code):
        """
        Récupère l'évolution des effectifs sur plusieurs années.

        Args:
            profession (str): libellé de la profession.
            departement_code (str): code du département.

        Returns:
            list: données triées par année.
        """
        where = (f"profession_sante=\"{profession}\" AND "
        f"departement=\"{departement_code}\" AND "
        f"libelle_classe_age=\"Tout âge\" AND "
        f"libelle_sexe=\"tout sexe\""
        )
        return self._requete(
        "demographie-effectifs-et-les-densites",
        {"select": "annee,effectif,densite", "where": where,
        "order_by": "annee", "limit": 100},
        )
    
    def get_prescriptions(self, profession, departement_code, annee):
        """Récupère les données de prescriptions médicales selon les critères."""
        # Les variables du filtre correspondent maintenant exactement aux arguments de la méthode
        where = (
            f"profession_sante=\"{profession}\" AND "
            f"departement=\"{departement_code}\"" #AND 
            # f"year(annee)=\"{annee}\"" 
        )

        group_by = (
            f"annee"
        )

        order_by = (
            f"annee"
        )
        
        return self._requete(
            "prescriptions",
            {"select": "year(annee) as annee, AVG(montant_total_prescription_integer) as montant_total, AVG(montant_moyen_prescription_integer) as montant_moyen", "where": where, "group_by": group_by, "order_by": order_by, "limit": 1},
        )
    
    def get_evolution_prescriptions(self, profession, departement_code):
        """Prescriptions sur toutes les années disponibles (pour un graphique)."""
        where = (
            f"profession_sante=\"{profession}\" AND "
            f"departement=\"{departement_code}\""
        )

        group_by = (
            f"annee"
        )

        order_by = (
            f"annee"
        )

        return self._requete(
            "prescriptions",
            {"select": "year(annee) as annee, AVG(montant_total_prescription_integer) as montant_total", "where": where, "group_by": group_by, "order_by" : order_by, "limit": 100},
        )

    def _requete(self, dataset, params):
        """
        Exécute une requête GET vers l'API Ameli.

        Méthode interne centralisant :
        - l'appel HTTP
        - la gestion des erreurs
        - l'extraction des résultats

        Args:
            dataset (str): nom du dataset interrogé.
            params (dict): paramètres de requête API.

        Returns:
            list: résultats JSON ou liste vide en cas d'erreur.
        """
        url = f"{self.BASE_URL}/{dataset}/records"
        try:
            resp = self._session.get(url, params=params, timeout=self._timeout)
            resp.raise_for_status()
            return resp.json().get("results", [])
        except requests.RequestException as e:
            print(f"[AmeliAPI] Erreur : {e}")
            return []