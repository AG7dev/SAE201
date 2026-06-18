# ==================================================
#   SAÉ 2.01 - Développement d'une application WEB
# ==================================================

"""
Contrôleur de la page de comparaison.

Ce module gère :
- l'affichage du formulaire de comparaison ;
- la récupération des choix utilisateur ;
- la récupération des objets SQLAlchemy ;
- l'appel au service de comparaison ;
- l'envoi des données préparées au template.
"""


from flask import Blueprint, render_template, request, current_app

from models.db import Session
from models.dimensions import ProfessionSante, Departement

from services.comparaison_service import comparer_effectifs

from utils.constants import DATASETS_COMPARAISON


# Blueprint de la page comparaison
bp_comparaison = Blueprint(
    "comparaison",
    __name__
)


@bp_comparaison.route("/comparaison")
def afficher():
    """
    Affiche la page de comparaison.

    Deux cas :

    Cas A :
        Aucun formulaire soumis.
        -> affichage des listes professions/départements/datasets.

    Cas B :
        Formulaire soumis.
        -> récupération des données et génération du graphique.
    """
    # Récupération des paramètres envoyés dans l'URL
    dataset = request.args.get(
        "dataset"
    )

    profession1_id = request.args.get(
        "profession1_id",
        type=int
    )

    profession2_id = request.args.get(
        "profession2_id",
        type=int
    )

    departement1_id = request.args.get(
        "departement1_id",
        type=int
    )

    departement2_id = request.args.get(
        "departement2_id",
        type=int
    )

    annee_debut = request.args.get(
        "annee_debut",
        type=int
    )

    annee_fin = request.args.get(
        "annee_fin",
        type=int
    )

    rafraichir_force = (
        request.args.get("force_refresh") == "1"
    )

    session = Session()

    try:

        # Chargement des données nécessaires au formulaire
        professions = (
            session.query(ProfessionSante)
            .order_by(
                ProfessionSante.libelle
            )
            .all()
        )

        departements = (
            session.query(Departement)
            .order_by(
                Departement.libelle
            )
            .all()
        )

        # ==========================
        # CAS A : premier affichage
        # ==========================

        if not all([
            dataset,
            profession1_id,
            profession2_id,
            departement1_id,
            departement2_id,
            annee_debut,
            annee_fin
        ]):

            return render_template(
                "comparaison.html",

                professions=professions,
                departements=departements,

                datasets=DATASETS_COMPARAISON
            )

        # ==========================
        # CAS B : comparaison demandée
        # ==========================


        prof1 = session.get(
            ProfessionSante,
            profession1_id
        )

        prof2 = session.get(
            ProfessionSante,
            profession2_id
        )


        dept1 = session.get(
            Departement,
            departement1_id
        )

        dept2 = session.get(
            Departement,
            departement2_id
        )


        if not prof1 or not prof2:

            return render_template(
                "erreur.html",
                message="Profession inconnue."
            ), 404


        if not dept1 or not dept2:

            return render_template(
                "erreur.html",
                message="Département inconnu."
            ), 404

        # Sélection du service selon le dataset
        if dataset == "effectifs":


            resultat = comparer_effectifs(

                current_app.api_ameli,

                prof1,
                dept1,

                prof2,
                dept2,

                annee_debut,
                annee_fin,

                # Légendes du graphique
                f"{dept1.libelle} - {prof1.libelle}",

                f"{dept2.libelle} - {prof2.libelle}",

                rafraichir=rafraichir_force
            )

        else:

            return render_template(
                "erreur.html",
                message="Dataset non disponible."
            ), 400

        # Retour vers le template
        return render_template(

            "comparaison.html",

            professions=professions,

            departements=departements,

            datasets=DATASETS_COMPARAISON,


            # Données sélectionnées
            profession1=prof1,
            profession2=prof2,

            departement1=dept1,
            departement2=dept2,

            annee_debut=annee_debut,
            annee_fin=annee_fin,


            # Données graphiques
            resultat=resultat
        )

    except Exception:

        return render_template(
            "erreur.html",
            message="Une erreur est survenue lors de la comparaison."
        ), 500

    finally:

        session.close()