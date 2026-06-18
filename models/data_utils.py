import pandas as pd
from flask import url_for
import os

def exportToCsv(data:list):
    """Fonction qui reçoit la liste au retour d'une reqête api 
    et le sauvegarde dans un fichier csv"""
    try:
        df = pd.DataFrame(data)
        df.to_csv(os.path.join("static", "csv", "donnees.csv"), index=False)
    except (TypeError, OSError) as e:
        print("[data_utils.py] Erreur dans la fonction exportToCsv()\n", e)
        
def get_about_data():
    """Informations sur le projet sous forme de liste de listes
    Une liste interne par information (clé, valeur)"""
    about = [
        ["Projet", "Visualisation des données de data Ameli de 1950 à 2023"],
        ["Source(s) des données", "Base de données World Population Prospects 2024 de l'ONU"],
        ["Lien(s) vers les données", "<a href='https://population.un.org/wpp/downloads?folder=Standard' target='_blank'>https://population.un.org/wpp/downloads?folder=Standard</a>"],
        ["Auteur(s) du projet", ["BODILIS Macéo", "GOBALASAMY Arvin", "GONET--PETIT Clément", "SETTOURAMAN Arthy"]],
        ["Institution", "IUT de Créteil-Vitry, département Informatique"],
        ["Formation", "BUT Informatique - 1ère année - Semestre 2"],
        ["Année", "2025 - 2026"],
        ["Description", "Cette application permet de visualiser les doonées de data Ameli, ARVIN tu finira"],
        ["Fonctionnalités", "Affichage des données sous forme de tableaux, graphiques interactifs, cartes et indicateurs clés."],
        ["Technologies utilisées", [("Python", "https://www.python.org/"), ("Flask", "https://flask.palletsprojects.com/"), ("SQLite", "https://www.sqlite.org/index.html"), ("Plotly", "https://plotly.com/"), ("Pandas", "https://pandas.pydata.org/"), ("DataTables", "https://datatables.net/"), ("Folium", "https://python-visualization.github.io/folium/"), ("Bootstrap", "https://getbootstrap.com/docs/5.3/getting-started/introduction/")]],
    ]

    # Renvoyer les informations
    return about