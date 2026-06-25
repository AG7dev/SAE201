import logging
from flask import Blueprint, render_template, request, current_app
from models.db import Session
from models.dimensions import ProfessionSante, Departement
from models.data_utils import exportToCsv

bp_prescriptions = Blueprint("prescriptions", __name__)

@bp_prescriptions.route("/prescriptions")
def afficher():
    """Affiche les prescriptions pour la sélection de l'utilisateur."""
    profession_id = request.args.get("profession_id", type=int)
    departement_id = request.args.get("departement_id", type=int)
    annee = request.args.get("annee", type=int)

    # Vérifie si l'utilisateur a demandé un rafraîchissement forcé du cache
    rafraichir_force = (request.args.get("force_refresh") == "1")

    session = Session()
    try:
        prof = session.get(ProfessionSante, profession_id)
        dept = session.get(Departement, departement_id)
        if not prof or not dept or not annee:
            return render_template("erreur.html",
        message="Paramètres manquants."), 400
        resultats = current_app.api_ameli.get_prescriptions(prof.libelle, dept.code, annee, rafraichir=rafraichir_force)
        evolution = current_app.api_ameli.get_evolution_prescriptions(prof.libelle, dept.code, rafraichir=rafraichir_force)
        
        exportToCsv(evolution)
        
        return render_template("prescriptions.html", prof=prof, dept=dept, annee=annee, resultats=resultats, evolution=evolution)
    
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des prescriptions : {e}")
        return render_template(
            "erreur.html",
            message=f"Erreur technique : {e}"
        ), 500
    
    finally:
        session.close()





