from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from controllers import eleve_controller
from controllers import home_controller

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(home_controller.router)
app.include_router(eleve_controller.router, prefix="/eleve", tags=["Élèves"])