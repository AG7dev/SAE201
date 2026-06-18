import logging
from flask import Blueprint, render_template, request
from models.db import Session
from models.dimensions import ProfessionSante, Departement
from services.ameli_api import AmeliAPI

bp_prescriptions = Blueprint("prescriptions", __name__)
api = AmeliAPI()

@bp_prescriptions.route("/prescriptions")
def afficher():
    """Affiche les prescriptions pour la sélection de l'utilisateur."""
    profession_id = request.args.get("profession_id", type=int)
    departement_id = request.args.get("departement_id", type=int)
    annee = request.args.get("annee", type=int)
    session = Session()
    try:
        prof = session.get(ProfessionSante, profession_id)
        dept = session.get(Departement, departement_id)
        if not prof or not dept or not annee:
            return render_template("erreur.html",
        message="Paramètres manquants."), 400
        resultats = api.get_prescriptions(prof.libelle, dept.code, annee)
        evolution = api.get_evolution_prescriptions(prof.libelle, dept.code)
        return render_template("prescriptions.html", prof=prof, dept=dept, annee=annee, resultats=resultats, evolution=evolution)
    
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des prescriptions : {e}")
        return render_template("erreur.html", message="Une erreur technique est survenue."), 500
    
    finally:
        session.close()


def trouver_erreur(l):
    for i in l:
        if i == "FRANCE":
            l.remove(i)

