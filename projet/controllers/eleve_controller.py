from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from services.eleves_service import *

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# -------- PAGE LISTE --------
@router.get("/", response_class=HTMLResponse)
def eleves_page(request: Request):
    eleves = get_all_eleves()
    return templates.TemplateResponse("eleve/index.html", {
        "request": request,
        "eleves": eleves
    })

# -------- AJOUT --------
@router.get("/new", response_class=HTMLResponse)
def new_eleve_page(request: Request):
    return templates.TemplateResponse("eleve/new.html", {"request": request})

@router.post("/new")
def create_eleve_form(
    nom: str = Form(...),
    age: int = Form(...),
    email: str = Form(...),
    promotion_id: int = Form(...)
):
    create_eleve(nom, email, age, promotion_id)
    return RedirectResponse("/eleve/", status_code=303)

# -------- EDIT --------
@router.get("/{eleve_id}/edit", response_class=HTMLResponse)
def edit_eleve_page(request: Request, eleve_id: int):
    eleve = get_eleve_by_id(eleve_id)
    return templates.TemplateResponse("eleve/edit.html", {
        "request": request,
        "eleve": eleve
    })

@router.post("/{eleve_id}/edit")
def update_eleve_form(
    eleve_id: int,
    nom: str = Form(...),
    age: int = Form(...),
    email: str = Form(...),
    promotion_id: int = Form(...)
):
    update_eleve(eleve_id, nom, email, age, promotion_id)
    return RedirectResponse("/eleve/", status_code=303)

# -------- DELETE --------
@router.get("/{eleve_id}/delete")
def delete_eleve_route(eleve_id: int):
    delete_eleve(eleve_id)
    return RedirectResponse("/eleve/", status_code=303)