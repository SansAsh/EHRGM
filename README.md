# EHRGM
Projet API - L2 - 2025-2026 - ESIEE-IT

## Groupe 4

## Objectif du projet

Ce projet a pour but de créer une API en Python permettant d’interagir avec notre base de données créer précédemment.

L’API permet :

* de consulter les données (élèves, notes, professeurs…)
* de modifier les données (CRUD)
* Authentification avec une clé api

## Technologies utilisées

* Python 3
* FastAPI
* MySQL

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/SansAsh/EHRGM.git
cd projet/api
```

### 2. Créer un environnement virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install "fastapi[standard]"
```

### 4. Configurer la base de données

Modifier le fichier `database.py` :

```python
DATABASE_URL = "mysql+pymysql://user:password@localhost/nom_bdd"
```

## Lancer l’API

```bash
uvicorn main:app --reload
```

---

## Accès

* API : http://127.0.0.1:8000
* Documentation interactive (Swagger) : http://127.0.0.1:8000/docs

---

## Authentification

L’API est sécurisée par une clé API.

### Générer une clé :

```http
GET /generate-api-key
```

Réponse :

```json
{
  "api_key": "xxxxxxxx-xxxx-xxxx"
}
```

### Utiliser la clé :

Dans chaque requête, ajouter dans les headers :

```
x-api-key: votre_cle
```

## Endpoints principaux

### Élèves

* GET /eleve/
* GET /eleve/{id}
* POST /eleve
* PUT /eleve/{id}
* DELETE /eleve/{id}

### Notes

* GET /notes/{eleve_id}
* POST /note
* PUT /note/{id}

### Professeurs

* GET /prof
* POST /prof
* PUT /prof/{id}
* DELETE /prof/{id}

### Marières

* GET /specialites/{id}/cours
* GET /specialites/{id}/prom

### Routes métier

* GET /eleve/avertis
* GET /eleve/bonne_notes
* GET /prof/severe
* GET /eleve/{id}/absence

### Bonus

* GET /eleve/sans_absence
* GET /top_eleve

## Choix techniques

* Les requêtes SQL sont volontairement simples (SELECT uniquement)
* Toute la logique métier est traitée en Python
* Authentification par clé API pour sécuriser l’accès
* API REST structurée et extensible

## Structure du projet

```
api/
│── main.py
│── database.py
│── README.md
```

## Tests

Utiliser :

* Swagger : `/docs`
* curl
* Postman


## Conclusion

Ce projet permet de mettre en pratique :

* le développement d’API REST
* la gestion de base de données
* la sécurisation d’un backend
