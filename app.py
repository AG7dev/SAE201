from flask import Flask, render_template
from config import Config
from controllers.accueil import bp_accueil
from controllers.api import bp_api
from controllers.effectifs import bp_effectifs
from controllers.login import login_controller
from controllers.about import about
from flask_login import LoginManager
from utils.user import User

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.get_secret_key()

# Initialise le gestionnaire d'utilisateur
login_manager = LoginManager()
login_manager.init_app(app)

# Enregistrement des contrôleurs (blueprints)
app.register_blueprint(bp_accueil)
app.register_blueprint(bp_api)
app.register_blueprint(bp_effectifs)
app.register_blueprint(login_controller)
app.register_blueprint(about)

@app.errorhandler(404)
def page_non_trouvee(e):
    return render_template("erreur.html",
    message="Page non trouvée."), 404

@app.errorhandler(500)
def erreur_serveur(e):
    return render_template("erreur.html",
    message="Erreur interne. Réessayez plus tard."), 500
    
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)