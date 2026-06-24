# ==================================================
#   SAÉ 2.01 - Développement d'une application WEB
# ==================================================

"""
Décorateur de cache pour l'API AMELI.

Ce module fournit une classe permettant d'ajouter un mécanisme
de mise en cache à une instance d'AmeliAPI.

Le cache permet de conserver temporairement les résultats des
requêtes afin d'éviter des appels répétés à l'API pour les mêmes
données, améliorant ainsi les performances de l'application.
"""

# Importations nécessaires
import time
from services.ameli_api import AmeliAPI


class CachedAmeliAPI:
    """
    Enveloppe une instance d'AmeliAPI afin d'ajouter un système de cache.

    Attributes:
        _api (AmeliAPI):
            Instance de l'API sous-jacente utilisée pour effectuer
            les requêtes réelles.

        _duree (int):
            Durée de vie du cache en secondes.

        _memoire (dict):
            Structure contenant les données mises en cache.
            Chaque entrée associe une clé de requête à son résultat
            et éventuellement à sa date d'expiration.
    """

    def __init__(self, api_sous_jacente, duree_vie_seconde=300):
        """
        Initialise le décorateur de cache.

        Args:
            api_sous_jacente (AmeliAPI):
                Instance de l'API à décorer.

            duree_vie_seconde (int, optional):
                Durée de conservation des données dans le cache.
                Par défaut : 300 secondes (5 minutes).
        """
        self._api = api_sous_jacente  # Instance de l'API décorée
        self._duree = duree_vie_seconde
        self._memoire = {}

    def afficher_cache(self):
        """
        Retourne le contenu actuel du cache.

        Returns:
            dict: Dictionnaire contenant toutes les données
            actuellement stockées en mémoire.
        """
        return self._memoire

    def vider_cache(self):
        """
        Supprime l'intégralité des données présentes dans le cache.

        Cette méthode réinitialise complètement la mémoire cache
        afin de forcer les prochains appels à interroger directement
        l'API sous-jacente.
        """
        self._memoire.clear()
    
    def get_effectifs(self, profession, departement_code, annee, rafraichir=False):
        """
        Retourne les effectifs des professionnels de santé.

        La méthode vérifie d'abord si les données demandées sont
        présentes dans le cache. Si ce n'est pas le cas, elle
        interroge l'API AMELI puis mémorise le résultat.

        Args:
            profession (str):
                Libellé de la profession de santé.

            departement_code (str):
                Code du département concerné.

            annee (int):
                Année des données recherchées.

            rafraichir (bool, optional):
                Indique s'il faut rafraîchir le cache.

        Returns:
            list | dict:
                Données d'effectifs retournées par l'API.
        """
        cle = ("effectifs", profession, departement_code, annee)

        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_effectifs(
                profession,
                departement_code,
                annee
            ),
            rafraichir=rafraichir
        )

    def get_evolution_effectifs(self, profession, departement_code, rafraichir=False):
        """
        Retourne l'évolution des effectifs d'une profession.

        Les données sont récupérées depuis le cache si elles sont
        encore valides, sinon un appel à l'API est effectué.

        Args:
            profession (str):
                Libellé de la profession de santé.

            departement_code (str):
                Code du département concerné.
            
            rafraichir (bool, optional):
                Indique s'il faut rafraîchir le cache.

        Returns:
            list | dict:
                Historique ou évolution des effectifs.
        """
        cle = ("evolution_effectifs", profession, departement_code)

        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_evolution_effectifs(
                profession,
                departement_code
            ),
            rafraichir=rafraichir
        )

    def get_prescriptions(self, profession, departement_code, annee, rafraichir=False):
        cle = (
            "prescriptions",
            profession,
            departement_code,
            annee
        )

        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_prescriptions(
                profession,
                departement_code,
                annee
            ),
            rafraichir=rafraichir
        )


    def get_evolution_prescriptions(self, profession, departement_code, rafraichir=False):
        cle = (
            "evolution_prescriptions",
            profession,
            departement_code
        )

        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_evolution_prescriptions(
                profession,
                departement_code
            ),
            rafraichir=rafraichir
        )


    def get_specialites(self, annee, territorio, type_honoraire=None, rafraichir=False):
        cle = (
            "specialites",
            annee,
            territorio,
            type_honoraire
        )

        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_specialites(
                annee,
                territorio,
                type_honoraire
            ),
            rafraichir=rafraichir
        )


    def get_evolution_honoraires(
        self,
        profession,
        departement_code,
        type_honoraire=None,
        rafraichir=False
    ):
        cle = (
            "evolution_honoraires",
            profession,
            departement_code,
            type_honoraire
        )

        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_evolution_honoraires(
                profession,
                departement_code,
                type_honoraire
            ),
            rafraichir=rafraichir
        )

    def get_indicateur_cle(self, rafraichir=False):
        cle = ("dashboard", "indicateur_cle")

        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_indicateur_cle(),
            rafraichir=rafraichir
    )

    def get_repartition__specialite(self, rafraichir=False):
        cle = ("dashboard", "repartition_specialite")

        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_repartition__specialite(),
            rafraichir=rafraichir
        )

    def get_evolution_effectifs_all(self, rafraichir=False):
        cle = ("dashboard", "evolution_effectifs_all")

        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_evolution_effectifs_all(),
            rafraichir=rafraichir
        )

    def get_repartition_profesionnel(self, rafraichir=False):
        cle = ("dashboard", "repartition_professionnel")

        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_repartition_profesionnel(),
            rafraichir=rafraichir
        )

    def get_presence_femme(self, rafraichir=False):
        cle = ("dashboard", "presence_femme")

        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_presence_femme(),
            rafraichir=rafraichir
        )

    def get_medecin_patient(self, rafraichir=False):
        cle = ("dashboard", "medecin_patient")

        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_medecin_patient(),
            rafraichir=rafraichir
        )

    def _lire_ou_calculer(self, cle, produire, rafraichir=False):
        """
        Retourne une valeur depuis le cache ou la calcule si nécessaire.

        Cette méthode centralise la logique de mise en cache :
        - vérifie si une entrée existe ;
        - contrôle qu'elle n'a pas expiré ;
        - retourne la valeur en cache si elle est valide ;
        - sinon exécute la fonction fournie et stocke le résultat.

        Args:
            cle (tuple):
                Identifiant unique de la requête.

            produire (callable):
                Fonction permettant de produire la valeur
                lorsqu'elle n'est pas présente dans le cache.

            rafraichir (bool, optional):
                Indique s'il faut rafraîchir le cache.

        Returns:
            Any:
                Résultat récupéré depuis le cache ou calculé.
        """
        # Vérifie si la clé existe déjà dans le cache
        if not rafraichir and cle in self._memoire:
            valeur, ts = self._memoire[cle]

            # Vérifie que la durée de validité n'est pas dépassée
            if time.time() - ts <= self._duree:
                return valeur

        # Calcul de la valeur si absente ou expirée
        resultat = produire()

        # Enregistrement du résultat avec son horodatage
        self._memoire[cle] = (resultat, time.time())

        return resultat
