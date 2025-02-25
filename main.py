
import sys

from interface import Interface
from helpers.read_in_accounts import readInAccounts
from helpers.debug_tools import debugPrint

from helpers.constants import CURRENT_BANK_ACCOUNTS, DAILY_TRANSACTION_LOG

"""
This is a CLI banking program, that handles various transactions including withdrawals, deposits, and transfers. 

Input is taken from the user, as well as the CurrentBankAccounts file, which contains any current bank accounts.

All transactions are written to a daily transaction log `dailyTransactionLog.txt`

The program can be run using python. No dependencies should need to be installed. 
All commands are to be one word. Additional steps of a command will be inputted on a separate line
"""

def main():
    global CURRENT_BANK_ACCOUNTS
    global DAILY_TRANSACTION_LOG
    """
    This should handle looping asking for user input, and pass the raw input to the user, and 
    print any output given by the interface class
    """
    print("Welcome to Banking System\n\ntype `login` to continue")
    
    debugPrint(f"command line args {sys.argv}")
    # update global paths to files
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            
            if arg.startswith("accounts="):
                CURRENT_BANK_ACCOUNTS = arg[9:]
                debugPrint(f"Updated current bank accounts path to {CURRENT_BANK_ACCOUNTS}")
                continue

            elif arg.startswith("log="):
                DAILY_TRANSACTION_LOG = arg[4:]
                debugPrint(f"Updated daily transaction log path to {DAILY_TRANSACTION_LOG}")
                continue

            else:
                print(f"unknown parameter {arg}. Parameters must start with `accounts=` or `log=`")
                return

    output:str = ""
    while output != "exit":

        try:
            inputText = input()
        
        except:
            return

        print(Interface.parseInput(inputText))

if __name__ == "__main__":
    main()