import pandas as pd
#! TODO Voir pour modifier l'emplacement et / ou le nom du fichier

def exportToCsv(data:list):
    """Fonction qui reçoit la liste au retour d'une reqête api 
    et le sauvegarde dans un fichier csv"""
    try:
        df = pd.DataFrame(data)
        df.to_csv("static/csv/donnees.csv")
    except TypeError as e:
        print("Erreur de type dans la fonction exportToCsv()\n", e)
        