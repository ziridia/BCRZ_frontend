

from transaction_manager import TransactionManager
from transaction_logger import TransactionLogger
from transaction_managers.login_manager import LoginManager


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
            return "error: not logged in"

        if self.state == states.beforeWithdrawal:

            if self.user.isAdmin():

                self.state = states.getAccountNameAsAdmin
                return "enter account name"
            
            self.state = states.getAccountNumber
            return "enter account number"

        if self.state == states.getAccountNameAsAdmin:

            # find user account from users list
            for name,user in LoginManager.users.items():
                if name == user_input:
                    self.withdrawal_user = user
                    self.state = states.getAccountNumber
                    return "enter account number"
            else:
                self.state = states.transactionExit
                return "error: user does not exist"

            
            

        if self.state == states.getAccountNumber:

            # check if the account number provided is valid
            # confirm its a number
            try:
                int(user_input)
            except:
                self.state = states.transactionExit
                return "error: invalid account number"
            
            # confirm its 5 digits
            if len(user_input) != 5:
                self.state = states.transactionExit
                return "error: invalid account number"
            
            # confirm the account exists in the user accounts list
            valid_account:bool = False
            for account in self.withdrawal_user.accounts:
                if account.account_number == int(user_input):
                    self.account = account
                    valid_account = True
                    break
            
            if not valid_account:
                self.state = states.transactionExit
                return "error: account does not exist"

            # account exists for this user, ask for amount to withdraw
            self.state = states.getAmountToWithdraw
            return "enter amount to withdraw"

        if self.state == states.getAmountToWithdraw:

            # parse the amount given by the user
            amount:int = 0
            try:
                # convert to float & multiply by 100 then cast to int so that an input of $100.96 becomes 10096 to remove decimal. 
                # Additional decimals are removed
                amount = int(float(user_input) * 100)

            except:

                self.state = states.transactionExit
                return "error: invalid amount to withdraw"

            if amount <= 0:
                self.state = states.transactionExit
                return "error: amount must be positive"

            if self.withdrawal_user.amount_withdrawn + amount > 500_00 and not self.user.isAdmin():
                self.state = states.transactionExit
                return "error: cannot exceed daily withdrawal cap of $500.00"

            if amount > self.account.balance:
                self.state = states.transactionExit
                return "error: amount to withdraw cannot exceed account balance"

            # attempt to update the balance of the account
            try:

                self.account.updateBalance(amount)

            except Exception as e:
                self.state = states.transactionExit
                return "error: invalid amount to withdraw"

            # do not update withdrawn amount if done by an admin
            # but do update it if a standard user
            if not self.user.isAdmin():
                self.withdrawal_user.amount_withdrawn += amount

            try:
                TransactionLogger.writeTransaction(
                    TransactionLogger.codes.withdrawal,
                    self.withdrawal_user.name,
                    self.account.account_number,
                    amount
                )
            except: 

                try:
                    self.account.updateBalance(-amount)
                except:
                    self.state = states.transactionExit
                    return "error: unable to revert transaction after failing to log"

                self.state = states.transactionExit
                return "error: unable to log transaction -- aborting"

            self.state = states.transactionExit
            return "withdrawal successful"
        
        return "error: state machine is not exiting properly"


    def isComplete(self):
        return self.state == states.transactionExit

    def getUser(self):
        return self.user