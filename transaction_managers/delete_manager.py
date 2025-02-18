

from transaction_manager import TransactionManager

class states:
    beforeDelete = 0 # user just typed "withdrawal", display appropriate message
    transactionExit = -1 # flag transaction as finished (error or successful completion)


class DeleteManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeDelete

    def next(self, user_input):

        if self.state == states.beforeDelete:

            self.state = states.transactionExit
            return "message"
        
        return "error: state machine is not exiting properly"


    def isComplete(self):
        return self.state == states.transactionExit

    def getUser(self):
        return self.user