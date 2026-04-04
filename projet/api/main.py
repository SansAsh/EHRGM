from typing import Optional

from database import execute, fetch_all, fetch_one
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

app = FastAPI(title="API École", version="1.0.0")

security = HTTPBearer()

FAKE_TOKEN = "mon-super-token-secret"

def verifier_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != FAKE_TOKEN:
        raise HTTPException(status_code=401, detail="Token invalide")

# ----------------- Création des class -----------------

class EleveCreate(BaseModel):
    nom: str
    email: str
    age: int
    promotion_id: Optional[int] = None

class EleveUpdate(BaseModel):
    nom: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    promotion_id: Optional[int] = None

class ProfCreate(BaseModel):
    nom: str
    email: str
    age: int

class ProfUpdate(BaseModel):
    nom: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

class NoteCreate(BaseModel):
    eleve_id: int
    cours_id: int
    prof_id: int
    note: float

class NoteUpdate(BaseModel):
    note: float

class DossierUpdate(BaseModel):
    infos: Optional[str] = None
    avertissement_travail: Optional[int] = None
    avertissement_comportement: Optional[int] = None

class InstanceCoursCreate(BaseModel):
    cours_id: int
    prof_id: int
    date: str

class InstanceCoursUpdate(BaseModel):
    cours_id: Optional[int] = None
    prof_id: Optional[int] = None
    date: Optional[str] = None

class ClubCreate(BaseModel):
    nom: str
    sport_id: int
    responsable_id: Optional[int] = None
    date_creation: Optional[str] = None
    nb_membres_max: Optional[int] = None

class ClubUpdate(BaseModel):
    nom: Optional[str] = None
    sport_id: Optional[int] = None
    responsable_id: Optional[int] = None
    nb_membres_max: Optional[int] = None

class ClubEleveCreate(BaseModel):
    eleve_id: int
    role: Optional[str] = "membre"

# --------------------- Fonctions utilitaires --------------------

def calculer_moyenne(notes: list) -> Optional[float]:
    valeurs = [float(n["note"]) for n in notes if n["note"] is not None]
    if not valeurs:
        return None
    return sum(valeurs) / len(valeurs)

def trier_par_moyenne(eleves_moyennes: list, reverse=True) -> list:
    return sorted(eleves_moyennes, key=lambda x: x["moyenne"] if x["moyenne"] is not None else -1, reverse=reverse)

def grouper_notes_par(notes: list, champ: str) -> dict:
    result = {}
    for n in notes:
        cle = n[champ]
        if cle not in result:
            result[cle] = []
        result[cle].append({
            "nomEleve": n["nomEleve"],
            "nomProf": n["nomProf"],
            "promotion": n["promotion"],
            "cours": n["cours"],
            "note": float(n["note"]) if n["note"] is not None else None
        })
    return result

def filtrer_avertis(eleves_dossiers: list) -> list:
    return [
        e for e in eleves_dossiers
        if e["avertissement_travail"] or e["avertissement_comportement"]
    ]

def calculer_heures_absence(absences: list) -> int:
    return sum(a["duree_minutes"] for a in absences if a["duree_minutes"])

# ------------- Login --------------------------

@app.post("/login")
def login(username: str, password: str):
    if username == "admin" and password == "1234":
        return {"token": FAKE_TOKEN}
    raise HTTPException(status_code=401, detail="Identifiants invalides")

# ------------- GET eleves ---------------------
# IMPORTANT : les routes statiques (/avertis, /bonne_notes) doivent être
# déclarées AVANT la route dynamique (/eleve/{id}), sinon FastAPI
# interprète "avertis" et "bonne_notes" comme des valeurs d'ID.

@app.get("/eleve/avertis")
def eleves_avertis(credentials=Depends(verifier_token)):
    rows = fetch_all(
        "SELECT e.id, e.nom, e.age, d.avertissement_travail, d.avertissement_comportement "
        "FROM eleve e JOIN dossier d ON e.id = d.eleve_id"
    )
    return filtrer_avertis(rows)

