from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from models.data_utils import get_about_data
from models.db import Session
from models.dimensions import Formulaire, UserTable
from datetime import datetime

bp_about = Blueprint("about", __name__)

@bp_about.route("/about")
def about():
    """Affiche les effectifs pour la sélection de l'utilisateur."""
    data = get_about_data()
    return render_template("about.html", data=data, option="about")

@bp_about.route("/about/form", methods=['GET', 'POST'])
@login_required
def form():
    if request.method == "POST":
        print(f"[DEBUG] {request.form.keys()=}")
        satisfaction_generale = request.form["noteSatisfaction"]
        facilite_utilisation = request.form["noteFacilite"]
        design_site = request.form["noteDesign"]
        rapidite_site = request.form["noteRapidite"]
        utilite_fontionalite = request.form["noteFonctionelite"]
        recommendation = 1 if request.form.get("recommendation", None) == "oui" else 0
        utilisation_fontionalite = request.form["fonction"]
        liste = [request.form.get(i, "") for i in ["problemeBugs", "problemeLenteurs", "problemeInterface"] if request.form.get(i, "") != ""]
        if len(liste) > 1: probleme = '/'.join(liste)
        elif len(liste) == 1: probleme = liste[0]
        else: probleme = None
        commentaire = request.form["text"]
        
        session = Session()
        try:
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
            render_template("about.html", option="about")
        finally:
            session.close()
            
    return render_template("about.html", option="form")

@bp_about.route("/about/adminPanel", methods=['GET', 'POST'])
@login_required
def adminPanel():
    view_type = request.args.get('view', 'form')
    
    data = None
    nbrUser = None
    nbrForm = None
    if view_type == "form":
        session = Session()
        try:
            data = session.query(Formulaire).all()
        finally:
            session.close()
            
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
    
    if view_type == "stat":
        session = Session()
        try:
            nbrUser = session.query(UserTable).count()
            nbrForm = session.query(Formulaire).count()
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
    
    if current_user.permissions != "admin":
        return render_template("erreur.hmtl", message="Vous n'avez pas les permissions"), 403
    return render_template("adminPanel.html", view=view_type, data=data, nbrUser=nbrUser, nbrForm=nbrForm)
