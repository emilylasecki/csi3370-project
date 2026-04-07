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
from starlette.middleware.sessions import SessionMiddleware
import bcrypt

from app.progress_report import generate_wrap
from app.progress_report import normalize_task_for_ai

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

task_manager = TaskManager(supabase)
group_manager = GroupManager(supabase)

def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return user_id


@app.route('/', methods=['GET', 'HEAD'])
def home(request: Request):

    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse("/welcome", status_code=303)

    try:
        min_tasks_required = 5
        monthly_tasks = task_manager.get_current_month_tasks_for_user(user_id)
        monthly_tasks = [normalize_task_for_ai(task) for task in monthly_tasks]
        wrap_ready = len(monthly_tasks) >= min_tasks_required

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "wrap_ready": wrap_ready,
                "tasks" : monthly_tasks
            }
        )

    except Exception as e:
        return HTMLResponse(
            f"<h1>Home route error</h1><pre>{str(e)}</pre>",
            status_code=500
        )

@app.get("/groupedit")
def group_edit(request: Request):

    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse("/welcome", status_code=303)

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
        #.eq("password", password)  
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
    
    #User logs in succesfully
    user = result.data[0]

    if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
        return templates.TemplateResponse(
            "WelcomePage.html",
            {
                "request": request,
                "error": "Invalid username or password. Register if you don't have an account."
            }
        )

    request.session["user_id"] = user["user_id"]
    request.session["username"] = user["username"]

    return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("RegisterPage.html", {"request": request})


@app.post("/register")
def register_user(
    request: Request,
    Username: str = Form(...),
    Email: str = Form(...),
    Question: str = Form(...),
    entry_password: str = Form(...),
    
):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(entry_password.encode('utf-8'), salt).decode('utf-8')
    hashed_security_answer = bcrypt.hashpw(Question.encode('utf-8'), salt).decode('utf-8')
    if Username.strip() == "" or Email.strip() == "" or Question.strip() == "" or entry_password.strip() == "":
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
    
    existing_email = (
    supabase
    .table("users")
    .select("*")
    .eq("email", Email)
    .execute()
)

    if len(existing_email.data) > 0:
        return templates.TemplateResponse(
            "RegisterPage.html",
            {
                "request": request,
                "error": "Email already registered. Please use a different email."
            }
        )

    supabase.table("users").insert(
        {
            "username": Username,
            "email": Email,
            "security_question": hashed_security_answer,
            "password": hashed_password
        }
    ).execute()

    return RedirectResponse(url="/welcome?registered=1", status_code=HTTP_303_SEE_OTHER)

@app.get("/reset-password")
def reset_password_page(request: Request):
    return templates.TemplateResponse("NewPasswordPage.html", {"request": request})

@app.post("/reset-password")
def reset_password(
    request: Request,
    Username: str = Form(...),
    Email: str = Form(...),
    Question: str = Form(...),
    new_password: str = Form(...)
):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt).decode('utf-8')

    user_result = (
        supabase
        .table("users")
        .select("*")
        .eq("username", Username)
        .eq("email", Email)
        #.eq("security_question", Question)
        .execute()
    )

    if len(user_result.data) == 0:
        return templates.TemplateResponse(
            "NewPasswordPage.html",
            {
                "request": request,
                "error": "No matching user found with provided information."
            }
        )

    user_id = user_result.data[0]["user_id"]

    if not bcrypt.checkpw(Question.encode('utf-8'), user_result.data[0]["security_question"].encode('utf-8')):
        return templates.TemplateResponse(
            "NewPasswordPage.html",
            {
                "request": request,
                "error": "Security question answer is incorrect."
            }
        )

    supabase.table("users").update(
        {"password": hashed_password}
    ).eq("user_id", user_id).execute()

    return RedirectResponse(url="/welcome?password_reset=1", status_code=HTTP_303_SEE_OTHER)

