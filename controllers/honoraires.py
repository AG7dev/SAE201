from flask import Blueprint, render_template, request
from models.db import Session
from models.dimensions import ProfessionSante, Departement, Region
from services.ameli_api import AmeliAPI

bp_honoraires = Blueprint("honoraires", __name__)
api = AmeliAPI()

@bp_honoraires.route('/honoraires', methods=['GET'])
def afficher():
    annee = request.args.get("annee")
    dept_id = request.args.get("departement_id")
    prof_id = request.args.get("profession_id")
    
    session = Session()
    prof_list = session.query(ProfessionSante).all()
    regions = session.query(Region).all()

    resultats = []
    prof_selectionnee = None
    dept = None

    if prof_id and dept_id: 
        prof_selectionnee = session.get(ProfessionSante, prof_id)
        dept = session.get(Departement, dept_id)

        if prof_selectionnee and dept : 
            resultats = api.get_honoraires(annee, prof_selectionnee.libelle, dept.code)

    session.close()
    
    return render_template('honoraires.html', 
                           resultats=resultats, 
                           professions=prof_list,
                           prof=prof_selectionnee,
                           regions=regions,
                           dept=dept,
                           annee=annee)