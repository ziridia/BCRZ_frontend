

from transaction_manager import TransactionManager

class states:
    beforeDeposit = 0 # user just typed "withdrawal", display appropriate message
    transactionExit = -1 # flag transaction as finished (error or successful completion)
    awaitAccountName = 1
    awaitAccountNumber = 2
    awaitAmount = 3


class DepositManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeDeposit
        self.account_name = None
        self.account_number = None
        self.amount = None
        self.deposit = []
        self.accountBalance = 1000

    def next(self, user_input):

        if self.state == states.beforeDeposit:
            self.state = states.awaitAccountName
            return "Enter Account name: "
        
        elif self.state == states.awaitAccountName:
            self.state = states.awaitAccountNumber
            self.account_name = user_input
            return "Enter Account Number: "
        
        elif self.state == states.awaitAccountNumber:
            self.state = states.awaitAmount
            self.account_number = user_input
            return "Enter amount to be deposited: "
        
        elif self.state == states.awaitAmount:
            try:
                self.amount = float(user_input)

                # proceed with deposit

                self.accountBalance += self.amount

                #transfer = f"04_{self.account_name}_{self.account_number}_{self.amount}"
                #self.deposit.append(transfer)

                self.state = states.transactionExit
                return f"Successfully deposited {self.amount}. New account balance: {self.accountBalance}"
            except ValueError:
                return f"Error: Invalid input. Please enter a numeric value and not {self.amount}"
        
        return "error: state machine is not exiting properly"


    def isComplete(self):
        return self.state == states.transactionExit

    def getUser(self):
        return self.user