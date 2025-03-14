from transaction_manager                        import TransactionManager
from transaction_managers.login_manager         import LoginManager
from transaction_managers.withdrawal_manager    import WithdrawalManager
from transaction_managers.transfer_manager      import TransferManager
from transaction_managers.paybill_manager       import PaybillManager
from transaction_managers.deposit_manager       import DepositManager
from transaction_managers.create_manager        import CreateManager
from transaction_managers.delete_manager        import DeleteManager
from transaction_managers.disable_manager       import DisableManager
from transaction_managers.changeplan_manager    import ChangeplanManager
from transaction_managers.logout_manager        import LogoutManager

from user import User

from helpers.debug_tools import debugPrint
from helpers.program_messages import ErrorMessages

class Interface:

    # this should be a transaction name -> transaction manager
    # all transactions should be in lowercase with no padding

    transactions_functions: dict = {
        'login'     : LoginManager,
        'withdrawal': WithdrawalManager,
        'transfer'  : TransferManager,
        'paybill'   : PaybillManager,
        'deposit'   : DepositManager,
        'create'    : CreateManager,
        'delete'    : DeleteManager,
        'disable'   : DisableManager,
        'changeplan': ChangeplanManager,
        'logout'    : LogoutManager,
    }
    
    transaction_manager = None

    user = None

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

        if formatted_input == "":
            Interface.user = Interface.transaction_manager.getUser()
            Interface.transaction_manager = None
            return ErrorMessages.no_input
        
        # if the transaction manager is null:
            # create a transaction manager depending on the input. Invalid input should not
            # create a transaction manager, and should instead just return an error message
        # if its not null, pass all formatted input into the transaction manager. Let it handle errors

        if Interface.transaction_manager == None:
            
            if formatted_input not in Interface.transactions_functions:
                # the user gave invalid input for its current step
                return "error: unknown command"

            # create transaction manager based on the input
            Interface.transaction_manager = Interface.transactions_functions[formatted_input](Interface.user)
        
        # transaction manager is not null, so pass the input directly off to it
        try:
            return_value = Interface.transaction_manager.next(formatted_input)

            # check if the transaction is complete, and if so, set the transaction manager to None
            if Interface.transaction_manager.isComplete():
                Interface.user = Interface.transaction_manager.getUser()
                # print("user balance after transaction is", Interface.user.accounts[0].balance)
                Interface.transaction_manager = None
                

            return return_value
        except Exception as e:
            debugPrint(e)
            return "error: unable to parse transaction"
        
        