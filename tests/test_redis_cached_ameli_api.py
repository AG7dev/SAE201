# ==================================================
#   SAÉ 2.01 - Développement d'une application WEB
# ==================================================

"""
Tests de la classe RedisCachedAmeliAPI avec pytest et fakeredis.
"""

import time
from unittest.mock import MagicMock
import fakeredis
import pytest

from services.ameli_api import AmeliAPI
from services.redis_cached_ameli_api import RedisCachedAmeliAPI


@pytest.fixture
def redis_api_setup():
    """
    Fixture initialisant un client Redis simulé (fakeredis) et l'API décorée.
    """
    api_brute_mock = AmeliAPI()
    api_brute_mock.get_effectifs = MagicMock(
        return_value=[{"annee": 2023, "effectif": 42}]
    )

    # Création du décorateur Redis
    api_avec_cache = RedisCachedAmeliAPI(api_brute_mock, duree_vie_seconde=2)
    
    # Utilisation d'un serveur FakeServer pour une gestion stable du temps et des commandes
    serveur_simule = fakeredis.FakeServer()
    api_avec_cache._redis = fakeredis.FakeRedis(server=serveur_simule, decode_responses=True)
    
    params = ("Médecin généraliste", "75", 2023)

    return api_avec_cache, api_brute_mock, params


def test_redis_cache_evite_appel_reseau_consecutif(redis_api_setup):
    """
    Vérifie que Redis distribue les données du cache au second appel.
    """
    api_avec_cache, api_brute_mock, params = redis_api_setup

    recup_1 = api_avec_cache.get_effectifs(*params)
    recup_2 = api_avec_cache.get_effectifs(*params)

    assert recup_1 == recup_2
    api_brute_mock.get_effectifs.assert_called_once_with(*params)


def test_redis_expiration_via_ttl(redis_api_setup):
    """
    Vérifie le comportement à l'expiration du TTL Redis.
    """
    api_avec_cache, api_brute_mock, params = redis_api_setup

    api_avec_cache.get_effectifs(*params)
    
    # Attente réelle de la fin du TTL (2 secondes configurées dans la fixture)
    time.sleep(2.1)

    api_avec_cache.get_effectifs(*params)
    assert api_brute_mock.get_effectifs.call_count == 2


def test_redis_vider_cache(redis_api_setup):
    """
    Vérifie que la suppression des clés correspondantes vide le cache global.
    """
    api_avec_cache, api_brute_mock, params = redis_api_setup

    api_avec_cache.get_effectifs(*params)
    api_avec_cache.vider_cache()
    api_avec_cache.get_effectifs(*params)

    assert api_brute_mock.get_effectifs.call_count == 2