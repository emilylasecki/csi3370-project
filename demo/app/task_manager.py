# demo/app/task_manager.py
from datetime import date
from app.task import Task
from supabase import Client

class TaskManager:
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client

    # ---------------- Add Task ----------------
    def add_task(self, taskName, description, dueDate,
                 status, effort, priority, groupID, userID):
        """
        Add a new task to Supabase.
        - groupID = 0 means no group assigned
        """

        # Optional: validate groupID exists, skip if 0
        if groupID != 0:
            group_check = self.supabase.table("task_groups").select("groupID").eq("groupID", groupID).execute()
            if not group_check.data:
                raise ValueError(f"TaskGroup with ID {groupID} does not exist.")

        # Create Task instance
        new_task = Task(
            taskID=None,
            taskName=taskName,
            description=description,
            creationDate=date.today().isoformat(),
            dueDate=dueDate,
            status=status,
            effortEstimation=effort,
            priority=priority,
            task_group=groupID,
            groupID=groupID
        )

        # Prepare data for Supabase insert
        insert_data = {
            "taskName": new_task.taskName,
            "description": new_task.description,
            "created_at": new_task.creationDate,
            "dueDate": new_task.dueDate,
            "status": new_task.status,
            "effortEstimation": new_task.effortEstimation,
            "priority": new_task.priority,
            "userID": userID  # Link the task to the logged-in user
        }

        # Include groupID only if it's not 0
        if groupID != 0:
            insert_data["groupID"] = new_task.groupID

        # Insert into Supabase
        response = self.supabase.table("tasks").insert(insert_data).execute()

        # Update taskID from Supabase response
        new_task.taskID = response.data[0]["task_id"]
        return new_task

    # ---------------- Get Task ----------------
    def get_task(self, taskID):
        """Fetch a single task by ID"""
        response = self.supabase.table("tasks") \
            .select("*") \
            .eq("task_id", taskID) \
            .execute()

        if response.data:
            task = response.data[0]
            if task.get("groupID"):
                group_resp = self.supabase.table("task_groups") \
                    .select("*") \
                    .eq("groupID", task["groupID"]) \
                    .execute()
                task["group"] = group_resp.data[0] if group_resp.data else None
            return task
        return None

    # ---------------- Update Task ----------------
    def update_task(self, taskID, updates, userID):
        """
        updates: dict of fields to update, e.g.
        {
            "taskName": "New Name",
            "description": "New desc",
            "dueDate": "2026-03-21",
            "status": "Incomplete",
            "priority": 2,
            "effortEstimation": 3,
            "groupID": 5
        }
        """
        task = self.get_task(taskID)
        if not task:
            raise Exception("Task not found")

        if int(task["userID"]) != int(userID):
            raise Exception("Unauthorized")

        response = self.supabase.table("tasks") \
            .update(updates) \
            .eq("task_id", taskID) \
            .execute()

        return response

    # ---------------- Delete Task ----------------
    def delete_task(self, taskID, userID):
        """Delete a task"""
        task = self.get_task(taskID)
        if not task:
            raise Exception("Task not found")
        if int(task["userID"]) != int(userID):
            raise Exception("Unauthorized")

        response = self.supabase.table("tasks") \
            .delete() \
            .eq("task_id", taskID) \
            .execute()
        return response