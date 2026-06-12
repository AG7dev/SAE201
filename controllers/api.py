# ==================================================
#   SAÉ 2.01 - Développement d'une application WEB
# ==================================================

"""
API de l'application.

Ce module expose des routes au format JSON permettant
l'accès aux données depuis le frontend (AJAX).
"""

# Importation des modules nécessaires
from flask import Blueprint, jsonify
from models.db import Session
from models.dimensions import Departement

bp_api = Blueprint("api", __name__, url_prefix="/api")

@bp_api.route("/departements/<int:region_id>")
def departements(region_id):
    """
    Retourne la liste des départements d'une région.

    Args:
        region_id (int): Identifiant de la région.

    Returns:
        Response JSON contenant les départements :
        [
            {
                "id": int,
                "code": str,
                "libelle": str
            }
        ]
    """
    session = Session()
    try:
        depts = (session.query(Departement)
        .filter_by(region_id=region_id)
        .order_by(Departement.code).all())
        return jsonify([
        {"id": d.id, "code": d.code, "libelle": d.libelle}
        for d in depts
        ])
    finally:
        session.close()