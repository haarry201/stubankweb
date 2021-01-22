from flask import Flask, Blueprint, render_template, request, redirect, url_for, session

from controllers import Transaction
from controllers.DbConnector import DbConnector
from mysql.connector import MySQLConnection, Error
from datetime import datetime
import random

from controllers.Transaction import MLTransaction

bank_transfer_page = Blueprint('bank_transfer_page', __name__, template_folder='templates')


@bank_transfer_page.route('/', methods=['GET', 'POST'])
def bank_transfer():
    try:
        if 'user_id' in session:
            if session['needs_auth'] == True:
                return redirect(url_for('login_page.login_page_func'))
            else:
                pass
        else:
            return redirect(url_for('login_page.login_page_func'))
    except:
        return redirect(url_for('login_page.login_page_func'))
    if request.method == 'POST':
        email = request.form.get("email")
        account_type = request.form.get("account_type")
        if account_type == "student current account":
            account_type_id = '123'
        if account_type == "savings account":
            account_type_id = '100'
        account_num = request.form.get("account_number")
        sort_code = request.form.get("sort_code")
        transfer_value = request.form.get("transfer_value")
        transfer_value = int(float(transfer_value) * 100)

        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-")
        date = now.strftime("%Y-%m-%d")
        hours = now.strftime("%H")
        minutes = now.strftime("%M")

        time = (int(hours) * 60) + int(minutes)

        longitude = 0.000
        latitude = 0.000

        try:
            db_connector = DbConnector()
            conn = db_connector.getConn()
            db_connector.closeConn(conn)
            cursor = conn.cursor(buffered=True)

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
                    receiver_user_id = row[2]
                    transferee_value_current = int(row[5])
                    new_transferee_value = transferee_value_current + transfer_value
                    cursor.execute("UPDATE UserAccounts SET CurrentBalance = (%s) WHERE"
                                   " AccountNum = (%s) AND SortCode = (%s)",
                                   (new_transferee_value, account_num, sort_code))
                    break

                else:
                    row = cursor.fetchone()




            cursor.execute("SELECT * FROM UserAccounts")
            row = cursor.fetchone()

            while row is not None:
                if row[2] == user_id:
                    transferer_account_num = row[0]
                    transferer_sort_code = row[1]
                    break

                else:
                    row = cursor.fetchone()

            cursor.execute("SELECT * FROM UserInfo")
            row = cursor.fetchone()

            while row is not None:
                if row[0] == receiver_user_id:
                    receiver_name = row[5] + row[6]
                    break

                else:
                    row = cursor.fetchone()

            ran = random.randrange(10 ** 80)
            myhex = "%016x" % ran
            myhex = myhex[:16]

            transaction_id = dt_string + myhex

            balance_change = transfer_value - transfer_value - transfer_value

            transaction_type = "direct transfer"

            card_num_sending = 0000000000000000

            # Determining whether transaction can go ahead by machine learning
            t_list = Transaction.fetch_transactions(transferer_account_num)
            new_transaction = MLTransaction(receiver_name, transfer_value, latitude, longitude, time)
            if len(t_list) < 5:
                print("not enough prior transactions")
            else:
                p_fraud = new_transaction.analyse_transaction(t_list)
                print("Probabiliy of fraud =", p_fraud)
                if p_fraud > 1:
                    return redirect(url_for('error_page.error_page_foo', code="e7", src="card_payment.html"))

            cursor.execute("INSERT INTO Transactions VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (transaction_id, transferer_account_num, account_num, transferer_sort_code, sort_code,
                            balance_change, date, time, transaction_type, card_num_sending, receiver_name,
                            longitude, latitude))


            conn.commit()
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
            return redirect(url_for('error_page.error_page_foo', code="e2", src="accounts.html"))

        return render_template('index.html')

    return render_template('bank_transfer.html')
