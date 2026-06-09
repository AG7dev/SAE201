from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from models.data_utils import get_about_data
from models.db import Session
from models.dimensions import Formulaire
from datetime import datetime

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
        print(f"[DEBUG] {request.form.keys()=}")
        satisfaction_generale = request.form["noteSatisfaction"]
        facilite_utilisation = request.form["noteFacilite"]
        design_site = request.form["noteDesign"]
        rapidite_site = request.form["noteRapidite"]
        utilite_fontionalite = request.form["noteFonctionelite"]
        recommendation = 1 if request.form.get("formation", None) == "oui" else 0
        utilisation_fontionalite = request.form["fonction"]
        liste = [request.form.get(i, "") for i in ["problemeBugs", "problemeBugs", "problemeInterface"]]
        probleme = ';'.join(liste)
        commentaire = request.form["text"]
        
        session = Session()
        try:
            session.add(Formulaire(satisfaction_generale=satisfaction_generale, 
                        facilite_utilisation=facilite_utilisation,
                        design_site=design_site, rapidite_site=rapidite_site,
                        utilite_fontionalite=utilite_fontionalite,
                        recommendation=recommendation, 
                        utilisation_fontionalite=utilisation_fontionalite,
                        probleme=probleme, commentaire=commentaire,
                        date=datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                        username=current_user.id))
            session.commit()
            flash("Formulaire enregistrée !", "success")
        finally:
            session.close()
            
    return render_template("about.html", option="form")