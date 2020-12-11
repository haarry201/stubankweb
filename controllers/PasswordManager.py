import binascii
import hashlib


class PasswordManager:
    def check_password(password, data):
        pwd = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), data[3].encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwd).decode('ascii')
        return pwdhash == data[2]  # returns true if generated hash matches stored hash