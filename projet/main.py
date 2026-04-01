from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from controllers import home_controller, eleve_controller

app = FastAPI()

# Static (CSS / JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routes
app.include_router(home_controller.router)
app.include_router(eleve_controller.router, prefix="/eleve", tags=["Élèves"])