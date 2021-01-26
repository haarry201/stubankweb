import binascii
import hashlib

'''
    File name: PasswordManager.py
    Author: Jacob Scase
    Credits: Jacob Scase, Rhys Minchin
    Date created: 11/12/2020
    Date last modified: 25/01/2021
    Python Version: 3.7
    Purpose: Class with method to check the password entered against the stored password, salting and rehashing the
             password entered to check if it matches the password stored. 
'''

class PasswordManager:
    def check_password(self, password_to_check, stored_pwd, stored_salt):
        pwd_hash = hashlib.pbkdf2_hmac('sha512', password_to_check.encode('utf-8'), stored_salt.encode('ascii'), 100000)
        pwd_hash_decoded = binascii.hexlify(pwd_hash).decode('ascii')
        return pwd_hash_decoded == stored_pwd # returns true if generated hash matches stored hash