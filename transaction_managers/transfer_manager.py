

from transaction_manager import TransactionManager

class states:
    beforeTransfer = 0 # user just typed "withdrawal", display appropriate message
    transactionExit = -1 # flag transaction as finished (error or successful completion)
    awaitAccountName = 1
    awaitAccountNumber = 2
    awaitSecondAccountNumber = 3
    awaitAmount = 4


class TransferManager(TransactionManager):

    def __init__(self, user):
        self.user = user    
        self.state:int = states.beforeTransfer
        self.account_name = None
        self.account_number = None
        self.second_account_number = None
        self.amount = None
        # For testing account balance
        self.accountBalance = 800
        # Logging transfers so they can be printed.
        self.transfers = []

    def next(self, user_input):


            if self.state == states.beforeTransfer:
                self.state = states.awaitAccountName
                return "Enter account name: "
            
            elif self.state == states.awaitAccountName:
                self.state = states.awaitAccountNumber
                self.account_name = user_input
                return "Enter account number: "
            
            elif self.state == states.awaitAccountNumber:
                # Verify if account exists

                # Next Part of the Transfer.
                self.account_number = user_input
                self.state = states.awaitSecondAccountNumber
                return "Enter reciever of transfer account number: "

            elif self.state == states.awaitSecondAccountNumber:
                # Verify if Reciever Account is a vaild code.
                
                # Next part of the Transfer.
                self.second_account_number = user_input.strip().upper()
                self.state = states.awaitAmount
                return "Enter amount for bill payment: "
            
            elif self.state == states.awaitAmount:
                # Check if amount is valid and proceed with the Transfer.
                try:
                    self.amount = float(user_input)

                    if self.amount < 0 or self.amount > 1000:
                        return f"Error: Invalid amount. Must be between 0 and 1000. Inputed: {self.amount}"
                    
                    # Example for exceeding account balance:
                    if self.amount > self.accountBalance:
                        return f"Error: Invalid amount. Exceeds account balance. Inputed: {self.amount}"
                    
                    # Recording Transfer for logs
                    #transfer = f"02_{self.account_name}_{self.account_number}_{self.amount}_{self.second_account_number}"
                    #self.transfer.append(transfer)

                    self.state = states.transactionExit
                    return f"Transfer of {self.amount} to {self.second_account_number} completed."

                except ValueError:
                    return f"Error: Invalid input. Please enter a numeric value and not {self.amount}"
        
            return "error: state machine is not exiting properly"


    def isComplete(self):
        return self.state == states.transactionExit

    def getUser(self):
        return self.user