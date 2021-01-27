from flask import Blueprint, render_template, request, session, redirect, url_for
from controllers.TwoFactorAuthentication import TwoFactorAuthentication

'''
File name: two_factor_auth_verify_page.py
Author: Jacob Scase
Credits: Jacob Scase, Harry Kenny
Date created: 14/12/2020
Date last modified: 25/01/2021
Python version: 3.7
Purpose: Back-end file for allowing the server to verify the users 
'''

two_factor_auth_verify_page = Blueprint('two_factor_auth_verify_page', __name__, template_folder='templates')


@two_factor_auth_verify_page.route('/', methods=['GET', 'POST'])
def two_factor_auth_verify_page_func():
    try:
        if 'needs_auth' in session:
            secret_key = session['secret_auth_key']
            pass
        elif 'user_id' in session and 'name' in session:
            return redirect(url_for('account_page.account_page_func'))
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
            if session['user_role'] == 'Admin':
                return redirect(url_for('admin_home_page.admin_home_page_func'))
            else:
                return redirect(url_for('account_page.account_page_func'))
        else:
            session.clear()
            return redirect(url_for('error_page.error_page_func', code="e12"))
    return render_template('two_factor_verification.html')