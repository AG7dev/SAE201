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
    
    def get_indicateur_cle(self):
        """Ensemble des indicateurs clé de la page dashboard"""
        indicateur_cle = []
        
        # Age moyen de l'essemble des professionels de sante en 2024
        # Part des femmes moyennes chez les professionels de sante en 2024
        where = ("year(annee)=2024")
        requete = self._requete("demographie-ages-moyens-part-des-femmes-part-des-plus-de-60-ans", 
                                {"select":"AVG(age_moyen_global) as age, AVG(part_femmes) as part",
                                "where":where, "group_by":"annee"})
        indicateur_cle.append(["Age moyen de l'essemble des professionels de sante en 2024",
                               round(requete[0]["age"], 2)])
        indicateur_cle.append(["Part des femmes moyennes chez les professionels de sante en 2024 en pourcentage",
                               round(requete[0]["part"]*100, 2)])
        
        # Densite des professionels de sante, pour 10 000 habitants, en 2024
        where = ("departement!=\"999\" and "
                 "year(annee)=\"2024\" and "
                 "libelle_sexe=\"tout sexe\" and "
                 "libelle_classe_age=\"Tout âge\"")
        requete = self._requete("demographie-effectifs-et-les-densites", {"select":"AVG(densite) as densite",
                                "where":where, "group_by":"annee"})
        indicateur_cle.append(["Densite des professionels de sante, pour 10 000 habitants",
                               round(requete[0]["densite"], 2)])
        
        # Taux de croissance des professionels de sante entre 2023 et 2024
        where = ("departement!=\"999\" and "
                 "(year(annee)=\"2023\" or "
                 "year(annee)=\"2024\") and "
                 "libelle_sexe=\"tout sexe\" and "
                 "libelle_classe_age=\"Tout âge\"")
        requete = self._requete("demographie-effectifs-et-les-densites", {"select":"SUM(effectif) as effectif",
                                "where":where, "group_by":"annee"})
        print("DEBUG")
        print(requete)
        indicateur_cle.append(["Taux de croissance des professionels de sante entre 2023 et 2024",
                               round(((requete[1]["effectif"] - requete[0]["effectif"]) / requete[0]["effectif"]) * 100, 2)])
        
        return indicateur_cle
    
    def get_repartition__specialite(self):
        """Spécialité et leur effectif dans l'annee 2024 (pour un graphique)."""
        where = ("year(annee)=2024 AND "
                 "departement!=\"999\""
                 )
        return self._requete("demographie-exercices-liberaux", 
                             {"select":"SUM(effectif) as effectif", "where":where, 
                              "group_by":"profession_sante", "order_by":"effectif"})
        
    def get_evolution_effectifs_all(self):
        """Effectifs Totaux sur les années disponible  (pour un graphique)."""
        where = ("departement!=\"999\" AND "
                "libelle_classe_age=\"Tout âge\" AND "
                "libelle_sexe=\"tout sexe\""
                )
        return self._requete(
        "demographie-effectifs-et-les-densites",
        {"select": "annee,SUM(effectif) as effectif", "where": where,
        "group_by":"annee", "order_by": "annee", "limit": 100},
        )
    
    def get_repartition_profesionnel(self):
        """Pourcentage des effectifs des professionels de santé ainsi 
        que la valeur totalepour chaque région"""
        where = ("departement!=\"999\" AND "
                "libelle_classe_age=\"Tout âge\" AND "
                "libelle_sexe=\"tout sexe\" AND "
                "year(annee)=2024"
                )
        requete =  self._requete(
        "demographie-effectifs-et-les-densites",
        {"select": "SUM(effectif) as effectif", "where": where,
         "limit": 1},
        )[0].get("effectif", -1)
        where = ("departement!=\"999\" AND "
                "libelle_classe_age=\"Tout âge\" AND "
                "libelle_sexe=\"tout sexe\" AND "
                "year(annee)=2024"
                )
        return self._requete("demographie-effectifs-et-les-densites", 
                             {"select":f"(SUM(effectif) / {requete})*100 as effectif, SUM(effectif) as effectif_totaux", "where":where,
                              "group_by":"libelle_region", "limit":20})
    
    def get_presence_femme(self):
        """Part des femmes dans chaque spécialité en 2024"""
        where = ("year(annee)=2024")
        return self._requete("demographie-ages-moyens-part-des-femmes-part-des-plus-de-60-ans", {
            "select":"AVG(part_femmes) as part_femmes, profession_sante", "group_by":"profession_sante", "order_by":"part_femmes DESC"
            , "limit":100
        })
    
    def get_medecin_patient(self):
        """Nombre moyen de patient unique et dont il est le médecin traitane 
        pour les médecin généraliste"""
        where = ("departement!=\"999\" AND" 
                 "profession_sante=\"Ensemble des médecins généralistes\"")
        return self._requete("patientele", {
            "select":"AVG(patients_medecin_traitant_integer) as patient_traitant, AVG(patients_uniques_integer) as patient_unique",
            where:where, "group_by":"annee"})
    
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