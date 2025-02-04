

class interface:

    # this should be a transaction name -> function dict
    transactions_functions: dict = dict()

    def parseInput(input:str):
        """
        This function should parse input as a string, and call the approproate transaction function.
        If the transaction handler throws an error, an appropriate error message should be printed
        If there is no transaction for the given input, return an appropriate error message

        the reply return is expected to be printed for the user to see as the feedback for their command

        Params: input (string)
        Returns: reply (string)
        """

