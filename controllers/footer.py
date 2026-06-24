from flask import Blueprint, render_template, request, flash

bp_footer = Blueprint("footer", __name__)


@bp_footer.route("/mentions-legales")
def mentions_legales():
    return render_template("mentions_legales.html")


@bp_footer.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        nom = request.form.get("nom")
        email = request.form.get("email")
        message = request.form.get("message")

        print("Contact reçu :")
        print(nom, email, message)

        flash("Votre message a bien été envoyé.", "succes")

    return render_template("contact.html")