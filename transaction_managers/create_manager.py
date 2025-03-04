

from transaction_manager import TransactionManager

from helpers.program_messages import ErrorMessages, SuccessMessages
from helpers.debug_tools import debugPrint
from helpers.transaction_logger import TransactionLogger
from helpers.read_in_accounts import getUser, getListOfAllUsers
from helpers.money_parser import MoneyParser
from helpers.constants import MAX_ACCOUNT_NAME_LENGTH, MAX_BALANCE

from account import Account
from user import User

class states:
    beforeCreate = 0 # user just typed "create", display appropriate message
    awaitAccountName = 1 # user entered the account name
    awaitAccountNumber = 2 # user entered account number
    awaitBalance = 3 # user entered the account balance
    transactionExit = -1 # flag transaction as finished (error or successful completion)

class CreateManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeCreate
        self.createdUser = None
        self.createdAccount = None

    def next(self, user_input):

        if self.user == None:

            self.state = states.transactionExit
            return ErrorMessages.not_logged_in


        if not self.user.isAdmin():
            # user is not an admin, abort transaction
            self.state = states.transactionExit
            return ErrorMessages.insufficient_permissions

        # no input; prompt user for account name
        if self.state == states.beforeCreate:
            
            self.state = states.awaitAccountName
            return SuccessMessages.enter_account_name
        
        # account name input; request account number
        if self.state == states.awaitAccountName: 

            # validate that the name is a valid length
            if len(user_input) > MAX_ACCOUNT_NAME_LENGTH or len(user_input) < 1:

                self.state = states.transactionExit
                return ErrorMessages.name_too_long

            # check if the name has any special characters
            if not user_input.isalpha():

                self.state = states.transactionExit
                return ErrorMessages.must_be_alpha

            # validate that the name is unique
            # specification does not say the name needs to be unique
            # does this mean that a person doesn't necessarily have multiple accounts under their name
            # and that anyone with the same name just has access to each others accouns?
            # seems like a deeply flawed implentation

            # check if the user exists
            # if it does, save reference to it
            name, self.createdUser = getUser(user_input)

            # if it doesn't, crease a new user object
            if name == "" or self.createdUser == None:

                self.createdUser = User(
                    user_input, # name
                    list() # account list
                )
                # add new user to user list
                USERS = getListOfAllUsers()
                USERS[user_input] = self.createdUser

            debugPrint(f"the account name is called: {self.createdUser.name}")

            # prompt for the account number
            self.state = states.awaitAccountNumber
            return SuccessMessages.enter_account_number
        
        # account number input; request initial balance
        if self.state == states.awaitAccountNumber:

            # check that the number is valid (dimensions)
            if not Account.validateAccountNumber(user_input):

                self.state = states.transactionExit
                return ErrorMessages.invalid_account_number
            
            # check that it is not a duplicate
            self.createdAccount = self.createdUser.getAccount(int(user_input))

            # account is a duplicate, abort creation
            if self.createdAccount != None:

                self.state = states.transactionExit
                return ErrorMessages.account_already_exists

            # account is not a duplicate, so create a new account
            self.createdAccount = Account(
                int(user_input) # account number
            )

            # disable account
            # we don't need to update the balance here because transactions cannot occur on it
            self.createdAccount.disable()

            # assign account to the user
            self.createdUser.addAccount(self.createdAccount)
            
            # ask for starting account balance
            self.state = states.awaitBalance
            return SuccessMessages.enter_starting_balance


        # balance as input; transaction exit here
        if self.state == states.awaitBalance:
            try:
                balance:int = MoneyParser.stringToInt(user_input)

                debugPrint(f"{type(balance)}, {balance}")
                if balance < 0 or balance > MAX_BALANCE:
                    return ErrorMessages.exceed_max_balance
                
                # create transaction logging the creation of the account
                TransactionLogger.writeTransaction(
                    TransactionLogger.codes.create,
                    self.createdUser.name,
                    self.createdAccount.account_number,
                    balance
                )

                # add user to the user list, mark it as disabled
                # necessary for checking to prevent accounts with the same name being created in the same session

                self.state = states.transactionExit
                return SuccessMessages.account_created

            except ValueError as e:
                
                debugPrint(e)
                self.state = states.transactionExit
                return ErrorMessages.invalid_amount
            
        self.state = states.transactionExit
        return ErrorMessages.state_machine_failure