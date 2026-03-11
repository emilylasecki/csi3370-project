from datetime import datetime
from app.task_group import TaskGroup

class GroupManager:

    def __init__(self, supabase_client):
        self.supabase = supabase_client

    def create_group(self, title, color, habit, user_id):

        new_group = TaskGroup(
            groupName = title,
            color = color,
            habitType = habit
        )

        # Convert checkbox to boolean
        new_group.habitType = True if habit else False

        data = {
            "groupName": new_group.groupName,
            "color": new_group.color,
            "is_habit": new_group.habitType,
            "user_id": user_id
        }

        response = self.supabase.table("task_groups").insert(data).execute()

        return response