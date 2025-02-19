

from transaction_manager import TransactionManager
from transaction_logger import TransactionLogger

class states:
    beforeWithdrawal = 0 # user just typed "withdrawal", ask for account name (admin) or number (standard)
    getAccountNameAsAdmin = 1 # user just typed account name as admin
    getAccountNumber = 2 # user just typed the account number
    getAmountToWithdraw = 3 # user just typed the amount to withdraw
    transactionExit = -1 # flag transaction as finished (error or successful completion)


class WithdrawalManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeWithdrawal
        self.accountNumber = -1

    def next(self, user_input):

        if self.user == None:
            return "error: not logged in"

        if self.state == states.beforeWithdrawal:

            if self.user.isAdmin():

                self.state = states.getAccountNameAsAdmin
                return "enter account name"
            
            self.state = states.getAccountNumber
            return "enter account number"

        if self.state == states.getAccountNameAsAdmin:

            # find user account from users list
            return "error: not implemented"

            self.state = states.getAccountNumber
            return "enter account number"
            

        if self.state == states.getAccountNumber:

            return "error: not implemented"

            self.state = getAmountToWithdraw

            self.state = states.transactionExit

            try:

                TransactionLogger.writeTransaction(
                    TransactionLogger.codes.withdrawal,
                    "John Doe",
                    0,
                    500
                )

            except Exception as e:
                print(e)

            return "withdrawal message"
        
        return "error: state machine is not exiting properly"


    def isComplete(self):
        return self.state == states.transactionExit

    def getUser(self):
        return self.user