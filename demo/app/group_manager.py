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
    

    
    def get_group(self, groupID):

        response = self.supabase.table("task_groups") \
            .select("*") \
            .eq("groupID", groupID) \
            .execute()

        if response.data:
            return response.data[0]

        return None
    


    def get_groups_for_user(self, user_id):

        response = self.supabase.table("task_groups") \
            .select("*") \
            .eq("user_id", user_id) \
            .execute()

        return response.data
    

    
    def update_group(self, groupID, title, color, habit, user_id):
        group = self.get_group(groupID)
        if not group:
            raise Exception("Group not found")

        if group["user_id"] != user_id:
            raise Exception("Unauthorized")

        data = {
            "groupName": title,
            "color": color,
            "is_habit": habit
        }

        response = self.supabase.table("task_groups") \
            .update(data) \
            .eq("groupID", groupID) \
            .execute()

        return response
    



    def delete_group(self, groupID, user_id):

        group = self.get_group(groupID)

        if not group:
            raise Exception("Group not found")

        if group["user_id"] != user_id:
            raise Exception("Unauthorized")

        response = self.supabase.table("task_groups") \
            .delete() \
            .eq("groupID", groupID) \
            .execute()

        return response