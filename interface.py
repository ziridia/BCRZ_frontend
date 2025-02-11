

class interface:

    # this should be a transaction name -> transaction manager
    # all transactions should be in lowercase with no padding
    transactions_functions: dict = {
        'login' : LoginManager,
    }

    transaction_manager = None

    def parseInput(input:str):
        """
        This function should parse input as a string, and call the approproate transaction function.
        If the transaction handler throws an error, an appropriate error message should be printed
        If there is no transaction for the given input, return an appropriate error message

        the reply return is expected to be printed for the user to see as the feedback for their command

        Params: input (string)
        Returns: reply (string)
        """

        """
        We can expect all transactions to be exactly 1 word. It should not be case sensitive
        """
        formatted_input = input.lower().strip()
        

        # if the transaction manager is null:
            # create a transaction manager depending on the input. Invalid input should not
            # create a transaction manager, and should instead just return an error message
        # if its not null, pass all formatted input into the transaction manager. Let it handle errors

        if transaction_manager = None:

            if formatted_input not in transaction_manager:
                # the user gave invalid input for its current step
                return "error: unknown command"

            # create transaction manager based on the input
            transaction_manager = transaction_functions[formatted_input]()
        
        # transaction manager is not null, so pass the input directly off to it
        try:
            return_value = transaction_manager.next(formatted_input)

            # check if the transaction is complete, and if so, set the transaction manager to None
            if transaction_manager.isComplete():
                transaction_manager = None

            return return_value
        except:
            return "error: unable to parse transaction"
        
        