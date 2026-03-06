class Task:

    def __init__(self, taskID, taskName, description, creationDate, dueDate, status, effortEstimation, priority, task_group, groupID):
        self.taskID = taskID
        self.taskName = taskName
        self.description = description
        self.creationDate = creationDate
        self.dueDate = dueDate
        self.status = status
        self.effortEstimation = effortEstimation
        self.priority = priority
        self.task_group = task_group # object of type task_group
        self.groupID = groupID # for use in database keys

    # getters

    def get_taskID(self):
        return self.taskID

    def get_taskName(self):
        return self.taskName

    def get_description(self):
        return self.description

    def get_creationDate(self):
        return self.creationDate

    def get_dueDate(self):
        return self.dueDate

    def get_status(self):
        return self.status

    def get_effortEstimation(self):
        return self.effortEstimation

    def get_priority(self):
        return self.priority


    # setters

    def set_taskID(self, taskID):
        self.taskID = taskID

    def set_taskName(self, taskName):
        self.taskName = taskName

    def set_description(self, description):
        self.description = description

    def set_creationDate(self, creationDate):
        self.creationDate = creationDate

    def set_dueDate(self, dueDate):
        self.dueDate = dueDate

    def set_status(self, status):
        self.status = status

    def set_effortEstimation(self, effortEstimation):
        self.effortEstimation = effortEstimation

    def set_priority(self, priority):
        self.priority = priority

    # use case functions

    def request_task_info(self, taskID):
        return 0
    
    def add_task_to_group(self, taskID, task_group):
        return 0
    
    def display_all_tasks(self, userID, taskID):
        return 0
    
    def remove_task_from_group(self): # also need to tell task group to not use
        self.task_group = None
    
    def add_task_to_group(self, task_group): # also need to tell task group to use
        self.task_group = task_group
    
    
    # helper or additional functions