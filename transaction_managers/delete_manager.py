

from transaction_manager import TransactionManager
from helpers.program_messages import ErrorMessages, SuccessMessages
from helpers.read_in_accounts import getUser
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

    def next(self, user_input):

        # if the user is not logged in, abort transaction immediately
        if self.user == None:

            self.state = states.transactionExit
            return ErrorMessages.not_logged_in

        # if the user is not admin, abort transaction immediately
        if not self.user.isAdmin():
            
            self.state = states.transactionExit
            return ErrorMessages.insufficient_permissions

        # ask for the account name
        if self.state == states.beforeDelete:

            self.state = states.askName
            return SuccessMessages.enter_account_name
        
        elif self.state == states.askName:

            # validate that the account exists
            name, self.deleteUser = getUser(user_input)

            if name == "" or self.deleteUser == None:

                self.state = states.transactionExit
                return ErrorMessages.user_not_found

            # ask for account number once user was found
            self.state = states.askNumber
            return SuccessMessages.enter_account_number
        
        elif self.state == states.askNumber:

            # get account object from user input
            try:

                account = TransactionManager.getAccountFromUser(self.deleteUser, user_input)
            
            except Exception as e:

                self.state = states.transactionExit
                return str(e)

            # write the transaction
            try:
                TransactionLogger.writeTransaction(
                    TransactionLogger.codes.delete,
                    self.deleteUser.name,
                    account.account_number,
                    0
                )
            except Exception as e:

                debugPrint(e)
                self.state = states.transactionExit
                return ErrorMessages.failed_to_log_transaction

            # flag the account as deleted
            account.isDeleted = True

            # exit transaction successfully
            self.state = states.transactionExit
            return SuccessMessages.account_deleted
        
        self.state = states.transactionExit
        return ErrorMessages.state_machine_failure