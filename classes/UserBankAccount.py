'''
File name: UserBankAccount.py
Author: Jacob Scase
Credits: Jacob Scase
Date created: 26/01/2021
Date last modified: 26/01/2021
Python version: 3.7
Purpose: Card Class for storing information about users bank accounts.
'''

class UserBankAccount:
    def __init__(self, account_num, sort_code, current_balance, agreed_overdraft, account_type, account_type_id):
        self.account_num = account_num
        self.sort_code = sort_code
        self.current_balance = current_balance
        self.agreed_overdraft = agreed_overdraft
        self.account_type = account_type
        self.account_type_id = account_type_id