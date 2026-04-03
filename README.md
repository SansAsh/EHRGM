# EHRGM
Projet API - L2 - 2025-2026 - ESIEE-IT

## Prérequis

- Python 3.10+
- MySQL avec la base `ehrgm` importée
- `pip`
- Fast api

## Lancer l'API

```bash
cd /chemin/du/projet
pip install -r requirements.txt

uvicorn main:app --reload
```

L'API sera disponible sur **http://127.0.0.1:8000**

Documentation interactive : **http://127.0.0.1:8000/docs**

## Lancer l'interface d'administration

```bash
cd admin
python admin.py
```
## Organisation du code

### `api/`

| Fichier | Rôle |
|---|---|
| `database.py` | Connexion MySQL + helpers `fetch_all`, `fetch_one`, `execute` |
| `main.py` | Application FastAPI – tous les endpoints |

#### Règles respectées (consignes)
- Tout traitement (calcul de moyennes, tri, filtrage, groupement) est fait en **Python**
- Les requêtes SQL utilisent uniquement `SELECT`, `FROM`, `JOIN`

### `admin/`

| Fichier | Rôle |
|---|---|
| `admin.py` | Interface CLI complète avec menus interactifs |

L'interface passe **toujours par l'API** via `requests` (GET, POST, PUT, DELETE). Elle ne se connecte jamais directement à la base de données.

## Endpoints API

### Élèves
| Méthode | Route | Description |
|---|---|---|
| GET | `/eleve/` | Liste tous les élèves |
| GET | `/eleve/{id}` | Détail d'un élève |
| GET | `/eleve/avertis` | Élèves avec avertissement |
| GET | `/eleve/bonne_notes` | Élèves avec moyenne > 12 (triés) |
| GET | `/eleve/{id}/absence` | Heures d'absence d'un élève |
| POST | `/eleve/` | Créer un élève |
| PUT | `/eleve/{id}` | Modifier un élève |
| DELETE | `/eleve/{id}` | Supprimer un élève |

### Notes
| Méthode | Route | Description |
|---|---|---|
| GET | `/notes/{eleve_id}` | Notes d'un élève |
| GET | `/note?par=eleve\|prof\|cours\|promotion` | Notes groupées par type |
| GET | `/notes/` | Toutes les notes |
| GET | `/note/{id}` | Détail d'une note |
| POST | `/note/` | Créer une note |
| PUT | `/note/{id}` | Modifier une note (uniquement à la hausse) |

### Professeurs
| Méthode | Route | Description |
|---|---|---|
| GET | `/prof/` | Liste des profs |
| GET | `/prof/{id}` | Détail d'un prof |
| GET | `/prof/severe` | Profs dont la moyenne des notes données < 8 |
| POST | `/prof/` | Créer un prof |
| PUT | `/prof/{id}` | Modifier un prof |
| DELETE | `/prof/{id}` | Supprimer un prof |

### Matières
| Méthode | Route | Description |
|---|---|---|
| GET | `/specialites/{id}/cours` | Cours d'une spécialité |
| GET | `/specialites/{id}/prom` | Promotions d'une spécialité |

### Cours
| Méthode | Route | Description |
|---|---|---|
| GET | `/instance_cours/` | Toutes les instances |
| GET | `/instance_cours/{id}` | Détail |
| POST | `/instance_cours/` | Créer |
| PUT | `/instance_cours/{id}` | Modifier |
| DELETE | `/instance_cours/{id}` | Supprimer |

### Dossiers
| Méthode | Route | Description |
|---|---|---|
| GET | `/dossier/{eleve_id}` | Voir le dossier d'un élève |
| PUT | `/dossier/{eleve_id}` | Modifier le dossier |

## Fonctionnalité supplémentaire : Clubs Sportifs

Gestion complète des clubs sportifs avec CRUD et deux endpoints GET analytiques :

| Méthode | Route | Description |
|---|---|---|
| GET | `/clubs/` | Liste des clubs avec sport et responsable |
| GET | `/clubs/{id}/membres` | Membres d'un club (triés : capitaines en premier) |
| GET | `/clubs/{id}/stats` | Stats : membres, événements, participations |
| POST | `/clubs/` | Créer un club |
| PUT | `/clubs/{id}` | Modifier un club |
| DELETE | `/clubs/{id}` | Supprimer un club |
| POST | `/clubs/{id}/membres` | Ajouter un membre |
| DELETE | `/clubs/{club_id}/membres/{eleve_id}` | Retirer un membre |
