from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from services.notes_service import *

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# -------- INDEX : élèves moyenne > 12 --------
@router.get("/", response_class=HTMLResponse)
def notes_index(request: Request):
    eleves_moyenne = get_eleves_moyenne_sup12()
    eleves_all = get_all_notes()
    return templates.TemplateResponse("note/index.html", {
        "request": request,
        "eleves_moyenne": eleves_moyenne,
        "eleves_all": eleves_all
    })

# -------- NEW --------
@router.get("/new", response_class=HTMLResponse)
def note_new_page(request: Request):
    return templates.TemplateResponse("note/new.html", {"request": request})

@router.post("/new")
def note_create(eleve_id: int = Form(...), prof_id: int = Form(...), note_valeur: float = Form(...)):
    create_note(eleve_id, prof_id, note_valeur)
    return RedirectResponse("/note/", status_code=303)

# -------- EDIT --------
@router.get("/{note_id}/edit", response_class=HTMLResponse)
def note_edit_page(request: Request, note_id: int):
    # récupérer la note à modifier
    notes = get_all_notes()
    note = next((n for n in notes if n["id"] == note_id), None)
    return templates.TemplateResponse("note/edit.html", {
        "request": request,
        "note": note
    })

@router.post("/{note_id}/edit")
def note_update(note_id: int, eleve_id: int = Form(...), prof_id: int = Form(...), note_valeur: float = Form(...)):
    update_note(note_id, eleve_id, prof_id, note_valeur)
    return RedirectResponse("/note/", status_code=303)