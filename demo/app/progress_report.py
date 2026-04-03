from collections import Counter
from datetime import datetime

def normalize_task_for_ai(task):
    due_date = task.get("dueDate")

    if due_date is None:
        due_date_str = ""
    else:
        due_date_str = str(due_date).split("T")[0]

    return {
        "taskName": task.get("taskName", ""),
        "description": task.get("description", ""),
        "status": task.get("status", ""),
        "priority": task.get("priority", 0),
        "dueDate": due_date_str,
        "effortEstimation": task.get("effortEstimation", 0)
    }


def normalize_status(status):
    if not status:
        return ""

    status = status.strip().lower()

    if status in ["completed", "complete", "done"]:
        return "completed"
    if status in ["in progress", "inprogress"]:
        return "in progress"
    if status in ["not started", "notstarted"]:
        return "not started"

    return status


def priority_label(priority_value):
    try:
        priority_value = int(priority_value)
    except:
        return "Unknown"

    if priority_value >= 3:
        return "High"
    elif priority_value == 2:
        return "Medium"
    else:
        return "Low"


def generate_wrap(tasks):
    total_tasks = len(tasks)
    completed_tasks = 0
    in_progress_tasks = 0
    not_started_tasks = 0
    overdue_tasks = 0

    priority_counter = Counter()
    due_day_counter = Counter()

    today = datetime.today().date()

    for task in tasks:
        status = normalize_status(task.get("status", ""))
        due_date_str = task.get("dueDate", "")
        priority = task.get("priority", 0)

        priority_counter[priority_label(priority)] += 1

        if status == "completed":
            completed_tasks += 1
        elif status == "in progress":
            in_progress_tasks += 1
        elif status == "not started":
            not_started_tasks += 1

        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()

                day_name = due_date.strftime("%A")
                due_day_counter[day_name] += 1

                if due_date < today and status != "completed":
                    overdue_tasks += 1
            except:
                pass

    if total_tasks > 0:
        completion_rate = round((completed_tasks / total_tasks) * 100, 2)
    else:
        completion_rate = 0

    top_priority = None
    if priority_counter:
        top_priority = priority_counter.most_common(1)[0][0]

    busiest_day = None
    if due_day_counter:
        busiest_day = due_day_counter.most_common(1)[0][0]

    summary_message = "You are building better task habits."
    if completion_rate >= 80:
        summary_message = "Amazing job. You stayed very consistent with your tasks."
    elif completion_rate >= 50:
        summary_message = "Nice work. You made solid progress and kept things moving."
    else:
        summary_message = "You made a start. Try focusing on finishing a few important tasks first."

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "in_progress_tasks": in_progress_tasks,
        "not_started_tasks": not_started_tasks,
        "completion_rate": completion_rate,
        "top_priority": top_priority,
        "busiest_day": busiest_day,
        "overdue_tasks": overdue_tasks,
        "summary_message": summary_message
    }

    