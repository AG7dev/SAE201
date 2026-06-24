# ==================================================
#   SAÉ 2.01 - Développement d'une application WEB
# ==================================================

"""

"""


# services/comparaison_service.py


def comparer_effectifs(
    api,
    profession1,
    departement1,
    profession2,
    departement2,
    annee_debut,
    annee_fin,
    legende1,
    legende2,
    rafraichir=False
):
    """
    Compare deux séries d'effectifs.
    """
    if annee_debut == annee_fin:

        reponse1 = api.get_effectifs(
            profession1.libelle,
            departement1.code,
            annee_debut,
            rafraichir=rafraichir
        )

        reponse2 = api.get_effectifs(
            profession2.libelle,
            departement2.code,
            annee_debut,
            rafraichir=rafraichir
        )

        serie1 = normaliser_reponse_api(reponse1)
        serie2 = normaliser_reponse_api(reponse2)


        labels, valeurs1, valeurs2 = aligner_series(
            serie1,
            serie2
        )

        type_graphique = "bar"

    else:

        reponse1 = api.get_evolution_effectifs(
            profession1.libelle,
            departement1.code,
            rafraichir=rafraichir
        )

        reponse2 = api.get_evolution_effectifs(
            profession2.libelle,
            departement2.code,
            rafraichir=rafraichir
        )


        reponse1 = filtrer_annees(
            reponse1,
            annee_debut,
            annee_fin
        )

        reponse2 = filtrer_annees(
            reponse2,
            annee_debut,
            annee_fin
        )


        serie1 = normaliser_reponse_api(reponse1)
        serie2 = normaliser_reponse_api(reponse2)


        labels, valeurs1, valeurs2 = aligner_series(
            serie1,
            serie2
        )

        type_graphique = "line"

    return {
        "labels": labels,
        "serie1": valeurs1,
        "serie2": valeurs2,
        "legendes": [
            legende1,
            legende2
        ],
        "type_graphique": type_graphique,
        "aucune_donnee": len(labels) == 0
    }

def comparer_honoraires(
    api,
    profession1,
    departement1,
    profession2,
    departement2,
    annee_debut,
    annee_fin,
    legende1,
    legende2,
    rafraichir=False
):
    """
    Compare deux séries d'honoraires.
    """

    reponse1 = api.get_evolution_honoraires(
        profession1.libelle,
        departement1.code
    )

    reponse2 = api.get_evolution_honoraires(
        profession2.libelle,
        departement2.code
    )


    reponse1 = filtrer_annees(
        reponse1,
        annee_debut,
        annee_fin
    )

    reponse2 = filtrer_annees(
        reponse2,
        annee_debut,
        annee_fin
    )


    serie1 = normaliser_honoraires(
        reponse1
    )

    serie2 = normaliser_honoraires(
        reponse2
    )


    labels, valeurs1, valeurs2 = aligner_series(
        serie1,
        serie2
    )


    if annee_debut == annee_fin:
        type_graphique = "bar"
    else:
        type_graphique = "line"


    return {
        "labels": labels,
        "serie1": valeurs1,
        "serie2": valeurs2,
        "legendes": [
            legende1,
            legende2
        ],
        "type_graphique": type_graphique,
        "aucune_donnee": len(labels) == 0
    }



def comparer_prescriptions(
    api,
    profession1,
    departement1,
    profession2,
    departement2,
    annee_debut,
    annee_fin,
    legende1,
    legende2,
    rafraichir=False
):
    """
    Compare deux séries de prescriptions.
    """

    reponse1 = api.get_evolution_prescriptions(
        profession1.libelle,
        departement1.code
    )

    reponse2 = api.get_evolution_prescriptions(
        profession2.libelle,
        departement2.code
    )


    reponse1 = filtrer_annees(
        reponse1,
        annee_debut,
        annee_fin
    )

    reponse2 = filtrer_annees(
        reponse2,
        annee_debut,
        annee_fin
    )


    serie1 = normaliser_prescriptions(
        reponse1
    )

    serie2 = normaliser_prescriptions(
        reponse2
    )


    labels, valeurs1, valeurs2 = aligner_series(
        serie1,
        serie2
    )


    if annee_debut == annee_fin:
        type_graphique = "bar"
    else:
        type_graphique = "line"


    return {
        "labels": labels,
        "serie1": valeurs1,
        "serie2": valeurs2,
        "legendes": [
            legende1,
            legende2
        ],
        "type_graphique": type_graphique,
        "aucune_donnee": len(labels) == 0
    }

def filtrer_annees(data, annee_debut, annee_fin):
    """
    Filtre une évolution API entre deux années.
    """
    resultat = []

    for ligne in data:

        annee = int(ligne["annee"])

        if annee_debut <= annee <= annee_fin:
            resultat.append(ligne)

    return resultat

def normaliser_reponse_api(reponse):
    """
    Transforme :

    [
        {
            "annee": "2024",
            "effectif": 150
        }
    ]

    en :

    {
        2024: 150
    }
    """
    resultat = {}

    for ligne in reponse:

        resultat[int(ligne["annee"])] = int(ligne["effectif"])
    return resultat

def normaliser_honoraires(reponse):
    """
    Transforme les données honoraires en série année: valeur
    """

    resultat = {}

    for ligne in reponse:

        resultat[int(ligne["annee"])] = float(
            ligne.get("montant_honoraires", 0)
        )

    return resultat



def normaliser_prescriptions(reponse):
    """
    Transforme les données prescriptions en série année: valeur
    """

    resultat = {}

    for ligne in reponse:

        resultat[int(ligne["annee"])] = float(
            ligne.get("montant_total", 0)
        )

    return resultat

def aligner_series(serie1, serie2):
    """
    Aligne les deux séries sur l'union des années.
    """

    labels = sorted(
        set(serie1.keys()) |
        set(serie2.keys())
    )

    valeurs1 = []
    valeurs2 = []

    for annee in labels:

        valeurs1.append(
            serie1.get(annee, 0)
        )

        valeurs2.append(
            serie2.get(annee, 0)
        )

    return labels, valeurs1, valeurs2