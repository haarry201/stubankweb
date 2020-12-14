from flask import Flask, Blueprint, render_template, request, session
from mysql.connector import MySQLConnection, Error
from controllers.DbConnector import DbConnector
from controllers.PasswordManager import PasswordManager

login_page = Blueprint('cards_page', __name__, template_folder='templates')


@login_page.route('/', methods=['GET', 'POST'])
def login_page_func():
    user_id = session["user_id"]
    db_connector = DbConnector()
    conn = db_connector.getConn()
    cursor = conn.cursor()
    query = ("SELECT * FROM UserCards WHERE UserID = %s")
    cursor.execute(query(user_id))
    if request.method == "POST":
        pwd_manager = PasswordManager()
        email = request.form.get("email")
        password = request.form.get("password")
        security_question = request.form.get("security_question")
        security_answer = request.form.get("security_answer")  # gets all input from login form
        try:
            db_connector = DbConnector()
            conn = db_connector.getConn()
            db_connector.closeConn(conn)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM UserInfo")  # gets all data stored in UserInfo table

            row = cursor.fetchone()  # fetches first row of table

            while row is not None:
                if email == row[1] and (pwd_manager.check_password(password, row) and security_question == row[10] and
                                        security_answer.lower() == row[11].lower()):
                    # checks input data against stored data
                    return render_template("accounts.html", user=row[5])
                else:
                    row = cursor.fetchone()
                    # if doesn't match, fetches next row stored in table

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()
            # closes connection

        return render_template("error.html", msg="These login credentials do not match an existing user, please try "
                                                 "again", src="login.html")
    return render_template('cards.html.html', user_cards = users_cards)