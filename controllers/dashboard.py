from flask import Blueprint, render_template
from models.db import Session
from services.ameli_api import AmeliAPI
from models.dimensions import ProfessionSante

bp_dashboard = Blueprint("dashboard", __name__)
api = AmeliAPI()

@bp_dashboard.route("/dashboard")
def dashboard():
    indicateurCle = None
    repartitionSpecialite = None
    evolutionNombreProfessionel = None
    
    session = Session()
    try:
        indicateurCle =  api.get_indicateur_cle()
        repartitionSpecialite = api.get_repartition__specialite()
        evolutionNombreProfessionel = api.get_evolution_effectifs_all()
        repartitionProfessionel = api.get_repartition_profesionnel()
        presenceFemme = api.get_presence_femme()
        medecinPatient = api.get_medecin_patient()
        return render_template("dashboard.html", indicateurCle=indicateurCle,
                               repartitionSpecialite=repartitionSpecialite,
                               evolutionNombreProfessionel=evolutionNombreProfessionel,
                               repartitionProfessionel=repartitionProfessionel,
                               presenceFemme=presenceFemme,
                               medecinPatient=medecinPatient)
    finally:
        session.close()