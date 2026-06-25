# ==================================================
#   SAÉ 2.01 - Développement d'une application WEB
# ==================================================

"""
Contrôleur d'authentification.

Ce module gère :
- la connexion des utilisateurs
- la déconnexion
- la création de comptes
- l'intégration avec Flask-Login
"""

# Importation des modules nécessaires
from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, logout_user, login_user
from utils.user import User
from models.db import Session
from models.dimensions import UserTable
from hashlib import sha3_256
from datetime import datetime

bp_login = Blueprint("login", __name__)

@bp_login.route("/login", methods=["GET", "POST"])
def login():
    """
    Gère l'authentification d'un utilisateur.

    En GET :
        Affiche la page de connexion.

    En POST :
        Vérifie les identifiants et connecte l'utilisateur si valides.

    Returns:
        Page login ou redirection vers l'accueil.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        session = Session()
        try:
            user = session.query(UserTable).filter(UserTable.username == username)\
                          .first()
            password = sha3_256(password.encode(), usedforsecurity=True).hexdigest()
            if user and user.password == password: # type: ignore
                login_user(User(username))
                return redirect(url_for("accueil.index"))
            flash("Identifiant incorrect", "erreur")

        finally:
            session.close()
    
    return render_template("login.html", option="login")

@bp_login.route("/logout")
@login_required
def logout():
    """
    Déconnecte l'utilisateur courant.

    Returns:
        Redirection vers la page d'accueil.
    """
    logout_user()
    return redirect(url_for("accueil.index"))

@bp_login.route("/createUser", methods=["GET", "POST"])
def createUser():
    """
    Crée un nouvel utilisateur.

    En GET :
        Affiche le formulaire d'inscription.

    En POST :
        Vérifie l'unicité du nom d'utilisateur,
        crée le compte et le stocke en base.

    Returns:
        Page login ou page d'inscription.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    
        session = Session()
        try:
            password = sha3_256(password.encode(), usedforsecurity=True).hexdigest()
            if not session.query(UserTable).filter(UserTable.username == username).first():
                session.add(UserTable(username=username, password=password, 
                                      date=datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
                session.commit()
                flash("Utilisateur créé", "success")
                return render_template("login.html", option="login")
            else:
                flash("Utilisateur déjà pris", "erreur")
        finally:
            session.close()
    
    return render_template("login.html", option="createUser")