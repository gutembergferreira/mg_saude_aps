from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="backend/app/templates")

router = APIRouter()


@router.get("/")
def root():
    return RedirectResponse(url="/login", status_code=302)


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/painel/gestantes")
def painel_gestantes_page(request: Request):
    return templates.TemplateResponse("painel_gestantes.html", {"request": request})


@router.get("/painel/criancas")
def painel_criancas_page(request: Request):
    return templates.TemplateResponse("painel_criancas.html", {"request": request})
