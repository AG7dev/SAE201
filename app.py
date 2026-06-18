# ==================================================
#   SAÉ 2.01 - Développement d'une application WEB
# ==================================================

"""
Point d'entrée de l'application Flask.

Ce module :
- initialise l'application Flask ;
- charge la configuration ;
- configure Flask-Login ;
- enregistre les blueprints ;
- définit les pages d'erreur personnalisées ;
- lance le serveur de développement.
"""

# Importation des modules nécessaires
from flask import Flask, render_template
from config import Config
from controllers.accueil import bp_accueil
from controllers.api import bp_api
from controllers.effectifs import bp_effectifs
from controllers.login import bp_login
from controllers.about import bp_about
from flask_login import LoginManager
from utils.user import User

# Importation des classes de l'API AMELI et du décorateur de cache
from services.ameli_api import AmeliAPI
from services.cached_ameli_api import CachedAmeliAPI
from services.redis_cached_ameli_api import RedisCachedAmeliAPI

# Création et configuration de l'application Flask
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.get_secret_key()

# Initialisation de l'API AMELI avec cache
api_brute = AmeliAPI()

# OPTION A : Cache local en mémoire (dictionnaire)
# app.api_ameli = CachedAmeliAPI(api_brute, duree_vie_seconde=300)

# OPTION B : Cache partagé Redis (à activer pour la mise en commun)
app.api_ameli = RedisCachedAmeliAPI(api_brute, hote='localhost', port=6379, duree_vie_seconde=300)

# Initialise le gestionnaire d'utilisateur
login_manager = LoginManager()
login_manager.init_app(app)

# Enregistrement des différentes routes de l'application (blueprints)
app.register_blueprint(bp_accueil)
app.register_blueprint(bp_api)
app.register_blueprint(bp_effectifs)
app.register_blueprint(bp_login)
app.register_blueprint(bp_about)

# Gestion des erreurs personnalisées
@app.errorhandler(401)
def acces_non_autorise(e):
    """
    Affiche une page personnalisée lorsqu'un accès est refusé.

    Args:
        e: Exception HTTP générée par Flask.

    Returns:
        Tuple contenant la page d'erreur et le code HTTP 401.
    """
    return render_template(
        "erreur.html",
        message="Vous n'avez pas accès a cette page pour l'instant"
    ), 401

@app.errorhandler(404)
def page_non_trouvee(e):
    """
    Affiche une page personnalisée lorsqu'une ressource est introuvable.

    Args:
        e: Exception HTTP générée par Flask.

    Returns:
        Tuple contenant la page d'erreur et le code HTTP 404.
    """
    return render_template(
        "erreur.html",
        message="Page non trouvée."
    ), 404

@app.errorhandler(500)
def erreur_serveur(e):
    """
    Affiche une page personnalisée lors d'une erreur interne du serveur.

    Args:
        e: Exception HTTP générée par Flask.

    Returns:
        Tuple contenant la page d'erreur et le code HTTP 500.
    """
    return render_template(
        "erreur.html",
        message="Erreur interne. Réessayez plus tard."
    ), 500

# Fonction de chargement de l'utilisateur pour Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """
    Charge un utilisateur à partir de son identifiant.

    Cette fonction est utilisée automatiquement par Flask-Login
    pour restaurer la session d'un utilisateur authentifié.

    Args:
        user_id: Identifiant de l'utilisateur stocké en session.

    Returns:
        Instance de User correspondant à l'identifiant fourni.
    """
    return User(user_id)

# Boucle de lancement de l'application Flask
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)