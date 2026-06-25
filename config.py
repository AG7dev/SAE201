# ==================================================
#   SAÉ 2.01 - Développement d'une application WEB
# ==================================================

"""
Configuration centralisée de l'application.

Ce module charge les variables d'environnement et fournit
les paramètres nécessaires au fonctionnement de l'application,
notamment la connexion à la base de données et la clé secrète.
"""

# Importation des modules nécessaires
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement à partir du fichier .env
load_dotenv()

class Config:
    """
    Regroupe les paramètres de configuration de l'application.

    Les valeurs sont récupérées depuis le fichier .env afin
    de séparer la configuration du code source.
    """
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    
    @classmethod
    def db_url(cls):
        """
        Construit l'URL de connexion à la base de données MySQL.

        Returns:
            str: URL de connexion SQLAlchemy.
        """
        return (f"mysql+pymysql://{cls.DB_USER}:{cls.DB_PASSWORD}"
        f"@{cls.DB_HOST}/{cls.DB_NAME}")
        
    @classmethod
    def get_secret_key(cls):
        """
        Retourne la clé secrète utilisée par Flask.

        Returns:
            str: Clé secrète de l'application.
        """
        return cls.SECRET_KEY