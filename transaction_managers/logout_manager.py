

from transaction_manager import TransactionManager

class states:
    beforeLogout = 0
    transactionExit = -1 # flag transaction as finished (error or successful completion)


class LogoutManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeLogout

    def next(self, user_input):

        if self.user == None:
            self.state = states.transactionExit
            return "error: not logged in"
                
        self.state = states.transactionExit
        self.user = None
        return "logged out"


    def isComplete(self):
        return self.state == states.transactionExit

    def getUser(self):
        return self.user