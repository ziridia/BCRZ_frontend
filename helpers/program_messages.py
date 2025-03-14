
"""
All messages should be written in this file, to ensure consistency between messages in the program

This includes error messages (e.g. "error: insufficient funds")
and it includes success messages (e.g. "enter account name")

This could theoretically be modified fairly trivially to support
language localization, should the spec change to require it
"""

class ErrorMessages:

    not_logged_in:str = "error: not logged in"
    user_not_found:str = "error: account holder does not exist"
    account_not_found:str = "error: account does not exist"
    invalid_account_number:str = "error: invalid account number"

    invalid_amount:str = "error: invalid amount"
    insufficient_funds:str = "error: insufficient funds"

    insufficient_permissions:str = "error: insufficient permissions"

    amount_must_be_positive:str = "error: amount must be positive"

    failed_to_log_transaction:str = "error: unable to log transaction"
    failed_to_revert_transaction:str = "error: unable to revert transaction - mismatch between log and state"

    state_machine_failure:str = "error: state machine is not exiting properly"

    name_too_long:str = "error: account name must be between 1 and 20 characters long"

    exceed_max_balance:str = "error: cannot exceed max balance of $999,999.99"

    account_disabled:str = "error: account is disabled"

    amount_cannot_be_negative:str = "error: amount cannot be negative"

    # input parser
    no_input:str = "error: no input provided"

    # Withdrawal specific
    daily_withdrawal_cap:str = "error: cannot withdraw more than $500.00 per session"

    # transfer specific
    daily_transfer_cap:str = "error: cannot transfer more than $1000 per session"
    cannot_transfer_to_yourself:str = "error: cannot transfer to the same account as is being transferred from"

    # changeplan specific
    already_non_student:str = "error: account plan is already not a student plan"

    # login specific
    invalid_session_type:str = "error: invalid session type"
    already_logged_in:str = "error: already logged in"

    # paybill specific
    invalid_receiver_code:str = "error: invalid receiver code"
    bill_payment_too_high:str = "error: max bill payment per session is $2000"

    # create specific
    account_already_exists:str = "error: account already exists"
    must_be_alpha:str = "error: name must be alphabetic"

    # deposit specific (sort of)
    cannot_access_deposited_funds:str = "error: funds deposited in current session cannot be accessed"
    


class SuccessMessages:

    enter_account_name:str = "enter account name"
    enter_account_number:str = "enter account number"

    transaction_success:str = "transaction successful"

    enter_amount:str = "enter amount"

    # Withdrawal specific. Decision needed on if this should be included here
    enter_amount_to_withdraw:str = "enter amount to withdraw"
    withdrawal_success:str = "withdrawal successful"

    # Transfer specific
    enter_transfer_to_account_name:str = "enter account name to transfer to"
    transfer_success:str ="transfer successful"
    
    # logout specific
    logged_out:str = "logged out"

    # login specific
    logged_in:str = "login successful"
    select_session_type:str = "select desired session type (admin, standard)"
    

    # create specific
    enter_starting_balance:str = "enter starting balance"
    account_created:str = "account created"
    
    # delete specific
    account_deleted:str = "account deleted"

    # disable specific
    account_disabled:str = "account disabled"

    # deposit specific
    deposit_success:str = "deposit successful"

    # paybill specific
    enter_receiver_code:str = "enter receiver code"
    bill_paid:str = "bill paid"

    # changeplan specific
    changed_plan:str = "Account payment plan successfully changed from student to non-student."