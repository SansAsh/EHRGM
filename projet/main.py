from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from controllers import home_controller, eleve_controller, prof_controller, note_controller, specialite_controller

app = FastAPI()

# Static (CSS / JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routes
app.include_router(home_controller.router)
app.include_router(eleve_controller.router, prefix="/eleve", tags=["Élèves"])
app.include_router(prof_controller.router, prefix="/prof", tags=["Profs"])
app.include_router(note_controller.router, prefix="/note", tags=["Notes"])
app.include_router(specialite_controller.router, prefix="/specialite", tags=["Spécialités"])