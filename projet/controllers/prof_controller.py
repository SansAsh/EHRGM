from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from services.profs_service import *

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# ---------------- LISTE ----------------
@router.get("/", response_class=HTMLResponse)
def prof_index(request: Request):
    profs_severe = get_prof_severe()
    all_profs = get_all_profs()
    return templates.TemplateResponse("prof/index.html", {
        "request": request,
        "profs_severe": profs_severe,
        "all_profs": all_profs
    })

# ---------------- NEW ----------------
@router.get("/new", response_class=HTMLResponse)
def prof_new_page(request: Request):
    return templates.TemplateResponse("prof/new.html", {"request": request})

@router.post("/new")
def prof_create(nom: str = Form(...), email: str = Form(...)):
    create_prof(nom, email)
    return RedirectResponse("/prof/", status_code=303)

# ---------------- EDIT ----------------
@router.get("/{prof_id}/edit", response_class=HTMLResponse)
def prof_edit_page(request: Request, prof_id: int):
    prof = get_prof_by_id(prof_id)
    return templates.TemplateResponse("prof/edit.html", {
        "request": request,
        "prof": prof
    })

@router.post("/{prof_id}/edit")
def prof_update(prof_id: int, nom: str = Form(...), email: str = Form(...)):
    update_prof(prof_id, nom, email)
    return RedirectResponse("/prof/", status_code=303)

# ---------------- DELETE ----------------
@router.get("/{prof_id}/delete")
def prof_delete(prof_id: int):
    delete_prof(prof_id)
    return RedirectResponse("/prof/", status_code=303)