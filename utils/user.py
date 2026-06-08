from flask_login import UserMixin
from models.db import Session
from models.dimensions import UserTable

class User(UserMixin):
    """Classe User qui représente un utilisateur connecté a l'application"""
    def __init__(self, username):
        self.id = username
        
    @property
    def permissions(self):
        """Renvoie la permission de l'utilisateur"""
        session = Session()
        try:
            user = session.query(UserTable).filter(UserTable.username == self.id).first()
        finally:
            session.close()
        return user.permissions if user else None