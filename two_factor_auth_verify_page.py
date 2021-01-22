from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from mysql.connector import MySQLConnection, Error
from controllers.DbConnector import DbConnector
from controllers.PasswordManager import PasswordManager
from controllers.TwoFactorAuthentication import TwoFactorAuthentication

two_factor_auth_verify_page = Blueprint('two_factor_auth_verify_page', __name__, template_folder='templates')


@two_factor_auth_verify_page.route('/', methods=['GET', 'POST'])
def two_factor_auth_verify_page_func():
    try:
        if 'needs_auth' in session:
            secret_key = session['secret_auth_key']
            pass
        elif 'user_id' in session and 'name' in session:
            return redirect(url_for('account_page.accounts_page'))
        else:
            return redirect(url_for('login_page.login_page_func'))
    except:
        # not already logged in, proceed
        return redirect(url_for('login_page.login_page_func'))

    if request.method == "POST":
        two_fa_manager = TwoFactorAuthentication()
        users_code = request.form.get("auth-code")  # gets all input from login form
        is_valid = two_fa_manager.verify_users_code(users_code, secret_key)
        if is_valid:
            session['needs_auth'] = False
            return redirect(url_for('account_page.accounts_page'))
        else:
            session.clear()
            return redirect(url_for('error_page.error_page_foo', code="e2"))
    return render_template('two_factor_verification.html')