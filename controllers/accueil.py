# ==================================================
#   SAÉ 2.01 - Développement d'une application WEB
# ==================================================

"""
Contrôleur de la page d'accueil.

Ce module gère l'affichage de la page principale de l'application,
incluant les régions et les professions de santé disponibles.
"""

# Importation des modules nécessaires
from flask import Blueprint, render_template
from models.db import Session
from models.dimensions import Region, ProfessionSante

bp_accueil = Blueprint("accueil", __name__)

@bp_accueil.route("/")
def index():
    """
    Affiche la page d'accueil.

    Récupère depuis la base de données :
    - la liste des régions
    - la liste des professions de santé

    Returns:
        Page HTML de l'accueil avec les données injectées.
    """
    session = Session()
    try:
        regions = session.query(Region).order_by(Region.libelle).all()
        professions = (session.query(ProfessionSante)
        .order_by(ProfessionSante.libelle).all())
        return render_template("accueil.html",
        regions=regions,
        professions=professions)
    finally:
        session.close()