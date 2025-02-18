
from interface import interface


def main():
    """
    This should handle looping asking for user input, and pass the raw input to the user, and 
    print any output given by the interface class
    """

    output:str = ""
    while output != "exit":
        inputText = input()
        print(interface.parseInput(inputText))

if __name__ == "__main__":
    main()