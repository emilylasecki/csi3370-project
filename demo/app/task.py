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