
from transaction_manager import TransactionManager
from helpers.transaction_logger import TransactionLogger
from transaction_managers.login_manager import LoginManager

from helpers.program_messages import ErrorMessages, SuccessMessages
from helpers.debug_tools import debugPrint
from helpers.money_parser import MoneyParser

from helpers.constants import RECEIVER_CODE_LENGTH, PAYBILL_COMPANIES, MAX_PAYBILL_AMOUNT

from helpers.read_in_accounts import getUser
from account import Account

class states:
    beforePaybill = 0 # user just typed "paybill", display appropriate message
    awaitAccountName = 1
    awaitAccountNumber = 2
    awaitReciever = 3
    awaitAmount = 4
    transactionExit = -1 # flag transaction as finished (error or successful completion)


class PaybillManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforePaybill
        
        self.paybill_user = user
        self.paybill_account = None
        self.receiver_index = ""
    

    def next(self, user_input):
        
        # abort transaction if not logged in
        if self.user == None:

            self.state = states.transactionExit
            return ErrorMessages.not_logged_in


        if self.state == states.beforePaybill:

            # ask for account name if admin
            if self.user.isAdmin():

                self.state = states.awaitAccountName
                return SuccessMessages.enter_account_name
            
            # otherwise ask for account number
            self.state = states.awaitAccountNumber
            return SuccessMessages.enter_account_number
        

        if self.state == states.awaitAccountName:

            # validate that the user exists
            name, self.paybill_user = getUser(user_input)
            
            if name == "" or self.paybill_user == None:

                self.state = states.transactionExit
                return ErrorMessages.user_not_found

            # ask for account number if the user exists
            self.state = states.awaitAccountNumber
            return SuccessMessages.enter_account_number


        if self.state == states.awaitAccountNumber:

            # check that the account number is valid
            try:
                self.paybill_account = TransactionManager.getAccountFromUser(self.paybill_user, user_input)
            
            except Exception as e:
                self.state = states.transactionExit
                return str(e)
            
                    
            # ask for the receiver code
            self.state = states.awaitReciever
            return SuccessMessages.enter_receiver_code

        
        if self.state == states.awaitReciever:

            # check if the user selected a valid company to pay bills to
            for code, name in PAYBILL_COMPANIES.items():

                if user_input == code.lower() or user_input == name.lower():
                    # match found, update receiver index and ask for the amount to pay
                    self.receiver_index = code
                    self.state = states.awaitAmount
                    return SuccessMessages.enter_amount

            # exit w/ error message if there was no receiver code match
            self.state = states.transactionExit
            return ErrorMessages.invalid_receiver_code
        

        if self.state == states.awaitAmount:
            
            try:
                # convert user input to int
                amount = MoneyParser.stringToInt(user_input)

                # make sure this wont exceed bill payment cap
                # only applies when its not an admin paying
                if not self.user.isAdmin() and self.paybill_user.amount_paid_in_bills + amount > MAX_PAYBILL_AMOUNT:

                    self.state = states.transactionExit
                    return ErrorMessages.bill_payment_too_high
                
                # make sure user has enough money
                if self.paybill_account.balance < amount:

                    self.state = states.transactionExit
                    return ErrorMessages.insufficient_funds
                # take users money
                self.paybill_account.updateBalance(-amount)

                # update the bill payment amount for the user
                if not self.user.isAdmin():
                    self.paybill_user.amount_paid_in_bills += amount

                # log transaction
                TransactionLogger.writeTransaction(
                    TransactionLogger.codes.paybill,
                    self.paybill_user.name,
                    self.paybill_account.account_number,
                    amount,
                    misc=self.receiver_index
                )

                # exit successfully
                self.state = states.transactionExit
                return SuccessMessages.bill_paid

            except Exception as e:
                
                debugPrint(e)
                self.state = states.transactionExit
                return ErrorMessages.invalid_amount


        self.state = states.transactionExit
        return ErrorMessages.state_machine_failure