import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Import des controllers
from controllers.front_controller import router as front_router

# Import des services
from services.eleves_service import *
from services.notes_service import *
from services.profs_service import *

app = FastAPI(title="Gestion Élèves - FastAPI")

# ----------------------------
# Montée des fichiers statiques
# ----------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# ----------------------------
# Routes front
# ----------------------------
app.include_router(front_router)

# ----------------------------
# Routes API
# ----------------------------
@app.get("/eleve/")
def route_all_eleves():
    return get_all_eleves()

@app.get("/eleve/{eleve_id}")
def route_eleve_by_id(eleve_id: int):
    return get_eleve_by_id(eleve_id)

@app.get("/eleve/avertis")
def route_eleves_avertis():
    return get_eleves_avertis()

@app.get("/eleve/bonne_notes")
def route_bonne_notes():
    return get_bonne_notes()

@app.get("/eleve/{eleve_id}/absence")
def route_absence(eleve_id: int):
    return get_absence_eleve(eleve_id)

@app.post("/eleve/")
def route_create_eleve(eleve: dict):
    return create_eleve(
        eleve["nom"],
        eleve["email"],
        eleve["age"],
        eleve["promotion_id"]
    )

@app.put("/eleve/{eleve_id}")
def route_update_eleve(eleve_id: int, eleve: dict):
    return update_eleve(
        eleve_id,
        eleve["nom"],
        eleve["email"],
        eleve["age"],
        eleve["promotion_id"]
    )

@app.delete("/eleve/{eleve_id}")
def route_delete_eleve(eleve_id: int):
    return delete_eleve(eleve_id)

@app.get("/notes/{eleve_id}")
def route_notes_eleve(eleve_id: int):
    return get_notes_by_eleve(eleve_id)

@app.get("/note")
def route_notes_par(par: str):
    return get_notes_par(par)

@app.get("/prof/severe")
def route_prof_severe():
    return get_prof_severe()