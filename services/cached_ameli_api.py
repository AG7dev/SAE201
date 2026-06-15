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
