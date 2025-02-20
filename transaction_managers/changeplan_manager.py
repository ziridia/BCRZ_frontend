

from transaction_manager import TransactionManager

from helpers.program_messages import ErrorMessages, SuccessMessages
from helpers.read_in_accounts import USERS, getUser
from helpers.transaction_logger import TransactionLogger

from account import Account

class states:
    beforeChangeplan = 0 # user just typed "changeplan", display appropriate message
    awaitAccountName = 1 # user just entered account name, ask for account number
    awaitAccountNumber = 2 # 
    transactionExit = -1 # flag transaction as finished (error or successful completion)


class ChangeplanManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeChangeplan
        self.changeplan_user = None

    def next(self, user_input):

        if self.state == states.beforeChangeplan:

            if not self.user.isAdmin():
                self.state = states.transactionExit
                return ErrorMessages.insufficient_permissions

            self.state = states.awaitAccountName
            return SuccessMessages.enter_account_name
        
        if self.state == states.awaitAccountName:
            
            user_name, self.changeplan_user = getUser(user_input)

            if user_name == "" or self.changeplan_user == None:
                self.state = states.transactionExit
                return ErrorMessages.user_not_found
            
            self.state = states.awaitAccountNumber
            return SuccessMessages.enter_account_number
        
        if self.state == states.awaitAccountNumber:

            if not Account.validateAccountNumber(user_input):
                self.state = states.transactionExit
                return ErrorMessages.invalid_account_number

            account = self.changeplan_user.getAccount(int(user_input))

            if account == None:
                self.state = states.transactionExit
                return ErrorMessages.account_not_found
            
            # No way to know if an account has a student plan from the current bank accounts file
            # ignore this check for the time being and always log the change
            # if not account.isStudentPlan:
            #     self.state = states.transactionExit
            #     return ErrorMessages.already_non_student

            try:
                TransactionLogger.writeTransaction(
                    TransactionLogger.codes.changeplan,
                    self.changeplan_user.name,
                    account.account_number,
                    0,
                )

                account.isStudentPlan = False
            except Exception as e:
                debugPrint(e)

                self.state = states.transactionExit
                return ErrorMessages.failed_to_log_transaction

            self.state = states.transactionExit
            return SuccessMessages.transaction_success


        return "error: state machine is not exiting properly"


    def isComplete(self):
        return self.state == states.transactionExit

    def getUser(self):
        return self.user