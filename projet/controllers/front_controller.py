import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(current_dir, "..", "templates")

@router.get("/", response_class=HTMLResponse)
def home():
    index_path = os.path.join(templates_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()