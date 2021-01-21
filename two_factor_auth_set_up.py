from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from mysql.connector import MySQLConnection, Error
from controllers.DbConnector import DbConnector
from controllers.PasswordManager import PasswordManager
from controllers.TwoFactorAuthentication import TwoFactorAuthentication

two_factor_auth_set_up_page = Blueprint('two_factor_auth_set_up_page', __name__, template_folder='templates')


@two_factor_auth_set_up_page.route('/', methods=['GET', 'POST'])
def two_factor_auth_set_up_page_func():
    try:
        if 'needs_auth' in session:
            return redirect(url_for('login_page.login_page_func'))
        elif 'user_id' in session and 'name' in session:
            return redirect(url_for('account_page.accounts_page'))
        else:
            pass
    except:
        # not already logged in, proceed
        return redirect(url_for('login_page.login_page_func'))

    two_fa_manager = TwoFactorAuthentication()
    user_id = session['user_id']
    otp_key = session['otp_key']
    email = session['email']
    qr_code = two_fa_manager.get_barcode_url(otp_key,email)
    if request.method == "POST":

        users_code = request.form.get("auth-code")  # gets all input from login form
        is_valid = two_fa_manager.verify_users_code(users_code)
        if is_valid:
            return redirect(url_for('account_page.accounts_page'))
        else:
            session.clear()
            return redirect(url_for('error_page.error_page_foo', code="e2"))
    return render_template('two_factor_set_up.html', )