from flask import Blueprint, render_template, request
from models.db import Session
from models.dimensions import ProfessionSante, Departement
from services.ameli_api import AmeliAPI
from models.data_utils import exportToCsv 

bp_honoraires = Blueprint("honoraires", __name__)
api = AmeliAPI()

@bp_honoraires.route("/honoraires")
def afficher():
    """Affiche les honoraires pour la sélection de l'utilisateur."""
    profession_id = request.args.get("profession_id", type=int)
    departement_id = request.args.get("departement_id", type=int)
    annee = request.args.get("annee", type=int)
    session = Session()
    try:
        prof = session.get(ProfessionSante, profession_id)
        dept = session.get(Departement, departement_id)
        
        if not prof or not dept or not annee:
            return render_template("erreur.html", message="Paramètres manquants."), 400
        
        resultats = api.get_honoraires(annee, prof.libelle, dept.code)
        
        exportToCsv(resultats)
        
        return render_template("honoraires.html", prof=prof, dept=dept, annee=annee, resultats=resultats)
    finally:
        session.close()