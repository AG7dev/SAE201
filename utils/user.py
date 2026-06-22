# ==================================================
#   SAÉ 2.01 - Développement d'une application WEB
# ==================================================

"""
Gestion de l'utilisateur pour Flask-Login.

Ce module fournit une classe User permettant de :
- représenter un utilisateur connecté ;
- récupérer ses informations en base de données ;
- gérer les permissions.
"""

# Importation des modules nécessaires
from flask_login import UserMixin
from models.db import Session
from models.dimensions import UserTable

class User(UserMixin):
    """
    Représente un utilisateur connecté à l'application.

    Cette classe est utilisée par Flask-Login pour gérer
    l'authentification et les sessions utilisateur.
    """
    def __init__(self, username):
        self.id = username
        
    @property
    def permissions(self):
        """
        Récupère les permissions de l'utilisateur depuis la base.

        Returns:
            str | None: niveau de permission de l'utilisateur.
        """
        session = Session()
        try:
            user = session.query(UserTable).filter(UserTable.username == self.id).first()
        finally:
            session.close()
        return user.permissions if user else None