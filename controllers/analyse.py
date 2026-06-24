# ==================================================
# SAÉ 2.01 - Application WEB
# ==================================================

from flask import Blueprint, render_template
from models.db import Session
from models.dimensions import Region, ProfessionSante


bp_analyse = Blueprint(
    "analyse",
    __name__
)


@bp_analyse.route("/analyse")
def index():

    session = Session()

    try:

        regions = session.query(Region)\
            .order_by(Region.libelle)\
            .all()

        professions = session.query(ProfessionSante)\
            .order_by(ProfessionSante.libelle)\
            .all()

        return render_template(
            "analyse.html",
            regions=regions,
            professions=professions
        )

    finally:
        session.close()