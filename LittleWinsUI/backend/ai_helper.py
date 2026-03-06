from datetime import datetime


def count_high_priority_incomplete(tasks):
    count = 0

    for task in tasks:
        priority = task.get("priority", "").lower()
        status = task.get("status", "").lower()

        # count unfinished high priority tasks
        if priority == "high" and status != "complete":
            count += 1

    return count


def analyze_tasks(tasks):
    today = datetime.today().date()

    total_tasks = len(tasks)
    completed = 0
    incomplete = 0
    overdue = 0
    category_counts = {}
    incomplete_categories = {}

    high_priority_incomplete = count_high_priority_incomplete(tasks)

    for task in tasks:
        status = task.get("status", "").lower()
        category = task.get("category", "Other")
        due_date_str = task.get("due_date", "")

        # count complete and incomplete
        if status == "complete":
            completed += 1
        else:
            incomplete += 1

        # count total tasks by category
        category_counts[category] = category_counts.get(category, 0) + 1

        # count incomplete tasks by category
        if status != "complete":
            incomplete_categories[category] = incomplete_categories.get(category, 0) + 1

        # check if task is overdue
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                if status != "complete" and due_date < today:
                    overdue += 1
            except ValueError:
                pass

    # completion rate
    if total_tasks > 0:
        completion_rate = round((completed / total_tasks) * 100, 2)
    else:
        completion_rate = 0

    # find category with most incomplete tasks
    struggle_category = None
    max_incomplete = 0

    for category, count in incomplete_categories.items():
        if count > max_incomplete:
            max_incomplete = count
            struggle_category = category

    # suggestions
    suggestions = []

    if overdue >= 2:
        suggestions.append("You have several overdue tasks. Try finishing the smallest overdue task first.")

    if completion_rate < 50:
        suggestions.append("Your completion rate is low. Try setting fewer tasks each day.")

    if high_priority_incomplete >= 2:
        suggestions.append("You have many unfinished high priority tasks. Try completing one before adding new tasks.")

    if overdue >= 3:
        suggestions.append("Several tasks are overdue. Consider breaking tasks into smaller steps to avoid procrastination.")

    if struggle_category:
        suggestions.append(f"You seem to struggle most with {struggle_category} tasks. Break them into smaller steps.")

    if not suggestions:
        suggestions.append("You are doing well. Keep tracking your progress.")

    return {
        "total_tasks": total_tasks,
        "completed": completed,
        "incomplete": incomplete,
        "overdue": overdue,
        "completion_rate": completion_rate,
        "high_priority_incomplete": high_priority_incomplete,
        "struggle_category": struggle_category,
        "suggestions": suggestions
    }