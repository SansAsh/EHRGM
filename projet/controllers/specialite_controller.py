from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from services.specialite_service import *

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# PAGE AVEC FORMULAIRE
@router.get("/", response_class=HTMLResponse)
def specialite_page(request: Request):
    return templates.TemplateResponse("specialiter/index.html", {
        "request": request
    })


# PAGE RESULTAT
@router.get("/{id}", response_class=HTMLResponse)
def specialite_detail(request: Request, id: int):

    cours = get_cours_by_specialite(id)
    promotions = get_promotions_by_specialite(id)

    return templates.TemplateResponse("specialiter/index.html", {
        "request": request,
        "cours": cours,
        "promotions": promotions,
        "id": id
    })