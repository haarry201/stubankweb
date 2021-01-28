'''
File name: StoryTransasction.py
Author: Jacob Scase
Credits: Jacob Scase
Date created: 23/01/2021
Date last modified: 23/01/2021
Python version: 3.7
Purpose: StoryTransaction Class for storing information about Transactions for use in the stories feature.
'''

class StoryTransaction:
    def __init__(self, date, recipient, amount, time):
        self.date = date
        self.recipient = recipient
        self.amount = amount
        self.time = time