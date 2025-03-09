

from transaction_manager import TransactionManager

from helpers.program_messages import ErrorMessages, SuccessMessages
from helpers.read_in_accounts import getUser
from helpers.money_parser import MoneyParser
from helpers.transaction_logger import TransactionLogger
from helpers.constants import TRANSFER_CAP, TRANSFER_IN_MSG, TRANSFER_OUT_MSG

from account import Account


class states:
    beforeTransfer = 0 # transfer, ask for name(admin) or number
    awaitAccountName = 1 # parse name given (admin), ask for number
    awaitAccountNumber = 2 # parse account number, ask for 2nd name
    awaitSecondAccountName = 3 # parse name, ask for 2nd number
    awaitSecondAccountNumber = 4 # parse number, ask for transfer amount
    awaitAmount = 5 # parse amount, return success or fail 
    transactionExit = -1 # flag transaction as finished (error or successful completion)


class TransferManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeTransfer
        self.transfer_out_user = self.user
        self.transfer_out_account = None
        self.transfer_in_user = None
        self.transfer_in_account = None

    def next(self, user_input):
        """
        
        transfer
        (ADMIN) > enter name to transfer from
        > enter account number to transfer from
        > enter name to transfer to
        > enter account number to transfer to
        > enter amount to transfer
        ||exit||
        """

        # abort transaction if not logged in
        if self.user == None:

            self.state = states.transactionExit
            return ErrorMessages.not_logged_in
            

        if self.state == states.beforeTransfer:
            
            # if the user is an admin, ask for an account name
            if self.user.isAdmin():

                self.state = states.awaitAccountName
                return SuccessMessages.enter_account_name

            # otherwise ask for account number
            self.state = states.awaitAccountNumber
            return SuccessMessages.enter_account_number
            
        
        elif self.state == states.awaitAccountName:
            # this is admin only

            # check that the user exists
            user_name, user = getUser(user_input)

            if user_name == "" or user == None:
                self.state = states.transactionExit
                return ErrorMessages.user_not_found
            
            # user exists, update transfer out user and ask for account number
            self.transfer_out_user = user

            self.state = states.awaitAccountNumber
            return SuccessMessages.enter_transfer_from_account_number
        

        elif self.state == states.awaitAccountNumber:

            # # validate account number
            # if not Account.validateAccountNumber(user_input):
            #     self.state = states.transactionExit
            #     return ErrorMessages.invalid_account_number
            
            # # Verify if account exists
            # self.transfer_out_account = self.transfer_out_user.getAccount(int(user_input))
            # if self.transfer_out_account == None:
            #     self.state = states.transactionExit
            #     return ErrorMessages.account_not_found

            try:
                
                self.transfer_out_account = TransactionManager.getAccountFromUser(self.transfer_out_user, user_input)
            
            except Exception as e:

                self.state = states.transactionExit
                return str(e)

            # ask for account name of receiving account
            self.state = states.awaitSecondAccountName
            return SuccessMessages.enter_transfer_to_account_name


        if self.state == states.awaitSecondAccountName:

            # check if user exists
            user_name, user = getUser(user_input)

            # check that the user exists
            if user_name == "" or user == None:
                self.state = states.transactionExit
                return ErrorMessages.user_not_found

            # set transfer to user, ask for account number
            self.transfer_in_user = user
            self.state = states.awaitSecondAccountNumber
            return SuccessMessages.enter_transfer_to_account_number


        if self.state == states.awaitSecondAccountNumber:

            try:

                self.transfer_in_account = TransactionManager.getAccountFromUser(self.transfer_in_user, user_input)
            
            except Exception as e:

                self.state = states.transactionExit
                return str(e)

            # block transfers into the same account that is being pulled from
            if self.transfer_in_account == self.transfer_out_account:

                self.state = states.transactionExit
                return ErrorMessages.cannot_transfer_to_yourself

            # Next part of the Transfer.
            self.state = states.awaitAmount
            return SuccessMessages.enter_transfer_amount
        

        if self.state == states.awaitAmount:
            
            # convert amount to be correct format
            amount:int = 0
            try:

                amount = MoneyParser.stringToInt(user_input)

            except Exception as e:
                self.state = states.transactionExit
                return ErrorMessages.invalid_amount
    
            # validate user can transfer the amount given
            if amount <= 0:
                self.state = states.transactionExit
                return ErrorMessages.amount_must_be_positive

            if self.transfer_out_user.amount_transferred + amount > TRANSFER_CAP:
                self.state = states.transactionExit
                return ErrorMessages.daily_transfer_cap
            
            if amount > self.transfer_out_account.balance:
                self.state = states.transactionExit
                return ErrorMessages.insufficient_funds


            # update account balances
            try:
                self.transfer_out_account.updateBalance(-amount)
            except:
                self.state = states.transactionExit
                return ErrorMessages.invalid_amount


            try:
                self.transfer_in_account.updateBalance(amount)
            except Exception as e:
                # revert
                self.transfer_out_account.updateBalance(amount)

                self.state = states.transactionExit
                return ErrorMessages.invalid_amount


            # update daily transfer amount if not admin
            if not self.user.isAdmin():
                self.transfer_out_user.amount_transferred += amount

            # log transfer
            try:
                TransactionLogger.writeTransaction(
                    TransactionLogger.codes.transfer,
                    self.transfer_out_user.name,
                    self.transfer_out_account.account_number,
                    amount,
                    misc=TRANSFER_OUT_MSG
                )
                TransactionLogger.writeTransaction(
                    TransactionLogger.codes.transfer,
                    self.transfer_in_user.name,
                    self.transfer_in_account.account_number,
                    amount,
                    misc=TRANSFER_IN_MSG
                )
            except:
                # revert balance changes
                self.transfer_out_account.updateBalance(amount)
                self.transfer_in_account.updateBalance(-amount)

                # exit with error message because it wasn't logged
                self.state = states.transactionExit
                return ErrorMessages.failed_to_log_transaction

            self.state = states.transactionExit
            return SuccessMessages.transfer_success


        self.state = states.transactionExit
        return ErrorMessages.state_machine_failure