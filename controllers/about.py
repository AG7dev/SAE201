from flask import Blueprint, render_template, request
from flask_login import login_required
from models.data_utils import get_about_data

bp_about = Blueprint("about", __name__)

@bp_about.route("/about")
def about():
    """Affiche les effectifs pour la sélection de l'utilisateur."""
    data = get_about_data()
    return render_template("about.html", data=data, option="about")

@bp_about.route("/about/form", methods=['GET', 'POST'])
@login_required
def form():
    if request.method == "POST":
        pass
    return render_template("about.html", option="form")