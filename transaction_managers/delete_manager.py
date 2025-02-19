

from transaction_manager import TransactionManager

class states:
    beforeDelete = 0 # user just typed "delete", display appropriate message
    askName = 1 # ask for the bank account holders name
    askNumber = 2 # ask for the account number
    transactionExit = -1 # flag transaction as finished (error or successful completion)
    

class DeleteManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeDelete
        self.accountName = ""
        self.accountNumber = ""

    def next(self, user_input):

        if self.state == states.beforeDelete:

            self.state = states.askName
            return "Enter the account holder's name"
        
        elif self.state == states.askName:
            self.accountName = user_input
            self.state = states.askNumber
            return "Enter the account number you wish to delete"
        
        elif self.state == states.askNumber:
            self.accountNumber = user_input
            self.state = states.transactionExit

            return f"Account holder: {self.accountName}. Account number {self.accountNumber} has been deleted."
        
            
        return "error: state machine is not exiting properly"


    def isComplete(self):
        return self.state == states.transactionExit

    def getUser(self):
        return self.user