from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal
import uuid

app = FastAPI()

# =========================
# 🔐 GESTION API KEY
# =========================

# stockage simple (mémoire)
API_KEYS = set()

API_KEY_NAME = "x-api-key"


def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Clé API invalide")


# endpoint pour générer une clé
@app.get("/generate-api-key")
def generate_api_key():
    new_key = str(uuid.uuid4())
    API_KEYS.add(new_key)
    return {"api_key": new_key}


# =========================
# 🔌 Connexion DB
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# 🟢 ROOT (public)
# =========================

@app.get("/")
def root():
    return {"message": "API Ecole OK 🚀"}


# =========================
# 👨‍🎓 ELEVE
# =========================

@app.get("/eleve/", dependencies=[Depends(verify_api_key)])
def get_eleves(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM eleve")).fetchall()
    return [dict(r._mapping) for r in result]


@app.get("/eleve/{id}", dependencies=[Depends(verify_api_key)])
def get_eleve(id: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM eleve")).fetchall()
    for e in result:
        if e.id == id:
            return dict(e._mapping)
    raise HTTPException(status_code=404, detail="Eleve not found")


@app.post("/eleve", dependencies=[Depends(verify_api_key)])
def create_eleve(nom: str, age: int, db: Session = Depends(get_db)):
    db.execute(text("INSERT INTO eleve (nom, age) VALUES (:nom, :age)"),
               {"nom": nom, "age": age})
    db.commit()
    return {"message": "Eleve créé"}


@app.put("/eleve/{id}", dependencies=[Depends(verify_api_key)])
def update_eleve(id: int, nom: str, age: int, db: Session = Depends(get_db)):
    db.execute(text("UPDATE eleve SET nom=:nom, age=:age WHERE id=:id"),
               {"id": id, "nom": nom, "age": age})
    db.commit()
    return {"message": "Eleve modifié"}


@app.delete("/eleve/{id}", dependencies=[Depends(verify_api_key)])
def delete_eleve(id: int, db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM eleve WHERE id=:id"), {"id": id})
    db.commit()
    return {"message": "Eleve supprimé"}


# =========================
# 📝 NOTES
# =========================

@app.get("/notes/{eleve_id}", dependencies=[Depends(verify_api_key)])
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


@app.post("/note", dependencies=[Depends(verify_api_key)])
def create_note(eleve_id: int, prof_id: int, note: float, matiere: str, db: Session = Depends(get_db)):
    db.execute(text("""
        INSERT INTO note (eleve_id, prof_id, note, matiere)
        VALUES (:eleve_id, :prof_id, :note, :matiere)
    """), locals())
    db.commit()
    return {"message": "Note ajoutée"}


@app.put("/note/{id}", dependencies=[Depends(verify_api_key)])
def update_note(id: int, note: float, db: Session = Depends(get_db)):
    db.execute(text("UPDATE note SET note=:note WHERE id=:id"),
               {"id": id, "note": note})
    db.commit()
    return {"message": "Note modifiée"}


# =========================
# 👨‍🏫 PROF
# =========================

@app.get("/prof", dependencies=[Depends(verify_api_key)])
def get_profs(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM prof")).fetchall()
    return [dict(r._mapping) for r in result]


@app.post("/prof", dependencies=[Depends(verify_api_key)])
def create_prof(nom: str, db: Session = Depends(get_db)):
    db.execute(text("INSERT INTO prof (nom) VALUES (:nom)"), {"nom": nom})
    db.commit()
    return {"message": "Prof créé"}


@app.put("/prof/{id}", dependencies=[Depends(verify_api_key)])
def update_prof(id: int, nom: str, db: Session = Depends(get_db)):
    db.execute(text("UPDATE prof SET nom=:nom WHERE id=:id"),
               {"id": id, "nom": nom})
    db.commit()
    return {"message": "Prof modifié"}


@app.delete("/prof/{id}", dependencies=[Depends(verify_api_key)])
def delete_prof(id: int, db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM prof WHERE id=:id"), {"id": id})
    db.commit()
    return {"message": "Prof supprimé"}
