
from transaction_manager import TransactionManager
from helpers.program_messages import ErrorMessages, SuccessMessages
from helpers.debug_tools import debugPrint
from helpers.transaction_logger import TransactionLogger

class states:
    beforeLogout = 0
    transactionExit = -1 # flag transaction as finished (error or successful completion)


class LogoutManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeLogout

    def next(self, user_input):

        # abort transaction if not logged in
        if self.user == None:

            self.state = states.transactionExit
            return ErrorMessages.not_logged_in

        # log the logout transaction
        try:
            TransactionLogger.writeTransaction(
                TransactionLogger.codes.logout,
                self.user.name,
                0,
                0,
            )

        except Exception as e:
            debugPrint(e)

            self.state = states.transactionExit
            return ErrorMessages.failed_to_log_transaction

        # update user to None and exit
        self.state = states.transactionExit
        self.user = None
        return SuccessMessages.logged_out