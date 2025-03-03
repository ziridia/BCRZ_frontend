
from transaction_manager import TransactionManager
from helpers.program_messages import ErrorMessages, SuccessMessages
from helpers.read_in_accounts import USERS
from helpers.transaction_logger import TransactionLogger
from helpers.debug_tools import debugPrint
from helpers.money_parser import MoneyParser
from account import Account

class states:
    beforeDeposit = 0 # user just typed "deposit", display appropriate message
    transactionExit = -1 # flag transaction as finished (error or successful completion)
    awaitAccountName = 1
    awaitAccountNumber = 2
    awaitAmount = 3


class DepositManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeDeposit
        self.depositUser = user
        self.depositAccount = None

    def next(self, user_input):

        if self.state == states.beforeDeposit:
            
            if self.user.isAdmin():
                self.state = states.awaitAccountName
                return SuccessMessages.enter_account_name
            
            self.state = states.awaitAccountNumber
            return SuccessMessages.enter_account_number
        
        if self.state == states.awaitAccountName:

            # check if user exists
            for name,user in USERS.items():

                if name == user_input:
                    self.depositUser = user
                    break
            else:

                self.state = states.transactionExit
                return ErrorMessages.user_not_found

            # ask for account number
            self.state = states.awaitAccountNumber
            return SuccessMessages.enter_account_number
        
        elif self.state == states.awaitAccountNumber:

            # check if account exists for this user
            # check that the account number is a valid format
            if not Account.validateAccountNumber(user_input):

                self.state = states.transactionExit
                return ErrorMessages.invalid_account_number

            # validate that the name-number pair exists
            for account in self.depositUser.accounts:

                if account.account_number == int(user_input):
                    self.depositAccount = account
                    break
            else:

                self.state = states.transactionExit
                return ErrorMessages.account_not_found

            # ask for amount to deposit            
            self.state = states.awaitAmount
            return SuccessMessages.enter_amount
        
        elif self.state == states.awaitAmount:
            try:
                # convert to int
                amount = MoneyParser.stringToInt(user_input)

                # check that its positive
                if amount <= 0:
                    self.state = states.transactionExit
                    return ErrorMessages.invalid_amount

                # update account balance
                self.depositAccount.updateBalance(amount)

                # write transaction to file
                TransactionLogger.writeTransaction(
                    TransactionLogger.codes.deposit,
                    self.depositUser.name,
                    self.depositAccount.account_number,
                    amount
                )

                self.state = states.transactionExit
                return SuccessMessages.deposit_success

            except Exception as e:
                debugPrint(e)
                self.state = states.transactionExit
                return ErrorMessages.invalid_amount
        
        return "error: state machine is not exiting properly"


    def isComplete(self):
        return self.state == states.transactionExit

    def getUser(self):
        return self.user