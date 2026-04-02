class User:
    def __init__(self, userID, userName, email, hashedPassword):
        self.userID = userID
        self.userName = userName
        self.email = email
        self.hashedPassword = hashedPassword