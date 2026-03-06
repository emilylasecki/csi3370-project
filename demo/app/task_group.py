

class Task_Group:

    def __init__(self, groupID, color, habitType):
        self.groupID = groupID
        self.color = color
        self.habitType = habitType

    # getters

    def get_groupID(self):
        return self.groupID
    
    def get_color(self):
        return self.color
    
    def get_habitType(self):
        return self.habitType
    
    # setters

    def set_groupID(self, groupID): # will be called by group when make group
        self.groupID = groupID

    def set_color(self, color):
        self.color = color

    def set_habitType(self, habitType):
        self.habitType = habitType

    # use case functions

    def validate_group(self):
        return 0
    
    def validate_update(self):
        return 0
    
    def request_add_task_to_group(self):
        return 0
    
    def display_task_groups(self, userID): # for task in user id get all tasks (sql step i believe?)
        return 0
    
    def request_remove_task_from_group(self):
        return 0
    