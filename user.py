class User:
    def __init__(self, name="username", role=""):
        self.name = "username"
        self.role = role
    
    # Check if the current user is of type admin
    def isAdmin(self): 
        return self.role == ""
        
    def setRole(self, role):
        self.role = role.lower()