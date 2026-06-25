# ==================================================
#   SAÉ 2.01 - Développement d'une application WEB
# ==================================================

"""
Contrôleur des effectifs de professionnels de santé.

Ce module permet :
- la récupération des paramètres utilisateur (profession, département, année)
- l'appel à l'API AMELI
- l'affichage des effectifs et de leur évolution
- l'export des résultats en CSV
"""

# Importation des modules nécessaires
from flask import Blueprint, render_template, request, current_app
from models.db import Session
from models.dimensions import ProfessionSante, Departement
from models.data_utils import exportToCsv 

bp_effectifs = Blueprint("effectifs", __name__)

@bp_effectifs.route("/effectifs")
def afficher():
    """
    Affiche les effectifs des professionnels de santé.

    Récupère les paramètres fournis par l'utilisateur :
    - profession_id
    - departement_id
    - annee

    Procède ensuite à :
    - la récupération des objets en base
    - l'appel à l'API AMELI pour les données d'effectifs
    - la génération de l'évolution des effectifs
    - l'export des résultats en CSV

    Returns:
        Page HTML avec les résultats ou page d'erreur si paramètres invalides.
    """
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
        
        resultats = current_app.api_ameli.get_effectifs(prof.libelle, dept.code, annee, rafraichir=rafraichir_force)
        evolution = current_app.api_ameli.get_evolution_effectifs(prof.libelle, dept.code, rafraichir=rafraichir_force)
        
        exportToCsv(evolution)
        
        return render_template("effectifs.html",
        prof=prof, dept=dept, annee=annee,
        resultats=resultats, evolution=evolution)
    finally:
        session.close()
    