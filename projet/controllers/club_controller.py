from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from services.club_services import *

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# -------- LISTE DES CLUBS --------
@router.get("/", response_class=HTMLResponse)
def clubs_page(request: Request):
    clubs = get_all_clubs()
    return templates.TemplateResponse("club/index.html", {
        "request": request,
        "clubs": clubs
    })


# -------- AJOUT --------
@router.get("/new", response_class=HTMLResponse)
def new_club_page(request: Request):
    sports = get_all_sports()
    return templates.TemplateResponse("club/new.html", {
        "request": request,
        "sports": sports
    })


@router.post("/new")
def create_club_form(
    nom: str = Form(...),
    sport_id: int = Form(...)
):
    create_club(nom, sport_id)
    return RedirectResponse("/club/", status_code=303)


# -------- EDIT --------
@router.get("/{club_id}/edit", response_class=HTMLResponse)
def edit_club_page(request: Request, club_id: int):
    club = get_club_by_id(club_id)
    sports = get_all_sports()

    return templates.TemplateResponse("club/edit.html", {
        "request": request,
        "club": club,
        "sports": sports
    })


@router.post("/{club_id}/edit")
def update_club_form(
    club_id: int,
    nom: str = Form(...),
    sport_id: int = Form(...)
):
    update_club(club_id, nom, sport_id)
    return RedirectResponse("/club/", status_code=303)


# -------- DELETE --------
@router.post("/{club_id}/delete")
def delete_club_form(club_id: int):
    # Optionnel : vérifier si le club existe avant de supprimer
    club = get_club_by_id(club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club non trouvé")
    
    delete_club(club_id)
    return RedirectResponse("/club/", status_code=303)