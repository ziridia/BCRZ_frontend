



class User:
    def __init__(self, name, role, accounts=[]):
        self.name = name
        self.role = role
        self.accounts = accounts
    
    def isAdmin(self): 
        return self.role == "admin"