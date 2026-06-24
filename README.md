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
|Flask 3|Framework web Python utilisé pour développer l'application et gérer les routes, requêtes HTTP et API.|
|SQLAlchemy|ORM permettant d'interagir avec la base de données MySQL via des objets Python plutôt que du SQL brut.|
|Jinja2|Moteur de templates utilisé par Flask pour générer dynamiquement les pages HTML.|
|HTML5|Langage de balisage utilisé pour structurer le contenu des pages web.|
|JavaScript|Langage de programmation côté client utilisé pour rendre l'interface interactive.|
|Chart.js|Bibliothèque JavaScript permettant de créer des graphiques dynamiques et interactifs.|
|MySQL|Système de gestion de base de données relationnelle utilisé pour stocker les données de l'application.|
|Bootstrap|Framework CSS facilitant la création d'interfaces responsives et modernes.|
|Pandas|Bibliothèque Python utilisée pour la manipulation, l'analyse et le traitement des données.|

---

## Structure du projet

## Architecture de l'application

---

```mermaid
graph TB

    subgraph CONFIG["Configuration"]
        APP["app.py"]
        CONFIG["config.py"]
        ENV[".env"]
    end

    subgraph CONTROLLERS["Contrôleurs Flask"]
        ACCUEIL["accueil.py"]
        DASHBOARD["dashboard.py"]
        EFFECTIFS["effectifs.py"]
        HONORAIRES["honoraires.py"]
        PRESCRIPTIONS["prescriptions.py"]
        COMPARAISON["comparaison.py"]
        ABOUT["about.py"]
        LOGIN["login.py"]
        API["api.py"]
    end

    subgraph SERVICES["Services Métier"]
        AMELI["ameli_api.py"]
        CACHE["cached_ameli_api.py"]
        REDIS["redis_cached_ameli_api.py"]
        COMP_SERVICE["comparaison_service.py"]
    end

    subgraph MODELS["Modèle et Données"]
        DB["db.py"]
        DIM["dimensions.py"]
        DATA["data_utils.py"]
    end

    subgraph UTILS["Utilitaires"]
        USER["user.py"]
        CONST["constants.py"]
    end

    subgraph TEMPLATES["Templates Jinja2"]
        BASE["base.html"]
        ACCUEIL_HTML["accueil.html"]
        DASHBOARD_HTML["dashboard.html"]
        EFFECTIFS_HTML["effectifs.html"]
        HONORAIRES_HTML["honoraires.html"]
        PRESCRIPTIONS_HTML["prescriptions.html"]
        COMPARAISON_HTML["comparaison.html"]
        ABOUT_HTML["about.html"]
        LOGIN_HTML["login.html"]
    end

    subgraph STATIC["Ressources Statiques"]
        CSS["css/"]
        JS["js/"]
        IMG["images/"]
        GEOJSON["geojson/"]
        CSV["csv/"]
    end

    subgraph TESTS["Tests"]
        TEST_CACHE["test_cached_ameli_api.py"]
        TEST_REDIS["test_redis_cached_ameli_api.py"]
    end

    APP --> ACCUEIL
    APP --> DASHBOARD
    APP --> EFFECTIFS
    APP --> HONORAIRES
    APP --> PRESCRIPTIONS
    APP --> COMPARAISON
    APP --> ABOUT
    APP --> LOGIN
    APP --> API

    CONFIG --> APP
    ENV --> CONFIG

    ACCUEIL --> CACHE
    DASHBOARD --> CACHE
    EFFECTIFS --> CACHE
    HONORAIRES --> CACHE
    PRESCRIPTIONS --> CACHE
    COMPARAISON --> COMP_SERVICE

    CACHE --> AMELI
    REDIS --> AMELI

    AMELI --> DATA
    DATA --> DIM
    DIM --> DB

    LOGIN --> USER
    APP --> CONST

    ACCUEIL --> ACCUEIL_HTML
    DASHBOARD --> DASHBOARD_HTML
    EFFECTIFS --> EFFECTIFS_HTML
    HONORAIRES --> HONORAIRES_HTML
    PRESCRIPTIONS --> PRESCRIPTIONS_HTML
    COMPARAISON --> COMPARAISON_HTML
    ABOUT --> ABOUT_HTML
    LOGIN --> LOGIN_HTML

    ACCUEIL_HTML --> BASE
    DASHBOARD_HTML --> BASE
    EFFECTIFS_HTML --> BASE
    HONORAIRES_HTML --> BASE
    PRESCRIPTIONS_HTML --> BASE
    COMPARAISON_HTML --> BASE
    ABOUT_HTML --> BASE
    LOGIN_HTML --> BASE

    BASE --> CSS
    BASE --> JS
    BASE --> IMG

    EFFECTIFS --> GEOJSON
    COMPARAISON --> CSV

    TEST_CACHE --> CACHE
    TEST_REDIS --> REDIS

    classDef config fill:#e0f2fe,stroke:#0284c7
    classDef controller fill:#ffedd5,stroke:#ea580c
    classDef service fill:#dcfce7,stroke:#16a34a
    classDef model fill:#ede9fe,stroke:#7c3aed
    classDef view fill:#f5f3ff,stroke:#9333ea
    classDef util fill:#fef3c7,stroke:#d97706
    classDef test fill:#fecaca,stroke:#dc2626

    class APP,CONFIG,ENV config
    class ACCUEIL,DASHBOARD,EFFECTIFS,HONORAIRES,PRESCRIPTIONS,COMPARAISON,ABOUT,LOGIN,API controller
    class AMELI,CACHE,REDIS,COMP_SERVICE service
    class DB,DIM,DATA model
    class BASE,ACCUEIL_HTML,DASHBOARD_HTML,EFFECTIFS_HTML,HONORAIRES_HTML,PRESCRIPTIONS_HTML,COMPARAISON_HTML,ABOUT_HTML,LOGIN_HTML view
    class USER,CONST util
    class TEST_CACHE,TEST_REDIS test
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
