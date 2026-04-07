from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse, RedirectResponse
from services.dossier_services import get_all_dossiers, get_dossier_by_eleve, update_dossier

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# -------- LISTE DES DOSSIERS --------
@router.get("/", response_class=HTMLResponse)
def dossiers_page(request: Request):
    dossiers = get_all_dossiers()
    return templates.TemplateResponse("dossier/index.html", {
        "request": request,
        "dossiers": dossiers
    })

# -------- EDIT / MODIFIER UN DOSSIER --------
@router.get("/{eleve_id}/edit", response_class=HTMLResponse)
def edit_dossier_page(request: Request, eleve_id: int):
    dossier = get_dossier_by_eleve(eleve_id)
    return templates.TemplateResponse("dossier/edit.html", {
        "request": request,
        "dossier": dossier
    })

@router.post("/{eleve_id}/edit")
def update_dossier_form(
    eleve_id: int,
    avertissement_travail: int = Form(...),
    avertissement_comportement: int = Form(...)
):
    update_dossier(eleve_id, avertissement_travail, avertissement_comportement)
    return RedirectResponse("/dossier/", status_code=303)