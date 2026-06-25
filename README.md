# SAE 2.01 - Développement d'une Application Web Flask

## Présentation

Ce projet s'inscrit dans le cadre de la SAE 2.01 du BUT Informatique.  
Il consiste à développer une application web permettant d'exploiter des données issues de l’Assurance Maladie, en s’appuyant sur une base de données réalisée lors de la SAE 2.04.

L’application propose une interface interactive permettant :

- la consultation de données statistiques,
- la visualisation graphique dynamique,
- la comparaison de territoires,
- l’export de données,
- l’exposition d’une API REST,
- la gestion d’utilisateurs.

---

## Objectifs pédagogiques

- Mettre en œuvre une architecture web structurée (type MVC enrichie)
- Développer une application complète avec Flask
- Exploiter une base de données via SQLAlchemy
- Générer des interfaces dynamiques avec Jinja2
- Mettre en place des échanges AJAX et une API JSON
- Réaliser des visualisations avec Chart.js
- Gérer un déploiement sur environnement distant (Alwaysdata)

---

## Technologies utilisées

| Technologie | Rôle |
|:-|:-|
| Flask 3 | Framework web Python pour la gestion des routes et de l’application |
| SQLAlchemy | ORM pour l’accès et la manipulation de la base de données |
| Jinja2 | Moteur de templates pour la génération HTML dynamique |
| HTML5 / CSS3 | Structure et mise en forme des pages web |
| JavaScript | Interactivité côté client et AJAX |
| Chart.js | Visualisation de données (graphiques dynamiques) |
| MySQL | Système de gestion de base de données |
| Bootstrap | Framework CSS pour interface responsive |
| Pandas | Traitement et transformation des données pour export |

---

## Architecture du projet

L’application repose sur une architecture modulaire de type MVC enrichie (controllers / services / models / utils).

```text
SAE201/
│
├── app.py                      # Point d'entrée principal de l'application Flask
├── config.py                   # Configuration générale de l'application
├── .env                        # Variables d'environnement
├── .env.example                # Exemple de configuration
├── README.md                   # Documentation du projet
├── .gitignore                  # Fichiers ignorés par Git
│
├── controllers/                # Contrôleurs Flask (routes et logique de présentation)
│   ├── accueil.py              # Page d'accueil
│   ├── dashboard.py            # Tableau de bord principal
│   ├── analyse.py              # Analyse des données
│   ├── comparaison.py          # Comparaison de données
│   ├── effectifs.py            # Gestion des effectifs
│   ├── honoraires.py           # Analyse des honoraires
│   ├── prescriptions.py        # Analyse des prescriptions
│   ├── about.py                # Page à propos
│   ├── footer.py               # Pages du pied de page
│   ├── login.py                # Authentification
│   └── api.py                  # Endpoints API
│
├── models/                     # Accès et manipulation des données
│   ├── db.py                   # Connexion à la base de données
│   ├── dimensions.py           # Gestion des dimensions métier
│   └── data_utils.py           # Fonctions utilitaires de traitement des données
│
├── services/                   # Services métier
│   ├── ameli_api.py            # Communication avec l'API Ameli
│   ├── cached_ameli_api.py     # Mise en cache locale des appels API
│   ├── redis_cached_ameli_api.py # Mise en cache Redis
│   └── comparaison_service.py  # Logique métier des comparaisons
│
├── templates/                  # Templates HTML Jinja2
│   ├── base.html               # Template principal
│   ├── accueil.html            # Vue accueil
│   ├── dashboard.html          # Vue dashboard
│   ├── analyse.html            # Vue analyse
│   ├── comparaison.html        # Vue comparaison
│   ├── effectifs.html          # Vue effectifs
│   ├── honoraires.html         # Vue honoraires
│   ├── prescriptions.html      # Vue prescriptions
│   ├── login.html              # Vue connexion
│   ├── about.html              # Vue à propos
│   ├── contact.html            # Vue contact
│   ├── mentions_legales.html   # Mentions légales
│   ├── adminPanel.html         # Interface d'administration
│   └── erreur.html             # Gestion des erreurs
│
├── static/                     # Ressources statiques
│   ├── css/
│   │   └── style.css           # Feuille de style principale
│   │
│   ├── js/
│   │   ├── analyse.js          # Scripts de la page analyse
│   │   ├── cascade.js          # Gestion des listes dépendantes
│   │   └── download.js         # Export et téléchargement de données
│   │
│   ├── images/                 # Logos, icônes et captures d'écran
│   ├── geojson/                # Cartes des régions et départements
│   └── csv/                    # Données exportées au format CSV
│
├── utils/                      # Fonctions utilitaires
│   ├── constants.py            # Constantes globales
│   └── user.py                 # Gestion des utilisateurs
│
├── tests/                      # Tests unitaires
│   ├── test_ameli_api.py
│   ├── test_cached_ameli_api.py
│   └── test_redis_cached_ameli_api.py
│
├── scripts/                    # Scripts d'administration
│   └── create_user_table.py    # Création de la table utilisateurs
│
└── __pycache__/                # Fichiers Python compilés automatiquement
```

