# main.py
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.task_manager import TaskManager
from supabase import create_client
from starlette.status import HTTP_303_SEE_OTHER
from enviornment import SUPABASE_KEY, SUPABASE_URL
from flask import Flask, jsonify
from flask_cors import CORS
import json
from app.ai_helper import analyze_tasks

# Initialize FastAPI
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# TaskManager instance
task_manager = TaskManager(supabase)

# Home page
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/groupedit")
def group_edit(request: Request):
    return templates.TemplateResponse("GroupEdit.html", {"request": request})

@app.get("/welcome")
def welcome(request: Request):
    return templates.TemplateResponse("WelcomePage.html", {"request": request})

# Task creation page
@app.get("/taskcreation")
def task_creation(request: Request):
    groups_response = supabase.table("task_groups").select("*").execute()
    groups = groups_response.data
    return templates.TemplateResponse(
        "TaskCreation.html",
        {"request": request, "groups": groups}
    )

# Handle task submission
@app.post("/add_task")
def add_task_route(
    request: Request,
    taskName: str = Form(...),
    description: str = Form(...),
    dueDate: str = Form(...),
    status: str = Form(...),
    effort: int = Form(...),
    priority: int = Form(...),
    groupID: int = Form(...),
    is_habit: bool = Form(False)
):
    """
    Create a task using TaskManager and redirect back to task creation page
    """

    # Placeholder userID; replace with real session user
    userID = 1

    task_manager.add_task(
        taskName=taskName,
        description=description,
        dueDate=dueDate,
        status=status,
        effort=effort,
        priority=priority,
        groupID=groupID,
        userID=userID,
    )

    return RedirectResponse(url="/?success=1", status_code=HTTP_303_SEE_OTHER)

def load_tasks():
    with open("app/sample_tasks.json", "r") as file:
        return json.load(file)
    
@app.get("/tasks")
def get_tasks():
    tasks = load_tasks()
    return tasks


@app.get("/analyze")
def analyze():
    tasks = load_tasks()
    result = analyze_tasks(tasks)
    return result