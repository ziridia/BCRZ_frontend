
class account:
    """
    Each account has a(n):
        account number
        balance
        flag on if its a student plan
        flag if its disabled
        flag if its deleted
    """

    def __init__(self, account_number:int, balance:int = 0, isStudentPlan:bool = False, isDisabled:bool = False, isDeleted:bool = False):
        self.account_number = account_number
        self.balance = balance
        self.isStudentPlan = isStudentPlan
        self.isDisabled = isDisabled
        self.isDeleted = isDeleted

    def updateBalance(amount:int):
        """
        Ensures only valid changes to balance occurs. Changes that will cause balance to become negative or exceed $999,999.99 will raise an exception

        Amount can be positive or negative. Floating point values are not valid.
        """

        if self.isDisabled:
            raise Exception("cannot perform transactions on disabled accounts")

        if self.isDeleted:
            raise Exception("cannot perform transactions on deleted accounts")

        if self.balance - amount < 0:
            raise ValueError("amount to remove cannot be greater than the balance")

        if self.balance + amount > 999_999_99:
            raise ValueError("account balance cannot be greater than $999,999.99")

        self.balance += amount
    
    def disable():
        self.isDisabled = False