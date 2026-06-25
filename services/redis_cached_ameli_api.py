# ==================================================
#   SAÉ 2.01 - Développement d'une application WEB
# ==================================================

# Importations des modules nécessaires
import json
import redis
from models.db import Session
from models.dimensions import UserTable

class RedisCachedAmeliAPI:
    """
    Enveloppe une instance d'AmeliAPI pour ajouter un système de cache partagé
    via un serveur Redis.
    """

    def __init__(self, api_sous_jacente, hote='localhost', port=6379, db=0, duree_vie_seconde=600):
        """
        Initialise le décorateur de cache Redis.
        """
        self._api = api_sous_jacente
        self._duree = duree_vie_seconde
        # Connexion au client Redis
        self._redis = redis.Redis(host=hote, port=port, db=db, decode_responses=True)

    def vider_cache(self):
        """
        Vide toutes les clés associées à l'API AMELI sur Redis.
        """
        # Utilisation d'un pattern pour ne vider que les clés de cette API
        cles = self._redis.keys("ameli:*")
        if cles:
            self._redis.delete(*cles)

    def get_effectifs(self, profession, departement_code, annee, rafraichir=False):
        # Sérialisation de la clé sous forme de chaîne textuelle pour Redis
        cle = f"ameli:effectifs:{profession}:{departement_code}:{annee}"
        
        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_effectifs(profession, departement_code, annee),
            rafraichir=rafraichir
        )

    def get_evolution_effectifs(self, profession, departement_code, rafraichir=False):
        cle = f"ameli:evolution_effectifs:{profession}:{departement_code}"
        
        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_evolution_effectifs(profession, departement_code),
            rafraichir=rafraichir
        )

    def get_prescriptions(self, profession, departement_code, annee, rafraichir=False):
        cle = f"ameli:prescriptions:{profession}:{departement_code}:{annee}"

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
        cle = f"ameli:evolution_prescriptions:{profession}:{departement_code}"

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
            f"ameli:specialites:"
            f"{annee}:{territorio}:{type_honoraire}"
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
            f"ameli:evolution_honoraires:"
            f"{profession}:{departement_code}:{type_honoraire}"
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
        cle = "ameli:dashboard:indicateur_cle"

        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_indicateur_cle(),
            rafraichir=rafraichir
    )

    def get_repartition__specialite(self, rafraichir=False):
        cle = "ameli:dashboard:repartition_specialite"

        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_repartition__specialite(),
            rafraichir=rafraichir
        )

    def get_evolution_effectifs_all(self, rafraichir=False):
        cle = "ameli:dashboard:evolution_effectifs_all"

        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_evolution_effectifs_all(),
            rafraichir=rafraichir
        )

    def get_repartition_profesionnel(self, rafraichir=False):
        cle = "ameli:dashboard:repartition_professionnel"

        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_repartition_profesionnel(),
            rafraichir=rafraichir
        )

    def get_presence_femme(self, rafraichir=False):
        cle = "ameli:dashboard:presence_femme"

        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_presence_femme(),
            rafraichir=rafraichir
        )

    def get_medecin_patient(self, rafraichir=False):
        cle = "ameli:dashboard:medecin_patient"

        return self._lire_ou_calculer(
            cle,
            lambda: self._api.get_medecin_patient(),
            rafraichir=rafraichir
        )

    def get_permission(self, username, rafraichir=False):
        cle = f"user:{username}"
        
        def permission(username):
            session = Session()
            try:
                user = session.query(UserTable).filter(UserTable.username == username).first()
            finally:
                session.close()
            return user.permissions if user else None
        
        return self._lire_ou_calculer(
            cle,
            lambda: permission(username),
            rafraichir=rafraichir
        )

    def _lire_ou_calculer(self, cle, produire, rafraichir=False):
        """
        Gère la logique de lecture, désérialisation JSON et expiration native Redis.
        """
        if not rafraichir:
            # Tentative de récupération dans Redis
            valeur_stockee = self._redis.get(cle)
            if valeur_stockee is not None:
                # Redis renvoie une chaîne JSON, on la reconstruit en objet Python
                return json.loads(valeur_stockee)

        # Calcul/Appel API si absent ou rafraîchissement forcé
        resultat = produire()

        # Sérialisation en chaîne JSON obligatoire pour le stockage Redis
        valeur_json = json.dumps(resultat)
        
        # Stockage avec configuration native de la durée de vie (TTL)
        self._redis.set(cle, valeur_json, ex=self._duree)

        return resultat