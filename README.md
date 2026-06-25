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
├── app.py                 # Point d’entrée Flask
├── config.py             # Configuration globale
├── wsgi.py               # Déploiement WSGI
├── requirements.txt      # Dépendances
├── .env                  # Variables d’environnement
│
├── controllers/          # Routes Flask (couche contrôle)
│   ├── accueil.py
│   ├── dashboard.py
│   ├── effectifs.py
│   ├── honoraires.py
│   ├── prescriptions.py
│   ├── comparaison.py
│   ├── about.py
│   ├── login.py
│   └── api.py
│
├── models/               # Accès aux données
│   ├── db.py
│   ├── dimensions.py
│   └── data_utils.py
│
├── services/             # Logique métier + API externes
│   ├── ameli_api.py
│   ├── cached_ameli_api.py
│   ├── redis_cached_ameli_api.py
│   └── comparaison_service.py
│
├── utils/                # Outils et constantes
│   ├── constants.py
│   └── user.py
│
├── templates/            # Vues Jinja2
│   ├── base.html
│   ├── accueil.html
│   ├── dashboard.html
│   ├── effectifs.html
│   ├── honoraires.html
│   ├── prescriptions.html
│   ├── comparaison.html
│   ├── about.html
│   ├── login.html
│   └── erreur.html
│
├── static/               # Ressources statiques
│   ├── css/
│   ├── js/
│   ├── images/
│   ├── csv/
│   └── geojson/
│
├── scripts/
│   └── create_user_table.py
│
├── tests/
│   ├── test_cached_ameli_api.py
│   ├── test_redis_cached_ameli_api.py
│   └── test_ameli_api.py
```

---

## Fonctionnalités principales

### Consultation des données
L’application permet l’exploration de données statistiques :
- effectifs par spécialité, département et année,
- montants des honoraires,
- prescriptions médicales,
- tableau de bord global de synthèse.

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
```
http://localhost:5000
```

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
```