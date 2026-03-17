# main.py
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.task_manager import TaskManager
from app.group_manager import GroupManager
from supabase import create_client
from starlette.status import HTTP_303_SEE_OTHER
from enviornment import SUPABASE_KEY, SUPABASE_URL
from datetime import datetime, date
import json

from app.ai_helper import analyze_tasks
from app.progress_report import generate_wrap

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

task_manager = TaskManager(supabase)
group_manager = GroupManager(supabase)


@app.get("/")
def home(request: Request):
    try:
        user_id = 1
        min_tasks_required = 5

        today = date.today()
        current_month = today.month
        current_year = today.year

        month_start = datetime(current_year, current_month, 1)

        if current_month == 12:
            next_month_start = datetime(current_year + 1, 1, 1)
        else:
            next_month_start = datetime(current_year, current_month + 1, 1)

        tasks_result = (
            supabase
            .table("tasks")
            .select("*")
            .eq("userID", user_id)
            .gte("created_at", month_start.isoformat())
            .lt("created_at", next_month_start.isoformat())
            .execute()
        )

        monthly_tasks = tasks_result.data if tasks_result.data else []
        wrap_ready = len(monthly_tasks) >= min_tasks_required

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "wrap_ready": wrap_ready
            }
        )

    except Exception as e:
        return HTMLResponse(
            f"<h1>Home route error</h1><pre>{str(e)}</pre>",
            status_code=500
        )


@app.get("/groupedit")
def group_edit(request: Request):
    return templates.TemplateResponse("GroupEdit.html", {"request": request})


@app.get("/welcome")
def welcome_page(request: Request):
    return templates.TemplateResponse("WelcomePage.html", {"request": request})


@app.post("/welcome")
def welcome_signin(
    request: Request,
    Username: str = Form(...),
    password: str = Form(...)
):
    if Username.strip() == "" or password.strip() == "":
        return templates.TemplateResponse(
            "WelcomePage.html",
            {
                "request": request,
                "error": "Username and password cannot be empty."
            }
        )

    result = (
        supabase
        .table("users")
        .select("*")
        .eq("username", Username)
        .eq("password", password)
        .execute()
    )

    if len(result.data) == 0:
        return templates.TemplateResponse(
            "WelcomePage.html",
            {
                "request": request,
                "error": "Invalid username or password. Register if you don't have an account."
            }
        )

    return RedirectResponse(url="/taskcreation", status_code=HTTP_303_SEE_OTHER)


@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("RegisterPage.html", {"request": request})


@app.post("/register")
def register_user(
    request: Request,
    Username: str = Form(...),
    Email: str = Form(...),
    password: str = Form(...)
):
    if Username.strip() == "" or Email.strip() == "" or password.strip() == "":
        return templates.TemplateResponse(
            "RegisterPage.html",
            {
                "request": request,
                "error": "All fields cannot be empty."
            }
        )

    existing_user = (
        supabase
        .table("users")
        .select("*")
        .eq("username", Username)
        .execute()
    )

    if len(existing_user.data) > 0:
        return templates.TemplateResponse(
            "RegisterPage.html",
            {
                "request": request,
                "error": "Username already taken. Please choose a different one."
            }
        )

    supabase.table("users").insert(
        {
            "username": Username,
            "email": Email,
            "password": password
        }
    ).execute()

    return RedirectResponse(url="/welcome?registered=1", status_code=HTTP_303_SEE_OTHER)


@app.get("/taskcreation")
def task_creation(request: Request):
    groups = (
        supabase
        .table("task_groups")
        .select("*")
        .eq("user_id", 1)
        .execute()
    ).data

    return templates.TemplateResponse(
        "TaskCreation.html",
        {
            "request": request,
            "groups": groups
        }
    )


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


@app.get("/wrap")
def wrap():
    tasks = load_tasks()
    result = generate_wrap(tasks)
    return result


@app.get("/wrapped")
def wrapped_page(request: Request):
    try:
        user_id = 1
        min_tasks_required = 5

        today = date.today()
        current_month = today.month
        current_year = today.year

        month_start = datetime(current_year, current_month, 1)

        if current_month == 12:
            next_month_start = datetime(current_year + 1, 1, 1)
        else:
            next_month_start = datetime(current_year, current_month + 1, 1)

        tasks_result = (
            supabase
            .table("tasks")
            .select("*")
            .eq("userID", user_id)
            .gte("created_at", month_start.isoformat())
            .lt("created_at", next_month_start.isoformat())
            .execute()
        )

        monthly_tasks = tasks_result.data if tasks_result.data else []
        task_count = len(monthly_tasks)

        if task_count < min_tasks_required:
            tasks_needed = min_tasks_required - task_count

            return templates.TemplateResponse(
                "Wrapped.html",
                {
                    "request": request,
                    "wrap_locked": True,
                    "wrap_data": {},
                    "tasks_needed": tasks_needed
                }
            )

        wrap_data = generate_wrap(monthly_tasks) or {}

        return templates.TemplateResponse(
            "Wrapped.html",
            {
                "request": request,
                "wrap_locked": False,
                "wrap_data": wrap_data,
                "tasks_needed": 0
            }
        )

    except Exception as e:
        return HTMLResponse(
            f"<h1>Wrapped route error</h1><pre>{str(e)}</pre>",
            status_code=500
        )


@app.get("/groupcreation")
def group_creation(request: Request):
    return templates.TemplateResponse(
        "GroupCreation.html",
        {"request": request}
    )


@app.post("/create_group")
def create_group(
    title: str = Form(...),
    color: str = Form(...),
    habit: str = Form(None)
):
    user_id = 1

    group_manager.create_group(
        title,
        color,
        habit,
        user_id
    )

    return RedirectResponse(url="/?success=2", status_code=HTTP_303_SEE_OTHER)


@app.get("/modifygroup")
def modify_group(request: Request, groupID: int = 0):
    user_id = 1
    groups = group_manager.get_groups_for_user(user_id)

    selected_group = None
    if groupID != 0:
        selected_group = group_manager.get_group(groupID)

    return templates.TemplateResponse(
        "ModifyGroup.html",
        {
            "request": request,
            "groups": groups,
            "selected_group": selected_group
        }
    )


@app.post("/update_group")
def update_group_route(
    groupID: int = Form(...),
    title: str = Form(...),
    color: str = Form(...),
    habit: str = Form(None)
):
    user_id = 1

    habit_bool = True if habit in ("on", "true", True) else False

    group_manager.update_group(
        groupID=groupID,
        title=title,
        color=color,
        habit=habit_bool,
        user_id=user_id
    )

    return RedirectResponse(
        url=f"/modifygroup?groupID={groupID}",
        status_code=303
    )


@app.post("/delete_group")
def delete_group(groupID: int = Form(...)):
    user_id = 1

    group_manager.delete_group(
        groupID,
        user_id
    )

    return RedirectResponse(
        url="/modifygroup",
        status_code=HTTP_303_SEE_OTHER
    )