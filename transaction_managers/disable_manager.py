
from transaction_manager import TransactionManager
from helpers.program_messages import ErrorMessages, SuccessMessages
from helpers.read_in_accounts import getUser
from helpers.transaction_logger import TransactionLogger
from helpers.debug_tools import debugPrint
from account import Account

class states:
    beforeDisable = 0
    askName = 1
    askNumber = 2
    transactionExit = -1


class DisableManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeDisable
        self.disabledUser = None
        self.account = None

    def next(self, user_input):

        # abort transaction if not logged in
        if self.user == None:

            self.state = states.transactionExit
            return ErrorMessages.not_logged_in

        # abort transaction if not admin
        if not self.user.isAdmin():
            
            self.state = states.transactionExit
            return ErrorMessages.insufficient_permissions

        # request user account name
        if self.state == states.beforeDisable:

            self.state = states.askName
            return SuccessMessages.enter_account_name
        
        elif self.state == states.askName:

            # validate that the name is valid
            # validate that the name exists
            name, self.disabledUser = getUser(user_input)

            if name == "" or self.disabledUser == None:

                self.state = states.transactionExit
                return ErrorMessages.user_not_found
            
            # name found, ask for account number
            self.state = states.askNumber
            return SuccessMessages.enter_account_number
        
        elif self.state == states.askNumber:

            # check that the account number is a valid format
            if not Account.validateAccountNumber(user_input):

                self.state = states.transactionExit
                return ErrorMessages.invalid_account_number

            # validate that the name-number pair exists
            account = self.disabledUser.getAccount(int(user_input))

            if account == None:

                self.state = states.transactionExit
                return ErrorMessages.account_not_found

            # check if the account is disabled
            if account.isDisabled:
                self.state = states.transactionExit
                return ErrorMessages.account_disabled

            # check if the account is deleted
            if account.isDeleted:
                self.state = states.transactionExit
                return ErrorMessages.account_not_found
                
            # write the transaction
            try:
                TransactionLogger.writeTransaction(
                    TransactionLogger.codes.disable,
                    self.disabledUser.name,
                    account.account_number,
                    0
                )
            except Exception as e:

                debugPrint(e)
                self.state = states.transactionExit
                return ErrorMessages.failed_to_log_transaction

            # flag the account as disabled
            account.isDisabled = True

            self.state = states.transactionExit
            return SuccessMessages.account_disabled
        
        self.state = states.transactionExit
        return ErrorMessages.state_machine_failure