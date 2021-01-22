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
        # not already logged in, procede
        pass

    if request.method == "POST":
        pwd_manager = PasswordManager()
        email = request.form.get("email")
        password = request.form.get("password")
        security_question = request.form.get("security_question")
        security_answer = request.form.get("security_answer")  # gets all input from login form
        try:
            db_connector = DbConnector()
            conn = db_connector.getConn()
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM UserInfo")  # gets all data stored in UserInfo table

            row = cursor.fetchone()  # fetches first row of table

            while row is not None:
                if email == row[1] and (pwd_manager.check_password(password, row) and security_question == row[10] and
                                        security_answer.lower() == row[11].lower()):
                    # checks input data against stored data
                    two_factor_is_enabled = row[13]
                    if two_factor_is_enabled:
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
                        session['user_role'] = row[12]
                        return redirect(url_for('account_page.accounts_page'))
                    #return render_template("accounts.html", user=session['name'])

                else:
                    row = cursor.fetchone()
                    # if doesn't match, fetches next row stored in table

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()
            # closes connection
        return redirect(url_for('error_page.error_page_foo', code="e1"))
    return render_template('login.html')