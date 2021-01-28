'''
    File name: CardInfo.py
    Author: Jacob Scase
    Credits: Jacob Scase, Harry Kenny
    Date created: 14/12/2020
    Date last modified: 25/01/2021
    Python Version: 3.7
    Purpose: Class to store the information about credit cards that stubank offer.
'''

class CardInfo:
    def __init__(self, type_id, desc):
        self.desc = desc
        self.type_id = type_id