

from transaction_manager import transactionManager

class LoginManager(TransactionManager):

    int state = 0

    user = None

    def __init__(self, user):
        self.user = user    

    def next(self, input):

        if self.state == 0:

            if input == "standard":
                self.state = 1

            if input == "admin":
                self.state = -1

                return "logged in"

        elif self.state == 1:
            
            self.state = 2
            return "enter account name"

        elif self.state == 3:
            
            self.state = -1
            # see if the input matches any user accounts
            # if so, update the user, return success message

            # if not, return error message
            return "error: user not found" # double check what the error message in the tests is and make this match


    def isComplete(self):
        return self.state == -1

    def getUser(self):
        return self.user