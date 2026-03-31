from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from services.eleves_service import *

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class Eleve(BaseModel):
    nom: str
    email: str
    age: int
    promotion_id: int

@router.get("/", response_model=list)
async def get_eleves():
    return get_all_eleves()

@router.post("/")
async def create_eleve(eleve: Eleve):
    return create_eleve(eleve.nom, eleve.email, eleve.age, eleve.promotion_id)

@router.get("/template", response_class=HTMLResponse)
async def get_eleve_template(request: Request):
    return templates.TemplateResponse("eleve/index.html", {"request": request})