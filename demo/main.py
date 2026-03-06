# from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles

# from fastapi import FastAPI
# from app.controllers import router  # import your route definitions

# app = FastAPI()

# # Mount static files
# from fastapi.staticfiles import StaticFiles
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # Include routes from controllers.py
# app.include_router(router)

# templates = Jinja2Templates(directory="templates")

# @router.get("/taskcreation")
# def about(request: Request):
#     return templates.TemplateResponse("TaskCreation.html", {"request": request})

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates (you MUST do this in every file that uses templates)
templates = Jinja2Templates(directory="templates")

# Home page route
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# task creation
@app.get("/taskcreation")
def about(request: Request):
    return templates.TemplateResponse("TaskCreation.html", {"request": request})

# group edit
@app.get("/groupedit")
def about(request: Request):
    return templates.TemplateResponse("GroupEdit.html", {"request": request})

# welcome page
@app.get("/welcome")
def about(request: Request):
    return templates.TemplateResponse("WelcomePage.html", {"request": request})