
from transaction_manager import TransactionManager

from helpers.program_messages import ErrorMessages, SuccessMessages
from helpers.read_in_accounts import getUser
from helpers.transaction_logger import TransactionLogger

from account import Account

class states:
    beforeChangeplan = 0 # user just typed "changeplan", display appropriate message
    awaitAccountName = 1 # user just entered account name, ask for account number
    awaitAccountNumber = 2 # 
    transactionExit = -1 # flag transaction as finished (error or successful completion)
    
 # Valid characters
def validate_input(user_input):
    valid_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

    # Check if the user_input contains only valid characters
    if all(char in valid_characters for char in user_input):
        return True
    else:
        return False

class ChangeplanManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeChangeplan
        self.changeplan_user = None

    def next(self, user_input):

        # ensure that someone is signed in
        if self.user == None:

            self.state = states.transactionExit
            return ErrorMessages.not_logged_in

        # user typed in "changeplan", display appropriate message
        if self.state == states.beforeChangeplan:

            # if the user isn't admin, return error message
            if not self.user.isAdmin():
                self.state = states.transactionExit
                return ErrorMessages.disallow_change

            # ask for the account name
            self.state = states.awaitAccountName
            return SuccessMessages.enter_account_name
        
        if self.state == states.awaitAccountName:
            
            # get the user object
            user_name, self.changeplan_user = getUser(user_input)
            
            if not validate_input(user_input):
                self.state = states.transactionExit
                return ErrorMessages.invalid_char
            
            # if a user wasn't found, return error message
            if self.changeplan_user == None:
                self.state = states.transactionExit
                return ErrorMessages.user_not_found
            
            if user_name == "":
                self.state = states.transactionExit
                return ErrorMessages.no_input
            
            # ask for account number
            self.state = states.awaitAccountNumber
            return SuccessMessages.enter_account_number
        
        if self.state == states.awaitAccountNumber:

            # get account object from user input
            try:

                account = TransactionManager.getAccountFromUser(self.changeplan_user, user_input)
                
                if account is None:
                    self.state = states.transactionExit
                    return ErrorMessages.no_match
                
                # Check transaction log for a previously changed plan transaction
                if TransactionLogger.hasTransaction(self.changeplan_user.name, account.account_number, TransactionLogger.codes.changeplan):
                    self.state = states.transactionExit
                    return ErrorMessages.previously_changed_to_student
            
            except Exception as e:

                self.state = states.transactionExit
                return str(e)
            
            # No way to know if an account has a student plan from the current bank accounts file
            # ignore this check for the time being and always log the change
            if not account.isStudentPlan:
                self.state = states.transactionExit
                print(ErrorMessages.already_non_student)
            else:
                return ErrorMessages.changed_to_non_student

            # log the transaction
            try:
                TransactionLogger.writeTransaction(
                    TransactionLogger.codes.changeplan,
                    self.changeplan_user.name,
                    account.account_number,
                    0,
                )

                account.isStudentPlan = False
            except Exception as e:
                print(e)

                self.state = states.transactionExit
                return ErrorMessages.failed_to_log_transaction

            # success message and exit
            self.state = states.transactionExit
            return SuccessMessages.transaction_success


        self.state = states.transactionExit
        return ErrorMessages.state_machine_failure