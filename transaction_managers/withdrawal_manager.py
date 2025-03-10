

from transaction_manager import TransactionManager
from helpers.transaction_logger import TransactionLogger
from transaction_managers.login_manager import LoginManager

from helpers.program_messages import ErrorMessages, SuccessMessages

from helpers.money_parser import MoneyParser

from helpers.constants import ACCOUNT_NUMBER_LENGTH, WITHDRAWAL_CAP

from helpers.read_in_accounts import getUser

from account import Account

class states:
    beforeWithdrawal = 0 # user just typed "withdrawal", ask for account name (admin) or number (standard)
    getAccountNameAsAdmin = 1 # user just typed account name as admin
    getAccountNumber = 2 # user just typed the account number
    getAmountToWithdraw = 3 # user just typed the amount to withdraw
    transactionExit = -1 # flag transaction as finished (error or successful completion)


class WithdrawalManager(TransactionManager):

    def __init__(self, user):
        self.user = user
        self.state:int = states.beforeWithdrawal
        self.account:Account = None
        self.withdrawal_user = self.user

    def next(self, user_input):

        if self.user == None:

            self.state = states.transactionExit
            return ErrorMessages.not_logged_in

        if self.state == states.beforeWithdrawal:

            if self.user.isAdmin():

                self.state = states.getAccountNameAsAdmin
                return SuccessMessages.enter_account_name
            
            self.state = states.getAccountNumber            
            return SuccessMessages.enter_account_number

        if self.state == states.getAccountNameAsAdmin:

            # find user account from users list
            name, self.withdrawal_user = getUser(user_input)

            if name == "" or self.withdrawal_user == None:

                self.state = states.transactionExit
                return ErrorMessages.user_not_found
            
            # user was found, ask for account number
            self.state = states.getAccountNumber
            return SuccessMessages.enter_account_number
            

        if self.state == states.getAccountNumber:

            try:

                self.account = TransactionManager.getAccountFromUser(self.withdrawal_user, user_input)
            
            except Exception as e:

                self.state = states.transactionExit
                return str(e)

            # account exists for this user, ask for amount to withdraw
            self.state = states.getAmountToWithdraw
            return SuccessMessages.enter_amount_to_withdraw

        if self.state == states.getAmountToWithdraw:

            # parse the amount given by the user
            amount:int = 0
            try:
                # convert user input to correct format
                amount = MoneyParser.stringToInt(user_input)

            except:
                self.state = states.transactionExit
                return ErrorMessages.invalid_amount

            if amount <= 0:
                self.state = states.transactionExit
                return ErrorMessages.amount_must_be_positive

            if amount > self.account.balance:
                self.state = states.transactionExit
                return ErrorMessages.insufficient_funds

            if self.withdrawal_user.amount_withdrawn + amount > WITHDRAWAL_CAP and not self.user.isAdmin():
                self.state = states.transactionExit
                return ErrorMessages.daily_withdrawal_cap

            # make sure that this wouldn't eat into deposited amount this session
            if self.account.balance - self.withdrawal_user.amount_deposited < amount:
                self.state = states.transactionExit
                return ErrorMessages.cannot_access_deposited_funds


            # attempt to update the balance of the account
            try:

                self.account.updateBalance(-amount)

            except:
                self.state = states.transactionExit

                # this ideally should never be reached
                return ErrorMessages.invalid_amount

            # do not update withdrawn amount if done by an admin
            # but do update it if a standard user
            if not self.user.isAdmin():
                self.withdrawal_user.amount_withdrawn += amount

            # log transaction
            try:
                TransactionLogger.writeTransaction(
                    TransactionLogger.codes.withdrawal,
                    self.withdrawal_user.name,
                    self.account.account_number,
                    amount
                )
            except: 

                try:
                    self.account.updateBalance(amount)
                except:
                    self.state = states.transactionExit
                    return ErrorMessages.failed_to_revert_transaction

                self.state = states.transactionExit
                return ErrorMessages.failed_to_log_transaction

            self.state = states.transactionExit
            return SuccessMessages.withdrawal_success
        
        self.state = states.transactionExit
        return ErrorMessages.state_machine_failure
