from database import SessionLocal
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

app = FastAPI()


# Connexion DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ROOT
@app.get("/")
def root():
    return {"message": "API Ecole OK 🚀"}


# --------------- ELEVES ---------------------

# GET /eleve/
@app.get("/eleve/")
def get_eleves(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT nom, age FROM eleve")).fetchall()
    return [{"nom": r.nom, "age": r.age} for r in result]


# GET /eleve/{id}
@app.get("/eleve/{id}")
def get_eleve(id: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM eleve")).fetchall()

    for e in result:
        if e.id == id:
            return dict(e._mapping)

    raise HTTPException(status_code=404, detail="Eleve not found")


# GET /eleve/{id}/absence
@app.get("/eleve/{id}/absence")
def get_absence(id: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM absence")).fetchall()

    total = 0
    for a in result:
        if a.eleve_id == id:
            total += a.nb_heures

    return {"eleve_id": id, "heures_absence": total}


# GET /eleve/avertis
@app.get("/eleve/avertis")
def get_eleves_avertis(db: Session = Depends(get_db)):
    eleves = db.execute(text("SELECT * FROM eleve")).fetchall()
    dossiers = db.execute(text("SELECT * FROM dossier")).fetchall()

    result = []

    for d in dossiers:
        if d.avertissement_travail or d.avertissement_comportement:
            for e in eleves:
                if e.id == d.eleve_id:
                    result.append({"nom": e.nom})

    return result


# GET /eleve/bonne_notes
@app.get("/eleve/bonne_notes")
def get_bonnes_notes(db: Session = Depends(get_db)):
    eleves = db.execute(text("SELECT * FROM eleve")).fetchall()
    notes = db.execute(text("SELECT * FROM note")).fetchall()

    result = []

    for e in eleves:
        total = 0
        count = 0

        for n in notes:
            if n.eleve_id == e.id:
                total += n.note
                count += 1

        if count > 0:
            moyenne = total / count
            if moyenne > 12:
                result.append({"nom": e.nom, "moyenne": moyenne})

    # tri Python
    result.sort(key=lambda x: x["moyenne"], reverse=True)

    return result


# --------------- NOTES ---------------------

# GET /notes/{eleve_id}
@app.get("/notes/{eleve_id}")
def get_notes_eleve(eleve_id: int, db: Session = Depends(get_db)):
    eleves = db.execute(text("SELECT * FROM eleve")).fetchall()
    notes = db.execute(text("SELECT * FROM note")).fetchall()

    result = []

    for n in notes:
        if n.eleve_id == eleve_id:
            for e in eleves:
                if e.id == eleve_id:
                    result.append({
                        "eleve": e.nom,
                        "note": n.note,
                        "matiere": n.matiere
                    })

    return result


# GET /note?par=...
@app.get("/note")
def get_notes_par(par: str, db: Session = Depends(get_db)):
    notes = db.execute(text("SELECT * FROM note")).fetchall()
    eleves = db.execute(text("SELECT * FROM eleve")).fetchall()

    result = {}

    if par == "eleve":
        for e in eleves:
            result[e.nom] = []

            for n in notes:
                if n.eleve_id == e.id:
                    result[e.nom].append({
                        "note": n.note,
                        "matiere": n.matiere
                    })

    return result


# --------------- MATIERES ---------------------

# GET /specialites/{id}/cours
@app.get("/specialites/{id}/cours")
def get_cours_specialite(id: int, db: Session = Depends(get_db)):
    cours = db.execute(text("SELECT * FROM cours")).fetchall()

    result = []

    for c in cours:
        if c.specialite_id == id:
            result.append({"cours": c.nom})

    return result


# GET /specialites/{id}/prom
@app.get("/specialites/{id}/prom")
def get_prom_specialite(id: int, db: Session = Depends(get_db)):
    promos = db.execute(text("SELECT * FROM promotion")).fetchall()

    result = []

    for p in promos:
        if p.specialite_id == id:
            result.append({"promotion": p.nom})

    return result


# --------------- PROFESSEURS ---------------------

# GET /prof/severe
@app.get("/prof/severe")
def get_prof_severe(db: Session = Depends(get_db)):
    profs = db.execute(text("SELECT * FROM prof")).fetchall()
    notes = db.execute(text("SELECT * FROM note")).fetchall()

    result = []

    for p in profs:
        total = 0
        count = 0

        for n in notes:
            if n.prof_id == p.id:
                total += n.note
                count += 1

        if count > 0:
            moyenne = total / count
            if moyenne < 8:
                result.append({"prof": p.nom, "moyenne": moyenne})

    result.sort(key=lambda x: x["moyenne"])

    return result


# --------------- BONUS ---------------------

# Eleves sans absence
@app.get("/eleve/sans_absence")
def eleve_sans_absence(db: Session = Depends(get_db)):
    eleves = db.execute(text("SELECT * FROM eleve")).fetchall()
    absences = db.execute(text("SELECT * FROM absence")).fetchall()

    result = []

    for e in eleves:
        has_absence = False

        for a in absences:
            if a.eleve_id == e.id:
                has_absence = True

        if not has_absence:
            result.append({"nom": e.nom})

    return result


# Top élève (meilleure moyenne)
@app.get("/top_eleve")
def top_eleve(db: Session = Depends(get_db)):
    eleves = db.execute(text("SELECT * FROM eleve")).fetchall()
    notes = db.execute(text("SELECT * FROM note")).fetchall()

    best = None
    best_avg = 0

    for e in eleves:
        total = 0
        count = 0

        for n in notes:
            if n.eleve_id == e.id:
                total += n.note
                count += 1

        if count > 0:
            avg = total / count
            if avg > best_avg:
                best_avg = avg
                best = e.nom

    return {"top_eleve": best, "moyenne": best_avg}
