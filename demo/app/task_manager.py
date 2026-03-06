# demo/app/task_manager.py
from datetime import date
from app.task import Task
from supabase import Client

class TaskManager:
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client

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
            groupID = groupID
        )

        # Prepare data for Supabase insert
        insert_data = {
            "taskName": new_task.taskName,
            "description": new_task.description,
            "creationDate": new_task.creationDate,
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