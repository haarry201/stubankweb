import pyotp

class TwoFactorAuthentication:
    def get_random_secret_key(self):
        return pyotp.random_base32()
    def get_barcode_url(self, secret_key,users_email):
        return pyotp.totp.TOTP(secret_key).provisioning_uri(name=users_email, issuer_name='StuBank')
    def verify_users_code(self, users_code, secret_key):
        totp = pyotp.TOTP(secret_key)
        isvalid = totp.verify(users_code)
        return isvalid
