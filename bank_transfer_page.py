from flask import Flask, Blueprint, render_template, request
from controllers.DbConnector import DbConnector
from random import *
from mysql.connector import MySQLConnection, Error

bank_transfer_page = Blueprint('bank_transfer_page', __name__, template_folder='templates')


@bank_transfer_page.route('/', methods=['GET', 'POST'])
def bank_transfer():
    if request.method == 'POST':
        email = request.form.get("email")
        account_type = request.form.get("account_type")
        if account_type == "student current account":
            account_type_id = '123'
        if account_type == "savings account":
            account_type_id = '100'
        account_num = request.form.get("account_number")
        sort_code = request.form.get("sort_code")
        transfer_value = int(request.form.get("transfer_value"))

        try:
            db_connector = DbConnector()
            conn = db_connector.getConn()
            db_connector.closeConn(conn)
            cursor = conn.cursor(buffered=True)

            cursor.execute("SELECT * FROM UserInfo")
            row = cursor.fetchone()
            while row is not None:
                if row[1] == email:
                    user_id = row[0]
                    break
                else:
                    row = cursor.fetchone()

            cursor.execute("SELECT * FROM UserAccounts")
            row = cursor.fetchone()

            while row is not None:
                if row[2] == user_id and row[3] == account_type_id:
                    current_value = int(row[5])
                    new_value = current_value - transfer_value
                    cursor.execute("UPDATE UserAccounts SET CurrentBalance = (%s) WHERE UserID = (%s) AND"
                                   " AccountTypeID = (%s)", (new_value, user_id, account_type_id))
                    break

                else:
                    row = cursor.fetchone()

            cursor.execute("SELECT * FROM UserAccounts")
            row = cursor.fetchone()

            while row is not None:
                if row[0] == account_num and row[1] == sort_code:
                    transferee_value_current = int(row[5])
                    new_transferee_value = transferee_value_current + transfer_value
                    cursor.execute("UPDATE UserAccounts SET CurrentBalance = (%s) WHERE"
                                   " AccountNum = (%s) AND SortCode = (%s)",
                                   (new_transferee_value, account_num, sort_code))
                    break

                else:
                    row = cursor.fetchone()

            conn.commit()
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
            return render_template("error.html", msg="An unexpected error occurred, please try again",
                                   src="register.html")

        return render_template('index.html')

    return render_template('bank_transfer.html')
