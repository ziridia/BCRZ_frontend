
"""
This file will contain any constants that are referenced throughout the program.

For example: the maximum balance, transfer cap, withdrawal cap.

All constants / magic numbers should be put here instead of elsewhere in the code
"""
ACCOUNT_NUMBER_LENGTH = 5
MAX_ACCOUNT_NAME_LENGTH = 20
MAX_ACCOUNT_NUMBER = 99999
MAX_BALANCE = 999_999_99
TRANSFER_CAP = 1_000_00
WITHDRAWAL_CAP = 500_00

MISC_FIELD_LENGTH = 2

TRANSFER_OUT_MSG:str = "EX"
TRANSFER_IN_MSG:str = "IN"

CURRENT_BANK_ACCOUNTS:str = "CurrentBankAccounts"
DAILY_TRANSACTION_LOG:str = "dailyTransactionLog.txt"

TRANSACTION_LOG_LENGTH:int = 41