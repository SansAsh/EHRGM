from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal

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


# =========================
# 👨‍🎓 ELEVE (CRUD)
# =========================

@app.get("/eleve/")
def get_eleves(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM eleve")).fetchall()
    return [dict(r._mapping) for r in result]


@app.get("/eleve/{id}")
def get_eleve(id: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM eleve")).fetchall()
    for e in result:
        if e.id == id:
            return dict(e._mapping)
    raise HTTPException(status_code=404, detail="Eleve not found")


@app.post("/eleve")
def create_eleve(nom: str, age: int, db: Session = Depends(get_db)):
    db.execute(text("INSERT INTO eleve (nom, age) VALUES (:nom, :age)"),
               {"nom": nom, "age": age})
    db.commit()
    return {"message": "Eleve créé"}


@app.put("/eleve/{id}")
def update_eleve(id: int, nom: str, age: int, db: Session = Depends(get_db)):
    db.execute(text("UPDATE eleve SET nom=:nom, age=:age WHERE id=:id"),
               {"id": id, "nom": nom, "age": age})
    db.commit()
    return {"message": "Eleve modifié"}


@app.delete("/eleve/{id}")
def delete_eleve(id: int, db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM eleve WHERE id=:id"), {"id": id})
    db.commit()
    return {"message": "Eleve supprimé"}


# =========================
# 📝 NOTES
# =========================

@app.get("/notes/{eleve_id}")
def get_notes(eleve_id: int, db: Session = Depends(get_db)):
    notes = db.execute(text("SELECT * FROM note")).fetchall()
    eleves = db.execute(text("SELECT * FROM eleve")).fetchall()

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


@app.post("/note")
def create_note(eleve_id: int, prof_id: int, note: float, matiere: str, db: Session = Depends(get_db)):
    db.execute(text("""
        INSERT INTO note (eleve_id, prof_id, note, matiere)
        VALUES (:eleve_id, :prof_id, :note, :matiere)
    """), locals())
    db.commit()
    return {"message": "Note ajoutée"}


@app.put("/note/{id}")
def update_note(id: int, note: float, db: Session = Depends(get_db)):
    db.execute(text("UPDATE note SET note=:note WHERE id=:id"),
               {"id": id, "note": note})
    db.commit()
    return {"message": "Note modifiée"}


# =========================
# 📚 SPECIALITES
# =========================

@app.get("/specialites/{id}/cours")
def get_cours(id: int, db: Session = Depends(get_db)):
    cours = db.execute(text("SELECT * FROM cours")).fetchall()
    return [{"nom": c.nom} for c in cours if c.specialite_id == id]


@app.get("/specialites/{id}/prom")
def get_prom(id: int, db: Session = Depends(get_db)):
    promos = db.execute(text("SELECT * FROM promotion")).fetchall()
    return [{"nom": p.nom} for p in promos if p.specialite_id == id]


# =========================
# 👨‍🏫 PROF
# =========================

@app.get("/prof")
def get_profs(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM prof")).fetchall()
    return [dict(r._mapping) for r in result]


@app.post("/prof")
def create_prof(nom: str, db: Session = Depends(get_db)):
    db.execute(text("INSERT INTO prof (nom) VALUES (:nom)"), {"nom": nom})
    db.commit()
    return {"message": "Prof créé"}


@app.put("/prof/{id}")
def update_prof(id: int, nom: str, db: Session = Depends(get_db)):
    db.execute(text("UPDATE prof SET nom=:nom WHERE id=:id"),
               {"id": id, "nom": nom})
    db.commit()
    return {"message": "Prof modifié"}


@app.delete("/prof/{id}")
def delete_prof(id: int, db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM prof WHERE id=:id"), {"id": id})
    db.commit()
    return {"message": "Prof supprimé"}
