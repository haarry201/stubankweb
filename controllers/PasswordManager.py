import binascii
import hashlib


class PasswordManager:
    def check_password(self, password_to_check, stored_pwd, stored_salt):
        pwd_hash = hashlib.pbkdf2_hmac('sha512', password_to_check.encode('utf-8'), stored_salt.encode('ascii'), 100000)
        pwd_hash_decoded = binascii.hexlify(pwd_hash).decode('ascii')
        return pwd_hash_decoded == stored_pwd # returns true if generated hash matches stored hash