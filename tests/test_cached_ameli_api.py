# ==================================================
#   SAÉ 2.01 - Développement d'une application WEB
# ==================================================

"""
Tests de la classe CachedAmeliAPI.

Ce module vérifie le bon fonctionnement du mécanisme de cache :
- utilisation du cache entre deux appels identiques ;
- expiration automatique des données après un délai défini ;
- vidage manuel du cache.

Les tests utilisent un objet simulé (Mock) afin d'éviter
les appels réels à l'API AMELI.
"""

# Imports des modules nécessaires pour manipuler les chemins et le système
import os
import sys

# Ajoute la racine du projet dans le PYTHONPATH afin de pouvoir
# importer les modules de l'application depuis le dossier tests.
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if root_path not in sys.path:
    sys.path.insert(0, root_path)

# Imports des modules nécessaires pour les tests
import pytest
import time
from unittest.mock import MagicMock

# Imports des classes à tester
from services.ameli_api import AmeliAPI
from services.cached_ameli_api import CachedAmeliAPI

@pytest.fixture
def api_setup():
    """
    Fixture initialisant une API simulée et un cache local de 2 secondes.
    """
    api_brute_mock = AmeliAPI()
    api_brute_mock.get_effectifs = MagicMock(
        return_value=[{"annee": 2023, "effectif": 42}]
    )

    api_avec_cache = CachedAmeliAPI(api_brute_mock, duree_vie_seconde=2)
    params = ("Médecin généraliste", "75", 2023)

    return api_avec_cache, api_brute_mock, params


def test_cache_evite_appel_reseau_consecutif(api_setup):
    """
    Vérifie que deux appels identiques consécutifs utilisent le cache.
    """
    api_avec_cache, api_brute_mock, params = api_setup

    recup_1 = api_avec_cache.get_effectifs(*params)
    recup_2 = api_avec_cache.get_effectifs(*params)

    assert recup_1 == recup_2
    api_brute_mock.get_effectifs.assert_called_once_with(*params)


def test_expiration_cache(api_setup):
    """
    Vérifie qu'une entrée expirée est recalculée.
    """
    api_avec_cache, api_brute_mock, params = api_setup

    api_avec_cache.get_effectifs(*params)
    time.sleep(2.1)
    api_avec_cache.get_effectifs(*params)

    assert api_brute_mock.get_effectifs.call_count == 2


def test_vider_cache(api_setup):
    """
    Vérifie que le vidage manuel du cache force un nouvel appel.
    """
    api_avec_cache, api_brute_mock, params = api_setup

    api_avec_cache.get_effectifs(*params)
    api_avec_cache.vider_cache()
    api_avec_cache.get_effectifs(*params)

    assert api_brute_mock.get_effectifs.call_count == 2