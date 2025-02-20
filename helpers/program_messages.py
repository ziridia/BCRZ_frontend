
"""
All messages should be written in this file, to ensure consistency between messages in the program

This includes error messages (e.g. "error: insufficient funds")
and it includes success messages (e.g. "enter account name")

This could theoretically be modified fairly trivially to support
language localization, should the spec change to require it
"""

class ErrorMessages:

    not_logged_in:str = "error: not logged in"
    user_not_found:str = "error: user does not exist"
    account_not_found:str = "error: account does not exist"
    invalid_account_number:str = "error: invalid account number"

    invalid_amount:str = "error: invalid amount"
    insufficient_funds:str = "error: insufficient funds"

    amount_must_be_positive:str = "error: amount must be positive"

    failed_to_log_transaction:str = "error: unable to log transaction"
    failed_to_revert_transaction:str = "error: unable to revert transaction - mismatch between log and state"

    state_machine_failure:str = "error: state machine is not exiting properly"

    # Withdrawal specific
    daily_withdrawal_cap:str = "error: cannot exceed daily withdrawal cap of $500.00"



class SuccessMessages:

    enter_account_name:str = "enter account name"
    enter_account_number:str = "enter account number"

    transaction_success:str = "transaction successful"

    # Withdrawal specific. Decision needed on if this should be included here
    enter_amount_to_withdraw:str = "enter amount to withdraw"
    withdrawal_success:str = "withdrawal successful"