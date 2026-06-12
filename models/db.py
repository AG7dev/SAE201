# ==================================================
#   SAÉ 2.01 - Développement d'une application WEB
# ==================================================

"""
Configuration de la base de données.

Ce module initialise :
- le moteur SQLAlchemy ;
- la fabrique de sessions utilisée par l'application.
"""

# Importation des modules nécessaires
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config

# Moteur SQLAlchemy global de l'application
engine = create_engine(Config.db_url(), pool_recycle=3600)

# Fabrique de sessions (une session par requête HTTP)
Session = sessionmaker(bind=engine)