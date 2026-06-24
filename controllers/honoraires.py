from flask import Blueprint, render_template, request
from models.db import Session
from models.dimensions import ProfessionSante, Departement, Region
from services.ameli_api import AmeliAPI
import requests

# Initialisation du Blueprint et du service API
bp_honoraires = Blueprint("honoraires", __name__)
api = AmeliAPI()

@bp_honoraires.route('/honoraires/dashboard', methods=['GET'])
def afficher_honoraires():
    annee = request.args.get("annee")
    dept_id = request.args.get("departement_id")
    prof_id = request.args.get("profession_id")
    region_id = request.args.get("region_id")
    type_honoraire = request.args.get("type_honoraire")

    session = Session()
    prof_selectionnee = session.get(ProfessionSante, prof_id) if prof_id else None
    dept = session.get(Departement, dept_id) if dept_id else None
    region = session.get(Region, region_id) if region_id else None
    session.close()

    donnees_evolution = []
    donnees_specialites = []
    donnees_groupees_evo = {} 

    territoire_code = dept.code if dept else region_id
    nom_territoire = dept.libelle if dept else (region.libelle if region else "le territoire")

    if territoire_code:
        if prof_selectionnee:
            try:
                donnees_evolution = api.get_evolution_honoraires(prof_selectionnee.libelle, territoire_code, type_honoraire)
                
                for d in donnees_evolution:
                    an = d.get('annee')
                    if an not in donnees_groupees_evo:
                        donnees_groupees_evo[an] = {'total': 0, 'moyen': 0}
                    donnees_groupees_evo[an]['total'] += float(d.get('montant_honoraires') or 0)
                    donnees_groupees_evo[an]['moyen'] += float(d.get('montant_honoraires_moyens') or 0)
            except Exception as e:
                print(f"Erreur API Évolution : {e}")

        if annee:
            try:
                donnees_specialites = api.get_specialites(annee, territoire_code, type_honoraire)
            except Exception as e:
                print(f"Erreur API Spécialités : {e}")

    return render_template('honoraires.html',
                           donnees_evolution=donnees_evolution,
                           donnees_groupees_evo=donnees_groupees_evo,
                           donnees_specialites=donnees_specialites,
                           prof=prof_selectionnee,
                           nom_territoire=nom_territoire,
                           annee=annee)