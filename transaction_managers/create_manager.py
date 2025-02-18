

from transaction_manager import TransactionManager

class states:
    beforeCreate = 0 # user just typed "create", display appropriate message
    askName = 1
    askBalance = 2
    transactionExit = -1 # flag transaction as finished (error or successful completion)

class CreateManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeCreate
        self.accountName = ""
        self.initialBalance = 0.0

    def next(self, user_input):
        print("reached create manager. ")
        if self.state == states.beforeCreate:
            # Check if the user is an admin before creation
            # For now will allow creation to be made regardless
            # if not self.user.isAdmin():
            #     print("user is not an admin")
            #     self.state = states.transactionExit
            #     return "error: create is a privileged transaction"
            
            self.state = states.askName
            return "Enter account holder name:"
        
        # Creation of the account holder name
        elif self.state == states.askName: 
            if len(user_input) > 20:
                return "error: account holder name must be at most 20 characters long"

            self.accountName = user_input
            print("the account name is called: " ,self.accountName)
            self.state = states.askBalance
            return "Enter initial balance:"
        
        # Initial balance for the new account
        elif self.state == states.askBalance:
            try:
                balance = float(user_input)

                if balance < 0 or balance > 99999.99:
                    return "error: balance must be between $0 and $99999.99"
                
                self.initialBalance = balance
                # exit create transaction
                self.state = states.transactionExit
                
                return f"Account '{self.accountName}' created with balance of ${self.initialBalance}"
            except ValueError:
                return "error: invalid balance format, please enter a number correctly "
            
        return "error: unexpected input"

    def isComplete(self):
        return self.state == states.transactionExit

    def getUser(self):
        return self.user