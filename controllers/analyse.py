# ==================================================
# SAÉ 2.01 - Application WEB
# ==================================================

from flask import Blueprint, render_template


bp_analyse = Blueprint(
    "analyse",
    __name__
)


@bp_analyse.route("/analyse")
def index():

    return render_template(
        "analyse.html"
    )