@app.get("/eleve/bonne_notes")
def eleves_bonne_notes(credentials=Depends(verifier_token)):
    eleves = fetch_all("SELECT id, nom FROM eleve")
    notes = fetch_all("SELECT eleve_id, note FROM note")
    moyennes = []
    for eleve in eleves:
        notes_eleve = [n for n in notes if n["eleve_id"] == eleve["id"]]
        moy = calculer_moyenne(notes_eleve)
        if moy is not None and moy > 12:
            moyennes.append({"id": eleve["id"], "nom": eleve["nom"], "moyenne": round(moy, 2)})
    return trier_par_moyenne(moyennes)

@app.get("/eleve/")
def liste_eleves(credentials=Depends(verifier_token)):
    rows = fetch_all("SELECT id, nom, age FROM eleve")
    return rows

@app.get("/eleve/{id}/absence")
def heures_absence_eleve(id: int, credentials=Depends(verifier_token)):
    eleve = fetch_one("SELECT id, nom FROM eleve WHERE id = %s", (id,))
    if not eleve:
        raise HTTPException(status_code=404, detail="Élève introuvable")
    absences = fetch_all("SELECT duree_minutes FROM absence WHERE eleve_id = %s", (id,))
    total_minutes = calculer_heures_absence(absences)
    heures = total_minutes // 60
    minutes = total_minutes % 60
    return {
        "eleve": eleve["nom"],
        "total_minutes": total_minutes,
        "heures": heures,
        "minutes": minutes,
        "affichage": f"{heures}h{minutes:02d}"
    }

@app.get("/eleve/{id}")
def get_eleve(id: int, credentials=Depends(verifier_token)):
    row = fetch_one("SELECT id, nom, email, age, promotion_id FROM eleve WHERE id = %s", (id,))
    if not row:
        raise HTTPException(status_code=404, detail="Élève introuvable")
    return row

# ------------- GET notes ---------------------
# Même règle : /notes/ et /note (query) avant /note/{id}

@app.get("/notes/")
def liste_notes(credentials=Depends(verifier_token)):
    rows = fetch_all("SELECT id, eleve_id, cours_id, prof_id, note FROM note")
    return [{"id": r["id"], "eleve_id": r["eleve_id"], "cours_id": r["cours_id"],
             "prof_id": r["prof_id"], "note": float(r["note"])} for r in rows]

@app.get("/notes/{eleve_id}")
def notes_eleve(eleve_id: int, credentials=Depends(verifier_token)):
    eleve = fetch_one("SELECT nom FROM eleve WHERE id = %s", (eleve_id,))
    if not eleve:
        raise HTTPException(status_code=404, detail="Élève introuvable")
    rows = fetch_all(
        "SELECT n.note, c.nom AS matiere, e.nom AS nom_eleve "
        "FROM note n "
        "JOIN cours c ON n.cours_id = c.id "
        "JOIN eleve e ON n.eleve_id = e.id "
        "WHERE n.eleve_id = %s",
        (eleve_id,)
    )
    return [{"note": float(r["note"]), "matiere": r["matiere"], "nom_eleve": r["nom_eleve"]} for r in rows]

