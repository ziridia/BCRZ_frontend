
from abc import ABC, abstractmethod
from helpers.read_in_accounts import getUser
from helpers.program_messages import ErrorMessages, SuccessMessages
from account import Account
from user import User

# this is an abstract class that all other transaction managers should inherit from, and
# are expected to implement all methods of this class
class TransactionManager(ABC):
    
    # take the next input for the transaction and parse it accordingly
    @abstractmethod
    def next(self, user_input):
        pass

    # return true if the transaction is complete; false otherwise
    def isComplete(self):
        return self.state == -1

    # this should basically just keep track of the active user
    @abstractmethod
    def __init__(self, user):
        pass

    # should return a user object
    def getUser(self):
        return self.user
    
    # see if user has an account and return the account object
    def getAccountFromUser(user:User, account_number:str):
        """
        user: User object
        account_number: string representation of the account number
        validates account number, confirms if user has the account
        if account not found: throws an error
        if disabled/deleted: throws an error
        error message is printable
        """

        # check account number is valid
        if not Account.validateAccountNumber(account_number):
            raise Exception(ErrorMessages.invalid_account_number)
        
        # get account from user
        account = user.getAccount(int(account_number))

        # if the account doesn't exist or has been deleted, say its not found
        if account == None or account.isDeleted:
            raise Exception(ErrorMessages.account_not_found)

        # if the account has been disabled, give appropriate error
        if account.isDisabled:
            raise Exception(ErrorMessages.account_disabled)

        return account 

