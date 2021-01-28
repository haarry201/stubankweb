import binascii
import hashlib
from flask import Blueprint, render_template, request, session, redirect, url_for
from mysql.connector import Error
from controllers.DbConnector import DbConnector
from controllers.PasswordManager import PasswordManager
from controllers.TwoFactorAuthentication import TwoFactorAuthentication

'''
File name: account_settings_page.py
Author: Jacob Scase
Credits: Jacob Scase
Date created: 25/01/2021
Date last modified: 25/01/2021
Python version: 3.7
Purpose: Back-end file for the user's account settings page, allows the user to change their password or email,
         and allows for the removal of two factor authentication.
'''

account_settings_page = Blueprint('account_settings_page', __name__, template_folder='templates')


@account_settings_page.route('/', methods=['GET', 'POST'])
def account_settings_page_func():
    try:
        if 'user_id' in session:
            if session['needs_auth'] == True:
                return redirect(url_for('login_page.login_page_func'))
            else:
                user_id = session['user_id']
        else:
            return redirect(url_for('login_page.login_page_func'))
    except:
        return redirect(url_for('login_page.login_page_func'))
    if request.method == "POST":
        if 'email_change' in request.form:
            new_email = request.form.get('new_email')
            current_pwd = request.form.get('current_password')
            pwd_manager = PasswordManager()
            db_connector = DbConnector()
            conn = db_connector.getConn()
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT EmailAddress,Password,Salt FROM UserInfo WHERE UserID = (%s)", (user_id,))
            result = cursor.fetchall()
            for row in result:
                #Verify sent password
                db_email = row[0]
                db_pwd = row[1]
                db_salt = row[2]
                is_users_pwd = pwd_manager.check_password(current_pwd,db_pwd,db_salt)
                if is_users_pwd:
                    cursor.execute("SELECT EmailAddress FROM UserInfo WHERE UserID = (%s)", (new_email,))
                    result = cursor.fetchall()
                    email_in_use = False
                    for row in result:
                        if row[0] == new_email:
                            email_in_use = True
                    if not email_in_use:
                        cursor.execute("UPDATE UserInfo SET EmailAddress = (%s) WHERE UserID = (%s)", (new_email,user_id ))
                        conn.commit()
                        cursor.close()
                        conn.close()
                        changed_data = "Email"
                        session['email'] = new_email
                        return render_template('account_settings.html', changed_data=changed_data)
                    else:
                        return redirect(url_for('error_page.error_page_func', code="e9", src="accounts.html"))
                else:
                    return redirect(url_for('error_page.error_page_func', code="e8", src="accounts.html"))

        elif 'pwd_change' in request.form:
            current_pwd = request.form.get('current_password')
            new_pwd = request.form.get('new_password')
            pwd_manager = PasswordManager()
            db_connector = DbConnector()
            conn = db_connector.getConn()
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT Password,Salt FROM UserInfo WHERE UserID = (%s)",(user_id, ))
            result = cursor.fetchall()
            for row in result:
                #Verify sent password
                db_pwd = row[0]
                db_salt = row[1]
                is_users_pwd = pwd_manager.check_password(current_pwd,db_pwd,db_salt)
                if is_users_pwd:
                    new_salt = db_salt.encode('ascii')
                    pwd = hashlib.pbkdf2_hmac('sha512', new_pwd.encode('utf-8'), new_salt, 100000)
                    pwdhash = binascii.hexlify(pwd)  # hash password using salt, this is what is stored in database
                    cursor.execute("UPDATE UserInfo SET Password = (%s) WHERE UserID = (%s)", (pwdhash, user_id))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    changed_data = "Password"
                    return render_template('account_settings.html', changed_data=changed_data)
                else:
                    return redirect(url_for('error_page.error_page_func', code="e8", src="accounts.html"))

        elif 'auth_remove' in request.form:
            print("removing auth")
            auth_code = request.form.get('auth_code')
            users_secret_key = session['secret_auth_key']
            two_fa_manager = TwoFactorAuthentication()
            if two_fa_manager.verify_users_code(auth_code,users_secret_key):
                db_connector = DbConnector()
                conn = db_connector.getConn()
                cursor = conn.cursor(buffered=True)
                cursor.execute("UPDATE UserInfo SET TwoFactorEnabled = (%s) WHERE UserID = (%s)", (0, user_id))
                conn.commit()
                cursor.close()
                conn.close()
                session['two_factor_enabled'] = False
                return render_template('account_settings.html', changed_data="")
            else:
                return redirect(url_for('error_page.error_page_func', code="e8", src="accounts.html"))

    try:
        db_connector = DbConnector()
        conn = db_connector.getConn()
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM UserInfo WHERE UserID = (%s)",(user_id,))
    except Error as error:
        print(error)
        return redirect(url_for('error_page.error_page_func', code="e2", src="accounts.html"))

    return render_template('account_settings.html',changed_data="")