@app.get("/note")
def notes_par(par: str = Query(..., description="eleve, prof, cours, promotion"), credentials=Depends(verifier_token)):
    valeurs_valides = ["eleve", "prof", "cours", "promotion"]
    if par not in valeurs_valides:
        raise HTTPException(status_code=400, detail=f"Valeur invalide. Choisir parmi : {valeurs_valides}")
    rows = fetch_all(
        "SELECT e.nom AS nomEleve, p.nom AS nomProf, pr.annee AS promotion, "
        "c.nom AS cours, n.note "
        "FROM note n "
        "JOIN eleve e ON n.eleve_id = e.id "
        "JOIN prof p ON n.prof_id = p.id "
        "JOIN cours c ON n.cours_id = c.id "
        "JOIN eleve el2 ON n.eleve_id = el2.id "
        "JOIN promotion pr ON el2.promotion_id = pr.id"
    )
    champ_map = {
        "eleve": "nomEleve",
        "prof": "nomProf",
        "cours": "cours",
        "promotion": "promotion"
    }
    champ = champ_map[par]
    for r in rows:
        r["promotion"] = str(r["promotion"])
    return grouper_notes_par(rows, champ)

@app.get("/note/{id}")
def get_note(id: int, credentials=Depends(verifier_token)):
    row = fetch_one("SELECT id, eleve_id, cours_id, prof_id, note FROM note WHERE id = %s", (id,))
    if not row:
        raise HTTPException(status_code=404, detail="Note introuvable")
    row["note"] = float(row["note"])
    return row

# ------------- GET professeurs ---------------------
# /prof/severe AVANT /prof/{id}

@app.get("/prof/severe")
def profs_severes(credentials=Depends(verifier_token)):
    profs = fetch_all("SELECT id, nom FROM prof")
    notes = fetch_all("SELECT prof_id, note FROM note")
    result = []
    for prof in profs:
        notes_prof = [n for n in notes if n["prof_id"] == prof["id"]]
        moy = calculer_moyenne(notes_prof)
        if moy is not None and moy < 8:
            result.append({"id": prof["id"], "nom": prof["nom"], "moyenne_notes_donnees": round(moy, 2)})
    return sorted(result, key=lambda x: x["moyenne_notes_donnees"])

@app.get("/prof/")
def liste_profs(credentials=Depends(verifier_token)):
    return fetch_all("SELECT id, nom, age, email FROM prof")

@app.get("/prof/{id}")
def get_prof(id: int, credentials=Depends(verifier_token)):
    row = fetch_one("SELECT id, nom, email, age FROM prof WHERE id = %s", (id,))
    if not row:
        raise HTTPException(status_code=404, detail="Professeur introuvable")
    return row

# ------------- GET spécialités ---------------------

@app.get("/specialites/{id}/cours")
def cours_par_specialite(id: int, credentials=Depends(verifier_token)):
    return fetch_all("SELECT c.id, c.nom, c.niveau FROM cours c WHERE c.specialite_id = %s", (id,))

@app.get("/specialites/{id}/prom")
def promotions_par_specialite(id: int, credentials=Depends(verifier_token)):
    return fetch_all("SELECT p.id, p.annee FROM promotion p WHERE p.specialite_id = %s", (id,))

# ------------- GET clubs ---------------------

@app.get("/clubs/")
def liste_clubs(credentials=Depends(verifier_token)):
    rows = fetch_all(
        "SELECT cl.id, cl.nom, cl.nb_membres_max, cl.date_creation, "
        "s.nom AS sport, p.nom AS responsable "
        "FROM club cl "
        "JOIN sport s ON cl.sport_id = s.id "
        "LEFT JOIN prof p ON cl.responsable_id = p.id"
    )
    return rows

@app.get("/clubs/{id}/membres")
def membres_club(id: int, credentials=Depends(verifier_token)):
    club = fetch_one("SELECT id, nom FROM club WHERE id = %s", (id,))
    if not club:
        raise HTTPException(status_code=404, detail="Club introuvable")
    membres = fetch_all(
        "SELECT e.id, e.nom, ce.role, ce.date_adhesion "
        "FROM club_eleve ce JOIN eleve e ON ce.eleve_id = e.id "
        "WHERE ce.club_id = %s",
        (id,)
    )
    ordre = {"capitaine": 0, "coach": 1, "membre": 2}
    membres_tries = sorted(membres, key=lambda m: ordre.get(m["role"], 99))
    return {"club": club["nom"], "membres": membres_tries}

