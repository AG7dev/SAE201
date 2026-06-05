from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, logout_user, login_user, current_user, login_manager
from utils.user import User
from models.db import Session
from models.dimensions import UserTable
from hashlib import sha3_256

login_controller = Blueprint("login", __name__)

@login_controller.route("/login", methods=["GET", "POST"])
def login():    
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

@login_controller.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("accueil.index"))

@login_controller.route("/createUser", methods=["GET", "POST"])
def createUser():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    
        session = Session()
        try:
            password = sha3_256(password.encode(), usedforsecurity=True).hexdigest()
            if not session.query(UserTable).filter(UserTable.username == username).first():
                session.add(UserTable(username=username, password=password))
                session.commit()
                flash("utilisateur créé", "message")
                return render_template(url_for("login.login"))
            else:
                flash("utilisateur déjà pris", "erreur")
        finally:
            session.close()
    
    return render_template("login.html", option="createUser")