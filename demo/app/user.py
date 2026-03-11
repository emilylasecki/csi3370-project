class User:

    def __init__(self, userID, userName, email, hashedPassword):
        self.userID = userID
        self.userName = userName
        self.email = email
        self.hashedPassword = hashedPassword

    # mutators and accessors (getters and setters)

    def get_userID(self):
        return self.userID
    
    def get_userName(self):
        return self.userName
    
    def get_email(self):
        return self.email
    
    def get_hashedPassword(self):
        return self.hashedPassword
    
    def set_userID(self, id): # will probably change, since we need to verify unique ids
        if type(id) is int:
            self.userID = id

    def set_userName(self, name):
        if type(name) is str:
            self.userName = name

    def set_email(self, email):
        self.email = email
    
    def set_hashedPassword(self, hashedPassword):
        self.hashedPassword = hashedPassword



    # use case functions

    def login(self): # login entirely contained to user class
        return 0
    
    def add_task(self): # i believe just a gui interaction? might not need this function
        return 0
    
    def provide_task_info(self, name, description, dueDate, effortEstimation, priority, group): # will interact with task
        return 0
    
    def select_task(self): #also might be just a gui interaction
        return 0
    
    def delete_task(self): # 
        return 0
    
    def update_task_info(self, name, description, dueDate, effortEstimation, priority, group): # pass new data and existing data of unchanged fields?
        return 0
    
    def add_task_group(self, group):  # interact with group class
        return 0
    
    def provide_group_info(self, name, color, habitType):
        return 0
    
    def delete_group(self):
        return 0
    
    def update_group_info(self, name, color, habitType): # possibly merge provide and update group info into a single function?
        return 0
    
    def review_progress_report(self): # call get progress report
        return 0
    
    # helpers/additional functions

    def create_account(self):
        return 0