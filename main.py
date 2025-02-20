
from interface import Interface
from helpers.read_in_accounts import readInAccounts

"""
This is a CLI banking program, that handles various transactions including withdrawals, deposits, and transfers. 

Input is taken from the user, as well as the CurrentBankAccounts file, which contains any current bank accounts.

All transactions are written to a daily transaction log `dailyTransactionLog.txt`

The program can be run using python. No dependencies should need to be installed. 
All commands are to be one word. Additional steps of a command will be inputted on a separate line
"""

def main():
    """
    This should handle looping asking for user input, and pass the raw input to the user, and 
    print any output given by the interface class
    """
    print("Welcome to Banking System\n\ntype `login` to continue")
    
    output:str = ""
    while output != "exit":
        inputText = input()
        print(Interface.parseInput(inputText))

if __name__ == "__main__":
    main()