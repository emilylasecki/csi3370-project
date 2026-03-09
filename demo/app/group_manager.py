from datetime import datetime

class GroupManager:

    def __init__(self, supabase_client):
        self.supabase = supabase_client

    def create_group(self, title, color, habit, user_id):

        # Convert checkbox to boolean
        habit_value = True if habit else False

        data = {
            "groupName": title,
            "color": color,
            "is_habit": habit_value,
            "user_id": user_id
        }

        response = self.supabase.table("task_groups").insert(data).execute()

        return response