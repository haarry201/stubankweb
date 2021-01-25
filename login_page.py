from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from mysql.connector import MySQLConnection, Error
from controllers.DbConnector import DbConnector
from controllers.PasswordManager import PasswordManager

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
            cursor.execute("SELECT * FROM UserInfo WHERE EmailAddress = (%s)", (email,))
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
                        is_two_factor_enabled = row[4]
                        if is_two_factor_enabled:
                            session['needs_auth'] = True
                            session['two_factor_enabled'] = True
                            session['user_id'] = row[0]
                            session['email'] = email
                            session['secret_auth_key'] = row[4]
                            session['name'] = row[5]
                            session['user_role'] = row[12]
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
                                return redirect(url_for('account_page.accounts_page'))
        except Error as error:
            return redirect(url_for('error_page.error_page_foo', code="e1"))
        finally:
            cursor.close()
            conn.close()
            # closes connection
        return redirect(url_for('error_page.error_page_foo', code="e1"))
    return render_template('login.html')