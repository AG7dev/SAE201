# ==================================================
#   SAÉ 2.01 - Développement d'une application WEB
# ==================================================

"""
Utilitaires de gestion de données.

Ce module fournit :
- l'export des données API en CSV ;
- les informations statiques affichées dans la page "about".
"""

from flask import url_for
import os
import csv

def exportToCsv(data: list, filename: str = "donnees.csv"):
    """
    Exporte une liste de données vers un fichier CSV sans dépendance externe (Pandas).

    Args:
        data (list): liste de dictionnaires issue d'une requête API.
        filename (str): nom du fichier CSV généré dans static/csv/.

    Returns:
        None
    """
    if not data or not isinstance(data, list):
        print("[data_utils.py] Données invalides ou vides pour l'export CSV.")
        return

    chemin_fichier = os.path.join("static", "csv", filename)
    
    # Sécurité : création du sous-dossier si absent
    os.makedirs(os.path.dirname(chemin_fichier), exist_ok=True)

    try:
        with open(chemin_fichier, mode="w", encoding="utf-8", newline="") as f:
            # Extraction des en-têtes à partir des clés du premier dictionnaire
            en_tetes = data[0].keys()
            writer = csv.DictWriter(f, fieldnames=en_tetes)
            
            writer.writeheader()
            writer.writerows(data)
    except (TypeError, OSError) as e:
        print("[data_utils.py] Erreur dans la fonction exportToCsv()\n", e)
        
def get_about_data():
    """
    Retourne les informations statiques du projet.

    Returns:
        list: liste de paires [clé, valeur] décrivant le projet.
    """
    about = [
        ["Projet", "Visualisation des données de data Ameli de 2010 à 2024"],
        ["Source(s) des données", "DataAmeli (Service API)"],
        ["Lien(s) vers les données", "<a href='https://population.un.org/wpp/downloads?folder=Standard' target='_blank'>https://population.un.org/wpp/downloads?folder=Standard</a>"],
        ["Auteur(s) du projet", ["BODILIS Macéo", "GOBALASAMY Arvin", "GONET--PETIT Clément", "SETTOURAMAN Arthy"]],
        ["Institution", "IUT de Créteil-Vitry, département Informatique"],
        ["Formation", "BUT Informatique - 1ère année - Semestre 2"],
        ["Année", "2025 - 2026"],
        ["Description", 
            "Cette application web a été développée dans le cadre de la SAÉ 2.01 « Développement d'une application WEB » du BUT Informatique. Elle permet de visualiser, "
            "analyser et comparer des données publiques issues de Data Ameli à travers plusieurs jeux de données. "
            "L'application exploite notamment trois datasets portant sur les effectifs, les honoraires et les prescriptions médicales. "
            "Elle propose différentes fonctionnalités de consultation, de représentation graphique et de comparaison afin de faciliter l'analyse des informations disponibles. "
            "Ce projet a été réalisé dans un objectif pédagogique et permet de mettre en œuvre des technologies de développement web, de traitement de données et de visualisation."
        ],
        ["Fonctionnalités", "Affichage des données sous forme de tableaux, graphiques interactifs, cartes et indicateurs clés."],
        ["Technologies utilisées", [
            ("Python", "https://www.python.org/"), 
            ("Flask", "https://flask.palletsprojects.com/"), 
            ("MySQL", "https://dev.mysql.com/"), 
            ("Plotly", "https://plotly.com/"), 
            ("Pandas", "https://pandas.pydata.org/"), 
            ("DataTables", "https://datatables.net/"), 
            ("Folium", "https://python-visualization.github.io/folium/"), 
            ("Bootstrap", "https://getbootstrap.com/docs/5.3/getting-started/introduction/")
        ]],
    ]

    # Renvoyer les informations
    return about