@app.get("/taskcreation")
def task_creation(request: Request):

    user_id = get_current_user(request)

    if not user_id:
        return RedirectResponse("/welcome", status_code=303)

    groups = (
        supabase
        .table("task_groups")
        .select("*")
        .eq("user_id", user_id)
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
    user_id = get_current_user(request)

    if not user_id:
        return RedirectResponse("/welcome", status_code=303)
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

@app.get("/tasks")
def get_tasks(request: Request):
    user_id = get_current_user(request)  # Pass request to get session user

    if not user_id:
        return {"error": "Not logged in"}

    try:
        # Fetch tasks and include habit and color from task_groups
        tasks_result = (
            supabase
            .table("tasks")
            .select("*, task_groups(is_habit,color)")
            .eq("userID", user_id)
            .execute()
        )

        tasks = tasks_result.data or []

        # Add top-level habit and color fields for JS convenience
        for task in tasks:
            task['habit'] = False
            task['group_color'] = "#ffffff"  # default white

            if task.get("groupID") and task.get("task_groups"):
                group = task["task_groups"]
                task['habit'] = group.get("is_habit", False)
                task['group_color'] = group.get("color", "#ffffff")

        return tasks

    except Exception as e:
        return {"error": str(e)}



@app.get("/wrapped")
def wrapped_page(request: Request):
    user_id = get_current_user(request)

    if not user_id:
        return RedirectResponse("/welcome", status_code=303)

    try:
        min_tasks_required = 5
        monthly_tasks = task_manager.get_current_month_tasks_for_user(user_id)
        monthly_tasks = [normalize_task_for_ai(task) for task in monthly_tasks]
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
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse("/welcome", status_code=303)
    
    groups = group_manager.get_groups_for_user(user_id)

    # Provide a default empty object so template doesn't break
    selected_group = {
        "color": ""  # default to empty string
    }

    return templates.TemplateResponse(
        "GroupCreation.html",
        {
            "request": request,
            "groups": groups,
            "selected_group": selected_group
        }
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


@app.post("/update_group")
def update_group_route(
    request: Request,
    groupID: int = Form(...),
    title: str = Form(...),
    color: str = Form(...),
    habit: str = Form(None)
):
    user_id = get_current_user(request)

    if not user_id:
        return RedirectResponse("/welcome", status_code=303)
    """
    Update a group using GroupManager.
    """
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse("/welcome", status_code=303)

    habit_bool = True if habit in ("on", "true", True) else False

    group_manager.update_group(
        groupID=groupID,
        title=title,
        color=color,
        habit=habit_bool,
        user_id=user_id
    )

    print("SESSION USER:", user_id)
    print("GROUP ID:", groupID)

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

@app.get("/modify_task")
def modify_task_page(request: Request, taskID: int):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse("/welcome", status_code=303)
    task = task_manager.get_task(taskID)
    if not task:
        return HTMLResponse("Task not found", status_code=404)
    # Fetch groups for dropdown
    groups = group_manager.get_groups_for_user(user_id)
    return templates.TemplateResponse(
        "ModifyTask.html",
        {
            "request": request,
            "task": task,
            "groups": groups
        }
    )

@app.post("/modify_task")
def modify_task_submit(
    request: Request,
    taskID: int = Form(...),
    taskName: str = Form(...),
    description: str = Form(...),
    dueDate: str = Form(...),
    status: str = Form(...),
    priority: int = Form(...),
    effortEstimation: int = Form(...),
    groupID: int = Form(None)
):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse("/welcome", status_code=303)

    updates = {
        "taskName": taskName,
        "description": description,
        "dueDate": dueDate,
        "status": status,
        "priority": priority,
        "effortEstimation": effortEstimation,
        "groupID": groupID
    }

    task_manager.update_task(taskID, updates, user_id)

    return RedirectResponse(url="/?success=3", status_code=303)


@app.post("/delete_task")
def delete_task_route(request: Request, taskID: int = Form(...)):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse("/welcome", status_code=303)

    task_manager.delete_task(taskID, user_id)
    return RedirectResponse(url="/?success=4", status_code=303)