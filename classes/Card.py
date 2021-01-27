'''
File name: Card.py
Author: Harry Kenny
Credits: Harry Kenny
Date created: 23/01/2021
Date last modified: 23/01/2021
Python version: 3.7
Purpose: Card Class for storing information about users cards.
'''

class Card:
    def __init__(self, card_number, card_type_id, start_date, expiry_date, pin_number):
        self.card_number = card_number
        self.card_type_id = card_type_id
        self.start_date = start_date
        self.expiry_date = expiry_date
        self.pin_number = pin_number