@app.get("/clubs/{id}/stats")
def stats_club(id: int, credentials=Depends(verifier_token)):
    club = fetch_one("SELECT id, nom FROM club WHERE id = %s", (id,))
    if not club:
        raise HTTPException(status_code=404, detail="Club introuvable")
    membres = fetch_all("SELECT eleve_id FROM club_eleve WHERE club_id = %s", (id,))
    evenements = fetch_all("SELECT id FROM evenement WHERE club_id = %s", (id,))
    participations = []
    for eid in [e["id"] for e in evenements]:
        participations.extend(fetch_all("SELECT id FROM participation_evenement WHERE evenement_id = %s", (eid,)))
    return {
        "club": club["nom"],
        "nb_membres": len(membres),
        "nb_evenements": len(evenements),
        "total_participations": len(participations)
    }

# ------------- CRUD élèves ---------------------

@app.post("/eleve/", status_code=201)
def creer_eleve(eleve: EleveCreate, credentials=Depends(verifier_token)):
    new_id = execute(
        "INSERT INTO eleve (nom, email, age, promotion_id) VALUES (%s, %s, %s, %s)",
        (eleve.nom, eleve.email, eleve.age, eleve.promotion_id)
    )
    return {"id": new_id, **eleve.dict()}

@app.put("/eleve/{id}")
def modifier_eleve(id: int, eleve: EleveUpdate, credentials=Depends(verifier_token)):
    existing = fetch_one("SELECT id FROM eleve WHERE id = %s", (id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Élève introuvable")
    fields = {k: v for k, v in eleve.dict().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="Aucun champ à modifier")
    set_clause = ", ".join(f"{k} = %s" for k in fields)
    execute(f"UPDATE eleve SET {set_clause} WHERE id = %s", (*fields.values(), id))
    return fetch_one("SELECT id, nom, email, age, promotion_id FROM eleve WHERE id = %s", (id,))

@app.delete("/eleve/{id}")
def supprimer_eleve(id: int, credentials=Depends(verifier_token)):
    existing = fetch_one("SELECT id FROM eleve WHERE id = %s", (id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Élève introuvable")
    execute("DELETE FROM eleve WHERE id = %s", (id,))
    return {"detail": "Élève supprimé"}

# ------------- CRUD professeurs ---------------------

@app.post("/prof/", status_code=201)
def creer_prof(prof: ProfCreate, credentials=Depends(verifier_token)):
    new_id = execute(
        "INSERT INTO prof (nom, email, age) VALUES (%s, %s, %s)",
        (prof.nom, prof.email, prof.age)
    )
    return {"id": new_id, **prof.dict()}

@app.put("/prof/{id}")
def modifier_prof(id: int, prof: ProfUpdate, credentials=Depends(verifier_token)):
    existing = fetch_one("SELECT id FROM prof WHERE id = %s", (id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Professeur introuvable")
    fields = {k: v for k, v in prof.dict().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="Aucun champ à modifier")
    set_clause = ", ".join(f"{k} = %s" for k in fields)
    execute(f"UPDATE prof SET {set_clause} WHERE id = %s", (*fields.values(), id))
    return fetch_one("SELECT id, nom, email, age FROM prof WHERE id = %s", (id,))

@app.delete("/prof/{id}")
def supprimer_prof(id: int, credentials=Depends(verifier_token)):
    existing = fetch_one("SELECT id FROM prof WHERE id = %s", (id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Professeur introuvable")
    execute("DELETE FROM prof WHERE id = %s", (id,))
    return {"detail": "Professeur supprimé"}

# ------------- CRUD notes ---------------------

@app.post("/note/", status_code=201)
def creer_note(note: NoteCreate, credentials=Depends(verifier_token)):
    if note.note < 0 or note.note > 20:
        raise HTTPException(status_code=400, detail="La note doit être entre 0 et 20")
    new_id = execute(
        "INSERT INTO note (eleve_id, cours_id, prof_id, note) VALUES (%s, %s, %s, %s)",
        (note.eleve_id, note.cours_id, note.prof_id, note.note)
    )
    return {"id": new_id, **note.dict()}

@app.put("/note/{id}")
def modifier_note(id: int, note: NoteUpdate, credentials=Depends(verifier_token)):
    existing = fetch_one("SELECT id, note FROM note WHERE id = %s", (id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Note introuvable")
    if note.note < float(existing["note"]):
        raise HTTPException(status_code=400, detail="Impossible de baisser une note (règle BDD)")
    execute("UPDATE note SET note = %s WHERE id = %s", (note.note, id))
    return fetch_one("SELECT id, eleve_id, cours_id, prof_id, note FROM note WHERE id = %s", (id,))

# ------------- CRUD dossiers ---------------------

@app.get("/dossier/{eleve_id}")
def get_dossier(eleve_id: int, credentials=Depends(verifier_token)):
    row = fetch_one(
        "SELECT d.id, d.eleve_id, e.nom AS nom_eleve, d.infos, "
        "d.avertissement_travail, d.avertissement_comportement "
        "FROM dossier d JOIN eleve e ON d.eleve_id = e.id "
        "WHERE d.eleve_id = %s",
        (eleve_id,)
    )
    if not row:
        raise HTTPException(status_code=404, detail="Dossier introuvable")
    return row

@app.put("/dossier/{eleve_id}")
def modifier_dossier(eleve_id: int, dossier: DossierUpdate, credentials=Depends(verifier_token)):
    existing = fetch_one("SELECT id FROM dossier WHERE eleve_id = %s", (eleve_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Dossier introuvable")
    fields = {k: v for k, v in dossier.dict().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="Aucun champ à modifier")
    set_clause = ", ".join(f"{k} = %s" for k in fields)
    execute(f"UPDATE dossier SET {set_clause} WHERE eleve_id = %s", (*fields.values(), eleve_id))
    return fetch_one("SELECT * FROM dossier WHERE eleve_id = %s", (eleve_id,))

# ------------- CRUD instance_cours ---------------------

@app.get("/instance_cours/")
def liste_instances_cours(credentials=Depends(verifier_token)):
    rows = fetch_all(
        "SELECT ic.id, c.nom AS cours, p.nom AS prof, ic.date "
        "FROM instance_cours ic "
        "JOIN cours c ON ic.cours_id = c.id "
        "JOIN prof p ON ic.prof_id = p.id"
    )
    return rows

@app.get("/instance_cours/{id}")
def get_instance_cours(id: int, credentials=Depends(verifier_token)):
    row = fetch_one("SELECT id, cours_id, prof_id, date FROM instance_cours WHERE id = %s", (id,))
    if not row:
        raise HTTPException(status_code=404, detail="Instance de cours introuvable")
    return row

@app.post("/instance_cours/", status_code=201)
def creer_instance_cours(instance: InstanceCoursCreate, credentials=Depends(verifier_token)):
    new_id = execute(
        "INSERT INTO instance_cours (cours_id, prof_id, date) VALUES (%s, %s, %s)",
        (instance.cours_id, instance.prof_id, instance.date)
    )
    return {"id": new_id, **instance.dict()}

@app.put("/instance_cours/{id}")
def modifier_instance_cours(id: int, instance: InstanceCoursUpdate, credentials=Depends(verifier_token)):
    existing = fetch_one("SELECT id FROM instance_cours WHERE id = %s", (id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Instance de cours introuvable")
    fields = {k: v for k, v in instance.dict().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="Aucun champ à modifier")
    set_clause = ", ".join(f"{k} = %s" for k in fields)
    execute(f"UPDATE instance_cours SET {set_clause} WHERE id = %s", (*fields.values(), id))
    return fetch_one("SELECT id, cours_id, prof_id, date FROM instance_cours WHERE id = %s", (id,))

@app.delete("/instance_cours/{id}")
def supprimer_instance_cours(id: int, credentials=Depends(verifier_token)):
    existing = fetch_one("SELECT id FROM instance_cours WHERE id = %s", (id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Instance de cours introuvable")
    execute("DELETE FROM instance_cours WHERE id = %s", (id,))
    return {"detail": "Instance de cours supprimée"}

# ------------- CRUD clubs ---------------------

@app.post("/clubs/", status_code=201)
def creer_club(club: ClubCreate, credentials=Depends(verifier_token)):
    new_id = execute(
        "INSERT INTO club (nom, sport_id, responsable_id, date_creation, nb_membres_max) "
        "VALUES (%s, %s, %s, %s, %s)",
        (club.nom, club.sport_id, club.responsable_id, club.date_creation, club.nb_membres_max)
    )
    return {"id": new_id, **club.dict()}

@app.put("/clubs/{id}")
def modifier_club(id: int, club: ClubUpdate, credentials=Depends(verifier_token)):
    existing = fetch_one("SELECT id FROM club WHERE id = %s", (id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Club introuvable")
    fields = {k: v for k, v in club.dict().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="Aucun champ à modifier")
    set_clause = ", ".join(f"{k} = %s" for k in fields)
    execute(f"UPDATE club SET {set_clause} WHERE id = %s", (*fields.values(), id))
    return fetch_one("SELECT * FROM club WHERE id = %s", (id,))

@app.delete("/clubs/{id}")
def supprimer_club(id: int, credentials=Depends(verifier_token)):
    existing = fetch_one("SELECT id FROM club WHERE id = %s", (id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Club introuvable")
    execute("DELETE FROM club WHERE id = %s", (id,))
    return {"detail": "Club supprimé"}

@app.post("/clubs/{id}/membres", status_code=201)
def ajouter_membre_club(id: int, membre: ClubEleveCreate, credentials=Depends(verifier_token)):
    club = fetch_one("SELECT id FROM club WHERE id = %s", (id,))
    if not club:
        raise HTTPException(status_code=404, detail="Club introuvable")
    execute(
        "INSERT INTO club_eleve (club_id, eleve_id, role) VALUES (%s, %s, %s)",
        (id, membre.eleve_id, membre.role)
    )
    return {"detail": "Membre ajouté"}

@app.delete("/clubs/{club_id}/membres/{eleve_id}")
def retirer_membre_club(club_id: int, eleve_id: int, credentials=Depends(verifier_token)):
    existing = fetch_one(
        "SELECT * FROM club_eleve WHERE club_id = %s AND eleve_id = %s",
        (club_id, eleve_id)
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Membre introuvable dans ce club")
    execute("DELETE FROM club_eleve WHERE club_id = %s AND eleve_id = %s", (club_id, eleve_id))
    return {"detail": "Membre retiré du club"}

# ------------- Routes utilitaires ---------------------

@app.get("/cours/")
def liste_cours(credentials=Depends(verifier_token)):
    return fetch_all(
        "SELECT c.id, c.nom, c.niveau, s.nom AS specialite "
        "FROM cours c LEFT JOIN specialite s ON c.specialite_id = s.id"
    )

@app.get("/promotions/")
def liste_promotions(credentials=Depends(verifier_token)):
    return fetch_all(
        "SELECT p.id, p.annee, s.nom AS specialite "
        "FROM promotion p LEFT JOIN specialite s ON p.specialite_id = s.id"
    )

@app.get("/specialites/")
def liste_specialites(credentials=Depends(verifier_token)):
    return fetch_all("SELECT id, nom FROM specialite")

@app.get("/sports/")
def liste_sports(credentials=Depends(verifier_token)):
    return fetch_all("SELECT id, nom, nb_joueurs_max FROM sport")
