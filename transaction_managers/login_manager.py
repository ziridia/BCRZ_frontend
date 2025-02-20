
from helpers.read_in_accounts import readInAccounts
from helpers.read_in_accounts import USERS

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

        if self.state == states.beforeLogin:

            self.state = states.awaitSessionType
            return "enter session type (standard or admin)"

            
        elif self.state == states.awaitSessionType:
            
            if user_input == "standard":
                # self.user.setRole("standard")
                self.state = states.awaitAccountName

                return "enter account name"

            if user_input == "admin":
                # self.user.setRole("admin")
                self.user = User("admin", list(), role="admin")
                self.state = states.transactionExit

                return "logged in"

            # no expected input was matched, so they gave bad input.
            # give an error message and exit the transaction
            self.state = states.transactionExit
            return "error: error message"

        elif self.state == states.awaitAccountName:

            # if user doesn't exist return error message
            if user_input not in USERS:
                self.state = states.transactionExit
                return "error: user not found"

            # see if the input matches any user accounts
            # if so, update the user, return success message
            self.state = states.transactionExit
            self.user = USERS[user_input]
            return "logged in"


        # this should never be reached. Means that this function was called despite the transaction
        # being marked as complete
        return "error: state machine is not exiting properly"


    def isComplete(self):
        return self.state == states.transactionExit

    def getUser(self):
        return self.user