from flask import Blueprint, render_template, request, current_app
from models.db import Session
from models.dimensions import ProfessionSante

bp_dashboard = Blueprint("dashboard", __name__)

@bp_dashboard.route("/dashboard")
def dashboard():
    indicateurCle = None
    repartitionSpecialite = None
    evolutionNombreProfessionel = None

    rafraichir_force = (request.args.get("force_refresh") == "1")
    
    session = Session()
    try:
        indicateurCle =  current_app.api_ameli.get_indicateur_cle(rafraichir=rafraichir_force)
        repartitionSpecialite = current_app.api_ameli.get_repartition__specialite(rafraichir=rafraichir_force)
        evolutionNombreProfessionel = current_app.api_ameli.get_evolution_effectifs_all(rafraichir=rafraichir_force)
        repartitionProfessionel = current_app.api_ameli.get_repartition_profesionnel(rafraichir=rafraichir_force)
        presenceFemme = current_app.api_ameli.get_presence_femme(rafraichir=rafraichir_force)
        medecinPatient = current_app.api_ameli.get_medecin_patient(rafraichir=rafraichir_force)
        
        return render_template("dashboard.html", indicateurCle=indicateurCle,
                               repartitionSpecialite=repartitionSpecialite,
                               evolutionNombreProfessionel=evolutionNombreProfessionel,
                               repartitionProfessionel=repartitionProfessionel,
                               presenceFemme=presenceFemme,
                               medecinPatient=medecinPatient)
    finally:
        session.close()