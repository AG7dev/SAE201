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
    """Route qui gère la connection d'un utilisateur"""
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
    """Route qui gère la déconnection de l'utilisateur"""
    logout_user()
    return redirect(url_for("accueil.index"))

@bp_login.route("/createUser", methods=["GET", "POST"])
def createUser():
    """Route qui gère la création d'un utilisateur"""
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