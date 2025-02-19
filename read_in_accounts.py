
from user import User
from account import Account

def createAccountFromString(account_string:str):

    if len(account_string) != 37:
        raise ValueError("account string length is not 37 characters")
    
    account_number  = account_string[0:5]
    account_name    = account_string[6:26].strip()
    account_status  = account_string[27:28]
    account_balance = account_string[29:]

    
    return Account(
        int(account_number),
        int(account_balance),
        isDisabled=account_status == "D",
    ), account_name.lower()

def readInAccounts(path:str):
    """
    path should be a path to the current accounts file.

    Function returns a dict of user objects
    key is the user name
    value is the user object
    """

    # Read in 1 line at a time.
    # Check current users to see if the user for the line being read in exists
    # if it doesn't
        # create new user, add to user list
    # create account for the user on the line, add to the user object

    accounts_file = open(path, 'r')
    
    users = dict()

    for line in accounts_file:
        
        # get account and account name from the line
        account, user_name = createAccountFromString(line.strip())

        # check to see if the account name is in the dict of accounts
        
        if user_name not in users:
                        
            users[user_name] = User(user_name, accounts=list())

        # add the account for the current user to its account list
        users[user_name].addAccount(account)

    return users