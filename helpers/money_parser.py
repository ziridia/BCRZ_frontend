

class MoneyParser:

    def stringToInt(string:str):
        """
        This function should always be used to convert a string to the integer representation of money.

        __Never__ parse manually
        """

        string = string.strip(" $").replace(",", "")

        return int(float(string)*100)
    