
from account import Account


class User:
    def __init__(self, name, accounts:list, role="standard"):
        self.name = name
        self.role = role
        self.accounts = accounts
    
    def isAdmin(self): 
        return self.role == "admin"

    def addAccount(self, account:Account):

        for acc in self.accounts:

            if acc.account_number == account.account_number:
                raise Exception("Cannot have two accounts with the same number belonging to the same user")

        self.accounts.append(account)
        print(self.name, self.accounts)

    def __str__(self):
        return f"User: {self.name} role:{self.role}, accounts:{self.accounts}"