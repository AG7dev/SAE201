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
from models.dimensions import ProfessionSante, Region, Departement

from services.comparaison_service import (
    comparer_effectifs,
    comparer_honoraires,
    comparer_prescriptions
)

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
        -> affichage des listes professions/régions/datasets.
        -> les départements sont chargés dynamiquement par JavaScript.

    Cas B :
        Formulaire soumis.
        -> récupération des données et génération du graphique.
    """


    # ==========================
    # Récupération des paramètres
    # ==========================


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


    region1_id = request.args.get(
        "region1_id",
        type=int
    )

    region2_id = request.args.get(
        "region2_id",
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

    if annee_debut and not (2010 <= annee_debut <= 2024):
        return render_template(
            "erreur.html",
            message="Année début invalide."
        ), 400


    if annee_fin and not (2010 <= annee_fin <= 2024):

        return render_template(
            "erreur.html",
            message="Année fin invalide."
        ), 400

    rafraichir_force = (
        request.args.get("force_refresh") == "1"
    )


    session = Session()


    try:


        # ==========================
        # Données du formulaire
        # ==========================


        professions = (
            session.query(ProfessionSante)
            .order_by(
                ProfessionSante.libelle
            )
            .all()
        )


        regions = (
            session.query(Region)
            .order_by(
                Region.libelle
            )
            .all()
        )


        # ==========================
        # Année unique
        # ==========================

        if annee_debut and not annee_fin:
            annee_fin = annee_debut

        elif annee_debut and annee_fin:
            if annee_debut > annee_fin:

                return render_template(
                    "erreur.html",
                    message="L'année de début doit être inférieure ou égale à l'année de fin."
                ), 400



        # ==========================
        # CAS A :
        # formulaire incomplet
        # ==========================


        if not all([
            dataset,
            profession1_id,
            profession2_id,
            region1_id,
            region2_id,
            departement1_id,
            departement2_id,
            annee_debut
        ]):


            return render_template(
                "comparaison.html",

                professions=professions,
                regions=regions,

                datasets=DATASETS_COMPARAISON,


                dataset_selectionne=dataset,


                profession1_id=profession1_id,
                profession2_id=profession2_id,


                region1_id=region1_id,
                region2_id=region2_id,


                departement1_id=departement1_id,
                departement2_id=departement2_id,


                annee_debut=annee_debut,
                annee_fin=annee_fin,


                resultat=None,


                erreur=(
                    "Veuillez renseigner tous les champs."
                )
            )



        # ==========================
        # Vérification années
        # ==========================


        if annee_debut > annee_fin:


            return render_template(
                "comparaison.html",

                professions=professions,
                regions=regions,

                datasets=DATASETS_COMPARAISON,


                dataset_selectionne=dataset,


                profession1_id=profession1_id,
                profession2_id=profession2_id,


                region1_id=region1_id,
                region2_id=region2_id,


                departement1_id=departement1_id,
                departement2_id=departement2_id,


                annee_debut=annee_debut,
                annee_fin=annee_fin,


                resultat=None,


                erreur=(
                    "L'année de début doit être inférieure "
                    "ou égale à l'année de fin."
                )
            )



        # ==========================
        # CAS B :
        # comparaison
        # ==========================


        prof1 = session.get(
            ProfessionSante,
            profession1_id
        )


        prof2 = session.get(
            ProfessionSante,
            profession2_id
        )


        region1 = session.get(
            Region,
            region1_id
        )


        region2 = session.get(
            Region,
            region2_id
        )


        dept1 = session.get(
            Departement,
            departement1_id
        )


        dept2 = session.get(
            Departement,
            departement2_id
        )



        # ==========================
        # Vérification objets
        # ==========================


        if not prof1 or not prof2:

            return render_template(
                "erreur.html",
                message="Profession inconnue."
            ), 404



        if not region1 or not region2:

            return render_template(
                "erreur.html",
                message="Région inconnue."
            ), 404



        if not dept1 or not dept2:

            return render_template(
                "erreur.html",
                message="Département inconnu."
            ), 404



        # ==========================
        # Service comparaison
        # ==========================


        if dataset == "effectifs":

            resultat = comparer_effectifs(
                current_app.api_ameli,

                prof1,
                dept1,

                prof2,
                dept2,

                annee_debut,
                annee_fin,

                f"{region1.libelle} - {dept1.libelle} - {prof1.libelle}",

                f"{region2.libelle} - {dept2.libelle} - {prof2.libelle}",

                rafraichir=rafraichir_force
            )


        elif dataset == "honoraires":

            resultat = comparer_honoraires(
                current_app.api_ameli,

                prof1,
                dept1,

                prof2,
                dept2,

                annee_debut,
                annee_fin,

                f"{region1.libelle} - {dept1.libelle} - {prof1.libelle}",

                f"{region2.libelle} - {dept2.libelle} - {prof2.libelle}",

                rafraichir=rafraichir_force
            )


        elif dataset == "prescriptions":

            resultat = comparer_prescriptions(
                current_app.api_ameli,

                prof1,
                dept1,

                prof2,
                dept2,

                annee_debut,
                annee_fin,

                f"{region1.libelle} - {dept1.libelle} - {prof1.libelle}",

                f"{region2.libelle} - {dept2.libelle} - {prof2.libelle}",

                rafraichir=rafraichir_force
            )


        else:

            return render_template(
                "erreur.html",
                message="Dataset non disponible."
            ), 400


        # ==========================
        # Retour graphique
        # ==========================


        return render_template(

            "comparaison.html",


            professions=professions,

            regions=regions,


            datasets=DATASETS_COMPARAISON,


            dataset_selectionne=dataset,


            profession1_id=profession1_id,
            profession2_id=profession2_id,


            region1_id=region1_id,
            region2_id=region2_id,


            departement1_id=departement1_id,
            departement2_id=departement2_id,


            resultat=resultat
        )



    except Exception as e:


        print(e)


        return render_template(
            "erreur.html",
            message=str(e)
        ), 500



    finally:

        session.close()