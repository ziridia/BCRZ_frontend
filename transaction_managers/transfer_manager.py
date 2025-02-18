

from transaction_manager import TransactionManager

class states:
    beforeTransfer = 0 # user just typed "withdrawal", display appropriate message
    transactionExit = -1 # flag transaction as finished (error or successful completion)


class TransferManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeTransfer

    def next(self, user_input):

        if self.state == states.beforeTransfer:

            self.state = states.transactionExit
            return "message"
        
        return "error: state machine is not exiting properly"


    def isComplete(self):
        return self.state == states.transactionExit

    def getUser(self):
        return self.user