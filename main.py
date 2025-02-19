
from interface import interface


def main():
    """
    This should handle looping asking for user input, and pass the raw input to the user, and 
    print any output given by the interface class
    """
    print("Welcome to Banking System\n\nWhat would you like to do today?")
    print("Options: login, withdrawal, transfer, paybill, deopsit, create, delete, disable, changeplan")
    output:str = ""
    while output != "exit":
        inputText = input()
        print(interface.parseInput(inputText))

if __name__ == "__main__":
    main()