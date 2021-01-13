from flask import Flask, Blueprint, render_template,request
from controllers.DbConnector import DbConnector
from random import *
from mysql.connector import MySQLConnection, Error

bank_acc_application_page = Blueprint('bank_acc_application_page', __name__, template_folder='templates')


@bank_acc_application_page.route('/', methods=['GET', 'POST'])
def bank_application():
    if request.method == 'POST':
        account_type = request.form.get("account type")
        if account_type == "student current account":
            account_type_id = '123'
            agreed_overdraft = 1500
        elif account_type == "savings account":
            account_type_id = '100'
            agreed_overdraft = 0
        else:
            return render_template("error.html", msg="An unexpected error occurred, please try again",
                                   src="register.html")
        email = request.form.get("email")
        account_num = ''.join(["{}".format(randint(0, 9)) for num in range(0, 8)])
        sort_code = ''.join(["{}".format(randint(0, 9)) for num in range(0, 6)])

        current_balance = 0


        try:
            db_connector = DbConnector()
            conn = db_connector.getConn()
            db_connector.closeConn(conn)
            cursor = conn.cursor(buffered=True)

            cursor.execute ("SELECT * FROM UserInfo")
            row = cursor.fetchone()
            while row is not None:
                if row[1] == email:
                        user_id = row[0]
                        break
                else:
                    row = cursor.fetchone()


            cursor.execute("INSERT INTO Accounts VALUES (%s, %s)", (account_num, sort_code))

            cursor.execute("INSERT INTO UserAccounts VALUES (%s, %s, %s, %s, %s, %s)", (account_num, sort_code,\
                            user_id, account_type_id, agreed_overdraft, current_balance))



            conn.commit()
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
            return render_template("error.html", msg="An unexpected error occurred, please try again",
                                   src="register.html")

        return render_template('index.html')

    return render_template('bank_application.html')
