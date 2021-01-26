from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from mysql.connector import MySQLConnection, Error
from controllers.DbConnector import DbConnector
from controllers.PasswordManager import PasswordManager

'''
File name: login_page.py
Author: Rhys Minchin
Credits: Rhys Minchin
Date created: 08/12/2020
Date last modified: 25/01/2021
Python version: 3.7
Purpose: This provides the back-end for the login page. It gets the information from the login form and processes it
         in order to determine what happens next. If there is a login error, the user is forwarded to the error page
         and an appropriate error message is given. If not, the user is forwarded to their relevant homepage depending
         on their role (if two factor authentication enabled) or to the two factor authentication page if not.
'''

login_page = Blueprint('login_page', __name__, template_folder='templates')


@login_page.route('/', methods=['GET', 'POST'])
def login_page_func():
    try:
        if 'user_id' in session and 'name' in session:
            if session['needs_auth'] == True:
                # 2fa but not authenticated yet
                session.clear()
                pass
            else:
                return redirect(url_for('account_page.accounts_page'))
        else:
            pass

    except:
        # not already logged in, proceed
        pass

    if request.method == "POST":
        pwd_manager = PasswordManager()
        email = request.form.get("email")
        password_to_check = request.form.get("password")
        security_question = request.form.get("security_question")
        security_answer = request.form.get("security_answer")  # gets all input from login form
        try:
            db_connector = DbConnector()
            conn = db_connector.getConn()
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM UserInfo WHERE EmailAddress = (%s)", (email,))  # SQL query to find input email in database
            result = cursor.fetchall()
            for row in result:
                # Verify sent password
                db_pwd = row[2]
                db_salt = row[3]
                db_sq_question = row[10]
                db_sq_answer = row[11]
                is_users_pwd = pwd_manager.check_password(password_to_check, db_pwd, db_salt)
                if is_users_pwd:
                    if security_question == db_sq_question and security_answer.lower() == db_sq_answer.lower():
                        is_two_factor_enabled = row[13]
                        print(is_two_factor_enabled)
                        if is_two_factor_enabled:
                            session['needs_auth'] = True
                            session['two_factor_enabled'] = True
                            session['user_id'] = row[0]
                            session['email'] = email
                            session['secret_auth_key'] = row[4]
                            session['name'] = row[5]
                            session['user_role'] = row[12]
                            #  2FA checking and validation
                            return redirect(url_for('two_factor_auth_verify_page.two_factor_auth_verify_page_func'))
                        else:
                            session['needs_auth'] = False
                            session['two_factor_enabled'] = False
                            session['user_id'] = row[0]
                            session['email'] = email
                            session['secret_auth_key'] = row[4]
                            session['name'] = row[5]
                            user_role = row[12]
                            session['user_role'] = user_role
                            if user_role == 'Admin':
                                return redirect(url_for('admin_home_page.admin_home_page_func'))
                            else:
                                return redirect(url_for('account_page.accounts_page'))  # redirects user based on role
        except Error as error:
            return redirect(url_for('error_page.error_page_func', code="e1"))  # if error, user taken to error page
        finally:
            cursor.close()
            conn.close()
            # closes connection
        return redirect(url_for('error_page.error_page_func', code="e1"))  # if error, user taken to error page
    return render_template('login.html')