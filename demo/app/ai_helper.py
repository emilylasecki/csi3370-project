from datetime import datetime


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


def is_high_priority(priority):
    try:
        return int(priority) >= 3
    except:
        return False


def count_high_priority_incomplete(tasks):
    count = 0

    for task in tasks:
        priority = task.get("priority", 0)
        status = normalize_status(task.get("status", ""))

        if is_high_priority(priority) and status != "completed":
            count += 1

    return count


def analyze_tasks(tasks):
    today = datetime.today().date()

    total_tasks = len(tasks)
    completed = 0
    incomplete = 0
    overdue = 0

    priority_counts = {"High": 0, "Medium": 0, "Low": 0}

    high_priority_incomplete = count_high_priority_incomplete(tasks)

    for task in tasks:
        status = normalize_status(task.get("status", ""))
        due_date_str = task.get("dueDate", "")
        priority = task.get("priority", 0)

        if status == "completed":
            completed += 1
        else:
            incomplete += 1

        try:
            priority_num = int(priority)
            if priority_num >= 3:
                priority_counts["High"] += 1
            elif priority_num == 2:
                priority_counts["Medium"] += 1
            else:
                priority_counts["Low"] += 1
        except:
            priority_counts["Low"] += 1

        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                if status != "completed" and due_date < today:
                    overdue += 1
            except ValueError:
                pass

    if total_tasks > 0:
        completion_rate = round((completed / total_tasks) * 100, 2)
    else:
        completion_rate = 0

    top_priority_type = max(priority_counts, key=priority_counts.get) if total_tasks > 0 else None

    suggestions = []

    if overdue >= 2:
        suggestions.append("You have several overdue tasks. Try finishing the smallest overdue task first.")

    if completion_rate < 50:
        suggestions.append("Your completion rate is low. Try setting fewer tasks each day.")

    if high_priority_incomplete >= 2:
        suggestions.append("You have many unfinished high priority tasks. Try completing one before adding new tasks.")

    if overdue >= 3:
        suggestions.append("Several tasks are overdue. Break them into smaller steps so they feel easier to finish.")

    if top_priority_type == "High":
        suggestions.append("A lot of your tasks are high priority. Make sure everything is truly urgent before marking it high.")

    if not suggestions:
        suggestions.append("You are doing well. Keep tracking your progress.")

    return {
        "total_tasks": total_tasks,
        "completed": completed,
        "incomplete": incomplete,
        "overdue": overdue,
        "completion_rate": completion_rate,
        "high_priority_incomplete": high_priority_incomplete,
        "top_priority_type": top_priority_type,
        "suggestions": suggestions
    }