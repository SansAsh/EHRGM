from fastapi import FastAPI
from services.eleves_service import *
from services.notes_service import *
from services.profs_service import *

app = FastAPI()

# ELEVE
@app.get("/eleve/")
def eleves():
    return get_all_eleves()

@app.get("/eleve/{id}")
def eleve(id: int):
    return get_eleve_by_id(id)

@app.get("/eleve/avertis")
def avertis():
    return get_eleves_avertis()

@app.get("/eleve/bonne_notes")
def bonnes_notes():
    return get_bonne_notes()

@app.get("/eleve/{id}/absence")
def absence(id: int):
    return get_absence_eleve(id)

@app.post("/eleve/")
def add_eleve(eleve: dict):
    return create_eleve(
        eleve["nom"],
        eleve["email"],
        eleve["age"],
        eleve["promotion_id"]
    )

@app.delete("/eleve/{id}")
def remove_eleve(id: int):
    return delete_eleve(id)


# NOTES
@app.get("/notes/{eleve_id}")
def notes(eleve_id: int):
    return get_notes_by_eleve(eleve_id)

@app.get("/note")
def notes_par(type: str):
    return get_notes_par(type)


# PROF
@app.get("/prof/severe")
def prof_severe():
    return get_prof_severe()