
from transaction_manager import TransactionManager
from helpers.program_messages import ErrorMessages, SuccessMessages
from helpers.read_in_accounts import getUser
from helpers.transaction_logger import TransactionLogger
from helpers.debug_tools import debugPrint
from helpers.money_parser import MoneyParser
from helpers.constants import MAX_BALANCE
from account import Account

class states:
    beforeDeposit = 0 # user just typed "deposit", display appropriate message
    awaitAccountName = 1
    awaitAccountNumber = 2
    awaitAmount = 3
    transactionExit = -1 # flag transaction as finished (error or successful completion)


class DepositManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeDeposit
        self.depositUser = user
        self.depositAccount = None

    def next(self, user_input):

        # abort transaction if not logged in
        if self.user == None:

            self.state = states.transactionExit
            return ErrorMessages.not_logged_in


        if self.state == states.beforeDeposit:
            
            # if the user is an admin, request the account name
            if self.user.isAdmin():
                self.state = states.awaitAccountName
                return SuccessMessages.enter_account_name
            
            # otherwise ask for the account number
            self.state = states.awaitAccountNumber
            return SuccessMessages.enter_account_number
        
        if self.state == states.awaitAccountName:

            # check if user exists
            name, self.depositUser = getUser(user_input)

            if name == "" or self.depositUser == None:

                self.state = states.transactionExit
                return ErrorMessages.user_not_found

            # ask for account number
            self.state = states.awaitAccountNumber
            return SuccessMessages.enter_account_number
        
        elif self.state == states.awaitAccountNumber:

            # get account from the user input
            try:

                self.depositAccount = TransactionManager.getAccountFromUser(self.depositUser, user_input)
            
            except Exception as e:

                self.state = states.transactionExit
                return str(e)

            # ask for amount to deposit            
            self.state = states.awaitAmount
            return SuccessMessages.enter_amount
        
        elif self.state == states.awaitAmount:
            try:
                # convert to int
                amount = MoneyParser.stringToInt(user_input)

                # check that its positive
                if amount <= 0:
                    self.state = states.transactionExit
                    return ErrorMessages.invalid_amount

                # make sure this wont exceed max bal
                if self.depositAccount.balance + amount > MAX_BALANCE:
                    self.state = states.transactionExit
                    return ErrorMessages.exceed_max_balance

                # update account balance
                self.depositAccount.updateBalance(amount)

                # write transaction to file
                TransactionLogger.writeTransaction(
                    TransactionLogger.codes.deposit,
                    self.depositUser.name,
                    self.depositAccount.account_number,
                    amount
                )

                self.depositUser.amount_deposited += amount

                self.state = states.transactionExit
                return SuccessMessages.deposit_success

            except Exception as e:
                debugPrint(e)
                self.state = states.transactionExit
                return ErrorMessages.invalid_amount
        
        self.state = states.transactionExit
        return ErrorMessages.state_machine_failure