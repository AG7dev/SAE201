# ===== SAE 2.01 - Ajouter la table user_table =====

# Import des bibliothèques nécessaires
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Import du modèle depuis le fichier models_dimensions.py
from models.dimensions import Base

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# Construction de l'URL de connexion à la base MySQL
url = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
url += f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

# Création du moteur de connexion SQLAlchemy
engine = create_engine(url)

# Création des tables définies dans le modèle
Base.metadata.create_all(engine)

# Affichage des tables créées
print("Tables créées :")
for t in Base.metadata.tables: 
    print(f" Ok {t}")