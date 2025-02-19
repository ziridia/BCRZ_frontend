
from transaction_manager import TransactionManager

class states:
    beforePaybill = 0 # user just typed "withdrawal", display appropriate message
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
        self.account_name = None
        self.account_number = None
        self.reciever_index = None
        self.amount = None
        self.accountBalance = 1000
        """Logging transactions so they can be printed."""
        self.transactions = []
    

    def next(self, user_input):
        
        if self.state == states.beforePaybill:
            self.state = states.awaitAccountName
            return "Enter account name: "
        
        elif self.state == states.awaitAccountName:
            self.state = states.awaitAccountNumber
            self.account_name = user_input
            return "Enter account number: "
        
        elif self.state == states.awaitAccountNumber:
            # Verify if account exists

            # Next Part of the transaction.
            self.account_number = user_input
            self.state = states.awaitReciever
            return "Enter Reciever code (EC, CQ, FI): "

        elif self.state == states.awaitReciever:
            # Verify if Reciever code is a vaild code.
            if user_input.strip().upper() not in self.Company_Examples:
                return "Error: Invaild Reciever code"
            
            else:
                # Next part of the transaction.
                self.reciever_index = user_input.strip().upper()
                self.state = states.awaitAmount
                return "Enter amount for bill payment: "
        
        elif self.state == states.awaitAmount:
            # Check if amount is valid and proceed with the transaction.
            try:
                self.amount = float(user_input)

                if self.amount < 0 or self.amount > 2000:
                    return f"Error: Invalid amount. Must be between 0 and 2000. Inputed: {self.amount}"
                
                # Example for exceeding account balance:
                if self.amount > self.accountBalance:
                    return f"Error: Invalid amount. Exceeds account balance. Inputed: {self.amount}"
                
                # Recording transaction for logs
                #transaction = f"03_{self.account_name}_{self.account_number}_{self.amount}_{self.reciever_index}"
                #self.transactions.append(transaction)

                self.state = states.transactionExit
                return f"Bill Payment of {self.amount} to {self.Company_Examples[self.reciever_index]} completed."

            except ValueError:
                return f"Error: Invalid input. Please enter a numeric value and not {self.amount}"
        
        return "error: state machine is not exiting properly"


    def isComplete(self):
        return self.state == states.transactionExit

    def getUser(self):
        return self.user