
from transaction_manager import TransactionManager
from helpers.transaction_logger import TransactionLogger
from transaction_managers.login_manager import LoginManager

from helpers.program_messages import ErrorMessages, SuccessMessages
from helpers.debug_tools import debugPrint
from helpers.money_parser import MoneyParser

from helpers.constants import RECEIVER_CODE_LENGTH, PAYBILL_COMPANIES, MAX_PAYBILL_AMOUNT

from helpers.read_in_accounts import USERS
from account import Account

class states:
    beforePaybill = 0 # user just typed "paybill", display appropriate message
    transactionExit = -1 # flag transaction as finished (error or successful completion)
    awaitAccountName = 1
    awaitAccountNumber = 2
    awaitReciever = 3
    awaitAmount = 4


class PaybillManager(TransactionManager):
    """Company examples for bill payments, using reciever codes for company codes."""

    Company_Examples = {"EC": "The Bright Light Electric Company",
                        "CQ": "Credit Card Company Q",
                        "FI": "Fast Internet, Inc."}

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforePaybill
        
        self.paybill_user = user
        self.paybill_account = None
        self.receiver_index = ""
    

    def next(self, user_input):
        
        if self.user == None:

            self.state = states.transactionExit
            return ErrorMessages.not_logged_in


        if self.state == states.beforePaybill:

            if self.user.isAdmin():

                self.state = states.awaitAccountName
                return SuccessMessages.enter_account_name
            
            self.state = states.awaitAccountNumber
            return SuccessMessages.enter_account_number
        
        if self.state == states.awaitAccountName:

            # set paybill_user to the user that was entered
            # if it does not exist, return error message and exit
             # find user account from users list
            for name,user in USERS.items():
                if name == user_input:
                    self.paybill_user = user
                    self.state = states.awaitAccountNumber
                    return SuccessMessages.enter_account_number
            
            self.state = states.transactionExit
            return ErrorMessages.user_not_found

        if self.state == states.awaitAccountNumber:

            # check that the account number is valid
            if not Account.validateAccountNumber(user_input):

                self.state = states.transactionExit
                return ErrorMessages.invalid_account_number

            # check that the user has an account with that number
            for account in self.paybill_user.accounts:
                if account.account_number == int(user_input):
                    self.paybill_account = account

                    self.state = states.awaitReciever
                    return SuccessMessages.enter_receiver_code
                    
            
            self.state = states.transactionExit
            return ErrorMessages.account_not_found

        
        if self.state == states.awaitReciever:

            for code, name in PAYBILL_COMPANIES.items():

                if user_input == code.lower() or user_input == name.lower():
                    self.receiver_index = code
                    break

            else:
                self.state = states.transactionExit
                return ErrorMessages.invalid_receiver_code
                    
            self.state = states.awaitAmount
            return SuccessMessages.enter_amount
        

        if self.state == states.awaitAmount:
            
            try:
                # convert user input to int
                amount = MoneyParser.stringToInt(user_input)

                # make sure this wont exceed pill payment cap
                if self.paybill_user.amount_paid_in_bills + amount > MAX_PAYBILL_AMOUNT:

                    self.state = states.transactionExit
                    return ErrorMessages.invalid_amount
                
                # take users money
                self.paybill_account.updateBalance(-amount)

                # update the bill payment amount for the user
                self.paybill_user.amount_paid_in_bills += amount

                # log transaction
                TransactionLogger.writeTransaction(
                    TransactionLogger.codes.paybill,
                    self.paybill_user.name,
                    self.paybill_account.account_number,
                    amount,
                    misc=self.receiver_index
                )

                self.state = states.transactionExit
                return SuccessMessages.transaction_success

            except Exception as e:
                
                debugPrint(e)
                self.state = states.transactionExit
                return ErrorMessages.invalid_amount

        return ErrorMessages.state_machine_failure


    def isComplete(self):
        return self.state == states.transactionExit

    def getUser(self):
        return self.user