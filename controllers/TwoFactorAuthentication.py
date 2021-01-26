import pyotp

'''
    File name: TwoFactorAuthentication.py
    Author: Jacob Scase
    Credits: Jacob Scase
    Date created: 14/12/2020
    Date last modified: 25/01/2021
    Python Version: 3.7
    Purpose: Class to manage the two factor authentication of a user. Methods to generate a secret key, get the barcode
             url for a user to scan and enter in their authenticator app, and verify a users entered authentiaction code.
'''

class TwoFactorAuthentication:
    def get_random_secret_key(self):
        return pyotp.random_base32()
    def get_barcode_url(self, secret_key,users_email):
        return pyotp.totp.TOTP(secret_key).provisioning_uri(name=users_email, issuer_name='StuBank')
    def verify_users_code(self, users_code, secret_key):
        totp = pyotp.TOTP(secret_key)
        isvalid = totp.verify(users_code)
        return isvalid
