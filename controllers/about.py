# ==================================================
#   SAÉ 2.01 - Développement d'une application WEB
# ==================================================

"""
Gestion des pages à propos de l'application.

Ce module permet :
- l'affichage des informations du projet ;
- la soumission de formulaires de satisfaction ;
- l'administration des formulaires et des utilisateurs.
"""

# Importation des modules nécessaires
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.data_utils import get_about_data
from models.db import Session
from models.dimensions import Formulaire, UserTable
from datetime import datetime

bp_about = Blueprint("about", __name__)

@bp_about.route("/about")
def about():
    """
    Affiche la page de présentation du projet.

    Returns:
        La page about.html accompagnée des données de présentation.
    """
    data = get_about_data()
    return render_template("about.html", data=data, option="about")

@bp_about.route("/about/form", methods=['GET', 'POST'])
@login_required
def form():
    """
    Affiche et traite le formulaire de satisfaction.

    En méthode GET, affiche le formulaire.

    En méthode POST, récupère les réponses de l'utilisateur,
    enregistre les données en base puis affiche un message
    de confirmation.

    Returns:
        La page du formulaire.
    """
    if request.method == "POST":
        print(f"[DEBUG] {request.form.keys()=}")
        satisfaction_generale = request.form["noteSatisfaction"]
        facilite_utilisation = request.form["noteFacilite"]
        design_site = request.form["noteDesign"]
        rapidite_site = request.form["noteRapidite"]
        utilite_fontionalite = request.form["noteFonctionelite"]
        recommendation = 1 if request.form.get("recommendation", None) == "oui" else 0
        utilisation_fontionalite = request.form["fonction"]

        # Construction de la liste des problèmes rencontrés
        liste = [request.form.get(i, "") for i in ["problemeBugs", "problemeLenteurs", "problemeInterface"] if request.form.get(i, "") != ""]
        
        if len(liste) > 1: probleme = '/'.join(liste)
        elif len(liste) == 1: probleme = liste[0]
        else: probleme = None
        commentaire = request.form["text"]
        
        session = Session()
        try:
            # Enregistrement des réponses dans la base de données
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
            return redirect(url_for("about.about"))
        finally:
            session.close()
            
    return render_template("about.html", option="form")

@bp_about.route("/about/adminPanel", methods=['GET', 'POST'])
@login_required
def adminPanel():
    """
    Affiche le panneau d'administration.

    Selon le paramètre 'view', permet :
    - la consultation des formulaires ;
    - la gestion des utilisateurs ;
    - la consultation des statistiques.

    Returns:
        La page d'administration ou une erreur 403 si
        l'utilisateur n'est pas administrateur.
    """
    view_type = request.args.get('view', 'form')
    
    data = None
    
    # Gestion des formulaires enregistrés
    if view_type == "form":
        session = Session()
        try:
            data = session.query(Formulaire).all()
        finally:
            session.close()
    
    # Gestion des comptes utilisateurs et des permissions
    if view_type == "user":
        
        chn = request.form.get("changePermission", None)
        changePermission = chn.split(';') if chn else None
        deleteButton = request.form.get("deleteButton", None)
        
        session = Session()
        try:
            if changePermission:
                user = session.query(UserTable).filter(UserTable.username == changePermission[0]).first()
                user.permissions = changePermission[1] 
                session.commit()
                changePermission = None
            if  deleteButton:
                f = session.query(UserTable).filter(UserTable.username == deleteButton).first()
                session.delete(f)
                session.commit()
                deleteButton = None
            data = session.query(UserTable).all()
        finally:
            session.close()      
    
    # Préparation des données statistiques
    if view_type == "stat":
        session = Session()
        try:
            data = [{
                "satisfaction_generale": f.satisfaction_generale,
                "facilite_utilisation":f.facilite_utilisation,
                "design_site": f.design_site,
                "rapidite_site": f.rapidite_site,
                "utilite_fontionalite": f.utilite_fontionalite,
                "recommendation": f.recommendation,
                "utilisation_fontionalite": f.utilisation_fontionalite,
                "probleme": f.probleme
            } for f in session.query(Formulaire).all()]
        finally:
            session.close()
    
    # Vérification des droits administrateur
    if current_user.permissions != "admin":
        return render_template("erreur.hmtl", message="Vous n'avez pas les permissions"), 403
    return render_template("adminPanel.html", view=view_type, data=data)
