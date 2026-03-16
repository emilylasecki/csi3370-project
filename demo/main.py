# main.py
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.task_manager import TaskManager
from app.group_manager import GroupManager
from supabase import create_client
from starlette.status import HTTP_303_SEE_OTHER
from enviornment import SUPABASE_KEY, SUPABASE_URL
from starlette.middleware.sessions import SessionMiddleware

import json
from app.ai_helper import analyze_tasks
from app.progress_report import generate_wrap

# Initialize FastAPI
app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# TaskManager instance
task_manager = TaskManager(supabase)
group_manager = GroupManager(supabase)

def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return user_id


# Home page
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/groupedit")
def group_edit(request: Request):
    return templates.TemplateResponse("GroupEdit.html", {"request": request})

@app.get("/welcome")
def welcome_page(request: Request):
    return templates.TemplateResponse("WelcomePage.html", {"request": request})
#sign in page
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
    
    #find user in database
    result = supabase.table("users").select("*").eq("username", Username).eq("password", password).execute()

    #for not registered users
    if len(result.data) == 0:
        return templates.TemplateResponse(
            "WelcomePage.html",
            {
                "request": request,
                "error": "Invalid username or password. Register if you don't have an account."
            }
        )
    
    #User logs iin succesfully
    user = result.data[0]

    request.session["user_id"] = user["user_id"]
    request.session["username"] = user["username"]

    return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

# Registration page
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
    
    # Check if username already exists
    existing_user = supabase.table("users").select("*").eq("username", Username).execute()
    if len(existing_user.data) > 0:
        return templates.TemplateResponse(
            "RegisterPage.html",
            {
                "request": request,
                "error": "Username already taken. Please choose a different one."
            }
        )
    
    # Insert new user into database
    supabase.table("users").insert({"username": Username, "email": Email, "password": password}).execute()

    return RedirectResponse(url="/welcome?registered=1", status_code=HTTP_303_SEE_OTHER)

# Task creation page
@app.get("/taskcreation")
def task_creation(request: Request):

    user_id = get_current_user(request)

    if not user_id:
        return RedirectResponse("/welcome", status_code=303)

    groups = (
        supabase
        .table("task_groups")
        .select("*")
        .eq("user_id", user_id)   # TODO make this not hard coded
        .execute()
    ).data

    return templates.TemplateResponse(
        "TaskCreation.html",
        {
            "request": request,
            "groups": groups
        }
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
    userID = get_current_user(request)

    if not userID:
        return RedirectResponse("/welcome", status_code =303)

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
    return templates.TemplateResponse("Wrapped.html", {"request": request})

@app.get("/groupcreation")
def group_creation(request: Request):
    return templates.TemplateResponse(
        "GroupCreation.html",
        {"request": request}
    )

@app.post("/create_group")
def create_group(
    request: Request,
    title: str = Form(...),
    color: str = Form(...),
    habit: str = Form(None)
):

    user_id = get_current_user(request)

    if not user_id:
        return RedirectResponse("/welcome", status_code=303)
    

    group_manager.create_group(
        title,
        color,
        habit,
        user_id
    )

    return RedirectResponse(url="/?success=2", status_code=HTTP_303_SEE_OTHER)

# GET route to show ModifyGroup page
@app.get("/modifygroup")
def modify_group(request: Request, groupID: int = 0):
    user_id = get_current_user(request)

    if not user_id:
        return RedirectResponse("/welcome", status_code=303)

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

# POST route to handle updates
@app.post("/update_group")
def update_group_route(
    request: Request,
    groupID: int = Form(...),
    title: str = Form(...),
    color: str = Form(...),
    habit: str = Form(None)
):
    """
    Update a group using GroupManager.
    """
    user_id = get_current_user(request)

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
def delete_group(request: Request, groupID: int = Form(...)):

    user_id = get_current_user(request)

    if not user_id:
        return RedirectResponse("/welcome", status_code=303)

    group_manager.delete_group(groupID, user_id)

    return RedirectResponse(
        url="/modifygroup",
        status_code=HTTP_303_SEE_OTHER
    )

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/welcome", status_code=303)