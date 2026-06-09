from flask import Blueprint, render_template
from models.data_utils import get_about_data

about = Blueprint("about", __name__)

@about.route("/about")
def afficher():
    """Affiche les effectifs pour la sélection de l'utilisateur."""
    data = get_about_data()
    return render_template("about.html", data=data)