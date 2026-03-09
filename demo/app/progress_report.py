from collections import Counter
from datetime import datetime


def get_day_name(date_string):
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")
        return date_obj.strftime("%A")
    except:
        return None


def generate_wrap(tasks):
    total_tasks = len(tasks)
    completed_tasks = 0
    overdue_tasks = 0
    category_counter = Counter()
    completed_day_counter = Counter()

    today = datetime.today().date()

    for task in tasks:
        category = task.get("category", "Other")
        status = task.get("status", "").lower()
        due_date_str = task.get("due_date", "")
        completed_date_str = task.get("completed_date", "")

        category_counter[category] += 1

        if status == "complete":
            completed_tasks += 1

            day_name = get_day_name(completed_date_str)
            if day_name:
                completed_day_counter[day_name] += 1

        else:
            if due_date_str:
                try:
                    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                    if due_date < today:
                        overdue_tasks += 1
                except:
                    pass

    if total_tasks > 0:
        completion_rate = round((completed_tasks / total_tasks) * 100, 2)
    else:
        completion_rate = 0

    top_category = None
    if category_counter:
        top_category = category_counter.most_common(1)[0][0]

    best_day = None
    if completed_day_counter:
        best_day = completed_day_counter.most_common(1)[0][0]

    summary_message = "You are building strong habits."
    if completion_rate >= 80:
        summary_message = "Amazing job. You stayed very consistent."
    elif completion_rate >= 50:
        summary_message = "Nice work. You made steady progress."
    else:
        summary_message = "You started the journey. Try smaller daily goals next time."

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate": completion_rate,
        "top_category": top_category,
        "best_day": best_day,
        "overdue_tasks": overdue_tasks,
        "summary_message": summary_message
    }


    