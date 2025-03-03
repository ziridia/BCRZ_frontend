

from transaction_manager import TransactionManager
from helpers.program_messages import ErrorMessages, SuccessMessages
from helpers.read_in_accounts import USERS
from helpers.transaction_logger import TransactionLogger
from helpers.debug_tools import debugPrint
from account import Account

class states:
    beforeDelete = 0 # user just typed "delete", display appropriate message
    askName = 1 # ask for the bank account holders name
    askNumber = 2 # ask for the account number
    transactionExit = -1 # flag transaction as finished (error or successful completion)
    

class DeleteManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeDelete
        self.deleteUser = None
        self.account = None

    def next(self, user_input):

        if self.user == None:

            self.state = states.transactionExit
            return ErrorMessages.not_logged_in
            

        if not self.user.isAdmin():
            
            self.state = states.transactionExit
            return ErrorMessages.insufficient_permissions

        if self.state == states.beforeDelete:

            self.state = states.askName
            return SuccessMessages.enter_account_name
        
        elif self.state == states.askName:

            # validate that the name is valid
            # validate that the name exists
            for name,user in USERS.items():

                if name == user_input:
                    self.deleteUser = user
                    break
            else:

                self.state = states.transactionExit
                return ErrorMessages.user_not_found


            self.accountName = user_input
            
            self.state = states.askNumber
            return SuccessMessages.enter_account_number
        
        elif self.state == states.askNumber:

            # check that the account number is a valid format
            if not Account.validateAccountNumber(user_input):

                self.state = states.transactionExit
                return ErrorMessages.invalid_account_number

            # validate that the name-number pair exists
            for account in self.deleteUser.accounts:

                if account.account_number == int(user_input):
                    self.account = account
                    break
            else:

                self.state = states.transactionExit
                return ErrorMessages.account_not_found

            # write the transaction
            try:
                TransactionLogger.writeTransaction(
                    TransactionLogger.codes.delete,
                    self.deleteUser.name,
                    self.account.account_number,
                    0
                )
            except Exception as e:

                debugPrint(e)
                self.state = states.transactionExit
                return ErrorMessages.failed_to_log_transaction

            # flag the account as deleted
            self.account.isDeleted = True

            self.state = states.transactionExit
            return SuccessMessages.account_deleted
        
            
        return ErrorMessages.state_machine_failure


    def isComplete(self):
        return self.state == states.transactionExit

    def getUser(self):
        return self.user