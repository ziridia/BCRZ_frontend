
from helpers.constants import MutableGlobals, MAX_ACCOUNT_NAME_LENGTH, MAX_ACCOUNT_NUMBER, MAX_BALANCE, MISC_FIELD_LENGTH, TRANSACTION_LOG_LENGTH

class TransactionLogger:


    class codes:

        withdrawal  = 1
        transfer    = 2
        paybill     = 3
        deposit     = 4
        create      = 5
        delete      = 6
        disable     = 7
        changeplan  = 8
        logout      = 0

    def wipeTransactions():
        """
        Clear the daily transactions file. Should be run once on program start and
        should never be run again afterwards
        """

        transaction_file = open(MutableGlobals.DAILY_TRANSACTION_LOG, "w")
        transaction_file.close()

    def writeTransaction(transaction_code:int, account_name:str, account_number:int, amount:int, misc:str = "  "):
        """
        Writes the input as a new line to the daily transaction log.
        Throws an error in case of erroneous input, or if the line cannot be written
        """

        transaction:str = ""
        # Verify the transaction code is no more than 2 digits long, then convert to str adn add to transaction
        if transaction_code < 0 or transaction_code > 99:
            raise ValueError("transaction code must be between 0 and 99 inclusive")
        
        transaction = f"{transaction_code:02d}"

        # Verify the account name is not empty, and is at most 20 characters long
        if len(account_name) <= 0 or len(account_name) > MAX_ACCOUNT_NAME_LENGTH:
            raise ValueError("account name must be between 1 and 20 characters long inclusive") 

        # add padding to the right side of the string to make it 20 characters long
        transaction += f" {account_name.ljust(MAX_ACCOUNT_NAME_LENGTH)}"

        # verify account number is non-negative and <= 99999
        if account_number < 0 or account_number > MAX_ACCOUNT_NUMBER:
            raise ValueError("account number must be between 0 and 99999 (inclusive)")

        transaction += f" {account_number:05d}"

        # verify the amount is between 0 and 999,999.99
        if amount < 0 or amount > MAX_BALANCE:
            raise ValueError("amount must be between 0 and 999,999.99")

        transaction += f" {amount:08d}"

        # verify that the misc field is either empty or exactly 2 characters long
        if len(misc) != 0 and len(misc) != MISC_FIELD_LENGTH:
            raise ValueError("misc field must be empty or 2 characters long")

        misc = misc.rjust(MISC_FIELD_LENGTH)

        transaction += f" {misc}"

        # check that the length is correct
        if len(transaction) != TRANSACTION_LOG_LENGTH:
            raise Exception(f"transaction log length is not {TRANSACTION_LOG_LENGTH}. Something went wrong")

        # append the transaction to file
        transaction_file = open(MutableGlobals.DAILY_TRANSACTION_LOG, "a")

        transaction_file.write(transaction + "\n")
        
        transaction_file.close()