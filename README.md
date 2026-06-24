# SAE 2.01 - Développement d'une Application Web Flask

## Présentation

Cette SAE (Situation d'aprentissage évalué, ie un projet académique) consiste à développer une application web complète à partir de la base de données réalisée lors de la SAE 2.04.

L'application permet d'exploiter des données de l'Assurance Maladie à travers une interface web interactive intégrant :

- Consultation de données statistiques
- Visualisations graphiques dynamiques
- Comparaison de territoires
- Export CSV
- API REST JSON
- Architecture MVC

## Objectifs pédagogiques

- Mettre en œuvre une architecture MVC
- Développer une application web avec Flask
- Utiliser SQLAlchemy pour l'accès aux données
- Créer des interfaces dynamiques avec Jinja2
- Exploiter AJAX et les routes JSON
- Produire des visualisations avec Chart.js
- Déployer une application sur Alwaysdata

---

## Technologies utilisées

|Nom|Fonction|
|:-:|:-:|
|Python 3||
|Flask 3||
|SQLAlchemy||
|Jinja2||
|HTML5||
|CSS3||
|JavaScript||
|AJAX / Fetch API||
|Chart.js||
|MySQL||
|Alwaysdata||

---

## Structure du projet

## Architecture de l'application

---

```mermaid
---
config:
  layout: elk
---
graph TB
    subgraph Configuration["Configuration"]
        App["app.py<br/>Application Flask principale"]
        Config["config.py<br/>Paramètres et constantes"]
        WSGI["wsgi.py<br/>Interface WSGI (déploiement)"]
        Req["requirements.txt<br/>Dépendances Python"]
    end

    subgraph Modèle["Couche Modèle"]
        DB["models/db.py<br/>Connexion et gestion de la base de données"]
        Dimensions["models/dimensions.py<br/>Classes des tables correspondantes a celle de la base de données (dimensions)"]
    end

    subgraph Service["Couche Services"]
        AmeliAPI["services/ameli_api.py<br/>Client API externe (Ameli)"]
    end

    subgraph Contrôleur["Couche Contrôleurs"]
        AccueilCtrl["controllers/accueil.py<br/>Routes : Accueil"]
        EffectifsCtrl["controllers/effectifs.py<br/>Routes : Effectifs"]
        APICtrl["controllers/api.py<br/>Endpoints API"]
    end

    subgraph Vue["Couche Vues"]
        BaseHTML["templates/base.html<br/>Template principal"]
        AccueilHTML["templates/accueil.html<br/>Page d’accueil"]
        EffectifsHTML["templates/effectifs.html<br/>Page des effectifs"]
        ComparaisonHTML["templates/comparaison.html<br/>Page de comparaison"]
    end

    subgraph Statique["Fichiers statiques"]
        CSS["static/css/<br/>Feuilles de style"]
        JS["static/js/<br/>Scripts JavaScript"]
        Images["static/images/<br/>Images"]
    end

    %% Liaisons entre couches
    App -->|initialise| Contrôleur
    App -->|charge| Vue
    Config -->|configure| App
    WSGI -->|sert| App
    Req -->|liste| Config

    AccueilCtrl -->|interroge| Modèle
    EffectifsCtrl -->|interroge| Modèle
    APICtrl -->|interroge| Modèle

    AccueilCtrl -->|appelle| AmeliAPI
    EffectifsCtrl -->|appelle| AmeliAPI

    DB -->|gère| Dimensions
    AmeliAPI -->|alimente| Modèle

    AccueilCtrl -->|rend| AccueilHTML
    EffectifsCtrl -->|rend| EffectifsHTML
    EffectifsCtrl -->|rend| ComparaisonHTML
    AccueilHTML -->|hérite| BaseHTML
    EffectifsHTML -->|hérite| BaseHTML
    ComparaisonHTML -->|hérite| BaseHTML

    Vue -->|utilise| Statique
    BaseHTML -->|importe| CSS
    BaseHTML -->|importe| JS
    BaseHTML -->|affiche| Images

    %% Styles de groupe
    classDef configStyle stroke:#38bdf8,fill:#f0f9ff
    classDef modelStyle stroke:#818cf8,fill:#eef2ff
    classDef serviceStyle stroke:#4ade80,fill:#f0fdf4
    classDef controllerStyle stroke:#fb923c,fill:#fff7ed
    classDef viewStyle stroke:#a78bfa,fill:#f5f3ff
    classDef staticStyle stroke:#facc15,fill:#fefce8

    class App,Config,WSGI,Req configStyle
    class DB,Dimensions modelStyle
    class AmeliAPI serviceStyle
    class AccueilCtrl,EffectifsCtrl,APICtrl controllerStyle
    class BaseHTML,AccueilHTML,EffectifsHTML,ComparaisonHTML viewStyle
    class CSS,JS,Images staticStyle
```

---

## Fonctionnalités

### Consultation des données

Consultation sur les jeux de données suivants:

- Effectifs par spécialité, département et année
- Montant des prescription par spécialité, département et année
- Effectifs par spécialité, département et année
- Un dashboard qui affiche un ensemble d'information
- Une page permettent la comparaison entre deux jeux de données

### Cascade AJAX

Lorsqu'une région est sélectionnée :

1. Un appel AJAX est effectué.
2. Flask retourne les départements correspondants.
3. La liste des départements est mise à jour sans rechargement de page.

### Visualisations Chart.js

#### Courbe d'évolution

- Évolution des effectifs dans le temps
- Affichage dynamique des données

#### Diagramme en bar

- Comparaison entre deux jeux de données
- Affichage

#### Carte choroplèthe

- Comparaison entre deux territoires
- Affichage simultané sur un même graphique

### API REST

Routes JSON permettant d'alimenter les graphiques :

```http
GET /api/departements/<id_region>
GET /api/effectifs/<id_departement>
GET /api/honoraires/<id_departement>
```

### Export CSV

Téléchargement des résultats sous format CSV.

Exemple :

```csv
Annee,Effectif
2018,1200
2019,1350
2020,1400
```

---

### Export PDF

La majorité des graphes peuvent être exporté au format pdf

### Création d'utilisateur

L'utilisateur peut créer un compte sur le site, ainsi il peut remplir un formulaire de satisfaction sur le site, les administrateurs peuvent alors consulter ces formulaires et gérer les utilisateurs

## Installation

### Cloner le projet

```bash
git clone <url-du-projet>
cd SAE201-code
```

### Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## Configuration

Créer les variables d'environnement :

```env
FLASK_ENV=development

DB_USER=user
DB_PASSWORD=password
DB_HOST=localhost
DB_NAME=sae204

SECRET_KEY=cle_secrete
```

---

## Lancement de l'application

```bash
python app.py
```

L'application sera accessible à l'adresse :

```text
http://localhost:5000
```

> Egalement l'application sera en production pour un temps limité a cette adresse

---

## Compétences développées

### Développement Web

- Flask
- Jinja2
- Architecture MVC
- Blueprints

### Front-End

- HTML/CSS
- JavaScript
- AJAX
- Chart.js

### Bases de données

- SQLAlchemy
- MySQL
- ORM

### Déploiement

- Alwaysdata
- WSGI
- Gestion d'environnement Python

---

## Auteurs

Projet réalisé dans le cadre de la SAE 2.01 du BUT Informatique.

- BODILIS Macéo
- GOBALASAMY Arvin
- GONET--PETIT Clément
- SETTOURAMAN Arthy

Année universitaire : 2025-2026

IUT de Créteil-Vitry
Département Informatique

---
