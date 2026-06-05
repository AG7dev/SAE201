from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, logout_user, login_user, current_user, login_manager
from utils.user import User
from models.db import Session
from models.dimensions import UserTable

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
            if user and user.password == password: # type: ignore
                login_user(User(username))
                return redirect(url_for("accueil.index"))

            return "Identifiants incorrects"

        finally:
            session.close()
    
    return render_template("login.html", option="login")

@login_controller.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("accueil.index"))

@login_controller.route("/createUser")
def createUser():
    return render_template("login.html", option="createUser")