---

## Fonctionnalités principales

### Consultation des données

L’application permet l’exploration de données statistiques :

- une page analyse permettant d'explorer les données de différents jeux de données
  - Effectifs
  - Honoraires
  - Prescrpition
- tableau de bord global de synthèse.
- La possibilité de comparer des donnée au sein du même jeux de données

> La page analyse peut potentiellement ne pas marcher en raison de certain bloqueurs de publicités

### Visualisation des données

Utilisation de Chart.js pour :

- courbes d’évolution temporelle,
- graphiques de comparaison,
- visualisations territoriales (cartes choroplèthes).

### Interactivité AJAX

Les sélections dynamiques (régions → départements) sont gérées sans rechargement de page via des appels AJAX vers l’API Flask.

### API REST

Endpoints JSON permettant l’exploitation des données :

```http
GET /api/departements/<id_region>
GET /api/effectifs/<id_departement>
GET /api/honoraires/<id_departement>
```

### Export de données

- Export CSV des résultats statistiques
- Génération de fichiers exploitables pour analyse externe

### Gestion utilisateur

- Création de compte utilisateur
- Formulaire de satisfaction
- Interface administrateur pour consultation et gestion des utilisateurs

---

## Installation

```bash
git clone <url-du-projet>
cd SAE201
pip install -r requirements.txt
```

---

## Configuration

Créer un fichier `.env` :

```env
FLASK_ENV=development

DB_USER=user
DB_PASSWORD=password
DB_HOST=localhost
DB_NAME=sae204

SECRET_KEY=cle_secrete
```

---

## Lancement

```bash
python app.py
```

Application accessible sur :
`http://localhost:5000`

---

## Compétences mises en œuvre

### Développement web

- Flask (blueprints, routing)
- Architecture MVC enrichie
- API REST

### Front-end

- HTML / CSS / Bootstrap
- JavaScript + AJAX
- Chart.js

### Données

- SQLAlchemy (ORM)
- MySQL
- Pandas (export et traitement)

### Déploiement

- WSGI
- Alwaysdata
- Gestion des environnements

---

## Auteurs

Projet réalisé dans le cadre de la SAE 2.01 – BUT Informatique

- BODILIS Macéo
- GOBALASAMY Arvin
- GONET--PETIT Clément
- SETTOURAMAN Arthy

Année universitaire : 2025–2026  
IUT de Créteil-Vitry
![Logo de l'université Paris-est Créteil, Institut universitaire de Créteil Vitry, département informatique](/static/images/upec-iutcv_info-color.png)

## Galerie

Image du rendu du site :

|![Image de la page analyse](/static/images/Screenshot_Effectifs.png)|![Image de la page dashboard](/static/images/Screenshot_Dashboard.png)|![Image de la page a propos](/static/images/Screenshot_A_propos.png)|
|:-:|:-:|:-:|
