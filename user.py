class User:
    def __init__(self):
        self.name = "username"
        self.role = ""
    
    # Check if the current user is of type admin
    def isAdmin(self): 
        return self.role == ""
        
    