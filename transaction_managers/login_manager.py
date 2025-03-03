
from helpers.read_in_accounts import readInAccounts, getUser, USERS
from helpers.constants import ADMIN, STANDARD
from helpers.program_messages import ErrorMessages, SuccessMessages

from transaction_manager import TransactionManager

from user import User


class states:
    beforeLogin = 0 # prompt user to enter session type
    awaitSessionType = 1 # prompt user to enter standard or admin
    awaitAccountName = 2 # prompt user to enter account name
    transactionExit = -1 # flag transaction as finished (error or successful completion)


class LoginManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeLogin

    def next(self, user_input):

        if self.user != None:

            self.state = states.transactionExit
            return ErrorMessages.already_logged_in


        if self.state == states.beforeLogin:

            self.state = states.awaitSessionType
            return SuccessMessages.select_session_type
            

        if self.state == states.awaitSessionType:
            
            if user_input == STANDARD:
                
                self.state = states.awaitAccountName
                return SuccessMessages.enter_account_name

            if user_input == ADMIN:

                self.user = User(ADMIN, list(), role=ADMIN)

                self.state = states.transactionExit
                return SuccessMessages.logged_in

            # no expected input was matched, so they gave bad input.
            # give an error message and exit the transaction
            self.state = states.transactionExit
            return ErrorMessages.invalid_session_type


        if self.state == states.awaitAccountName:

            # get user from user list
            name, self.user = getUser(user_input)
            
            # if user doesn't exist, exit with error message
            if self.user == None:
                self.state = states.transactionExit
                return ErrorMessages.user_not_found
            
            # return success message
            self.state = states.transactionExit
            return SuccessMessages.logged_in

        self.state = states.transactionExit
        return ErrorMessages.state_machine_failure