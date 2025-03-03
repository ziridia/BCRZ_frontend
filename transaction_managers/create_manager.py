

from transaction_manager import TransactionManager

from helpers.program_messages import ErrorMessages, SuccessMessages
from helpers.debug_tools import debugPrint
from helpers.transaction_logger import TransactionLogger
from helpers.read_in_accounts import USERS, getUser
from helpers.money_parser import MoneyParser
from helpers.constants import MAX_ACCOUNT_NAME_LENGTH, MAX_BALANCE

from account import Account

class states:
    beforeCreate = 0 # user just typed "create", display appropriate message
    askName = 1 # user entered the account name
    askNumber = 2 # user entered 
    askBalance = 3 # user entered the account balance
    transactionExit = -1 # flag transaction as finished (error or successful completion)

class CreateManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeCreate
        self.accountName = ""
        self.accountNumber = ""

    def next(self, user_input):

        if not self.user.isAdmin():
            # user is not an admin, abort transaction
            self.state = states.transactionExit
            return ErrorMessages.insufficient_permissions

        # no input; prompt user for account name
        if self.state == states.beforeCreate:
            
            self.state = states.askName
            return SuccessMessages.enter_account_name
        
        # account name input; request account number
        if self.state == states.askName: 

            # validate that the name is a valid length
            if len(user_input) > MAX_ACCOUNT_NAME_LENGTH or len(user_input) < 1:

                self.state = states.transactionExit
                return ErrorMessages.name_too_long

            # validate that the name is unique
            # specification does not say the name needs to be unique
            # does this mean that a person doesn't necessarily have multiple accounts under their name
            # and that anyone with the same name just has access to each others accouns?
            # seems like a deeply flawed implentation


            self.accountName = user_input
            debugPrint(f"the account name is called: {self.accountName}")

            # prompt for the account number
            self.state = states.askNumber
            return SuccessMessages.enter_account_number
        
        # account number input; request initial balance
        if self.state == states.askNumber:

            # check that the number is valid (dimensions)
            if not Account.validateAccountNumber(user_input):

                self.state = states.transactionExit
                return ErrorMessages.invalid_account_number
            
            # check that it is not a duplicate (system wide)
            pass

            self.accountNumber = user_input
            
            self.state = states.askBalance
            return SuccessMessages.enter_starting_balance


        # balance as input; transaction exit here
        if self.state == states.askBalance:
            try:
                balance:int = MoneyParser.stringToInt(user_input)

                debugPrint(f"{type(balance)}, {balance}")
                if balance < 0 or balance > MAX_BALANCE:
                    return ErrorMessages.exceed_max_balance
                
                # create transaction logging the creation of the account
                TransactionLogger.writeTransaction(
                    TransactionLogger.codes.create,
                    self.accountName,
                    int(self.accountNumber),
                    balance
                )

                # add user to the user list, mark it as disabled
                # necessary for checking to prevent accounts with the same name being created in the same session

                self.state = states.transactionExit
                return SuccessMessages.account_created

            except ValueError as e:
                
                debugPrint(e)
                self.state = states.transactionExit
                return invalid_amount
            
        return ErrorMessages.state_machine_failure

    def isComplete(self):
        return self.state == states.transactionExit

    def getUser(self):
        return self.user