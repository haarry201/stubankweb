from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from controllers.DbConnector import DbConnector
from mysql.connector import MySQLConnection, Error
from datetime import datetime
import random
from controllers.Transaction import MLTransaction
import controllers.Transaction as Transaction

'''
File name: card_payment_page.py
Author: Jacob Scase
Credits: Jacob Scase
Date created: 19/01/2021
Date last modified: 25/01/2021
Python version: 3.7
Purpose: Back-end file for allowing the user to simulate a card payment
'''

card_payment_page = Blueprint('card_payment_page', __name__, template_folder='templates')


@card_payment_page.route('/', methods=['GET', 'POST'])
def card_payment():
    try:
        if 'user_id' in session:
            if session['needs_auth'] == True:
                return redirect(url_for('login_page.login_page_func'))
            else:
                user_id = session['user_id']
                pass
        else:
            return redirect(url_for('login_page.login_page_func'))
    except:
        return redirect(url_for('login_page.login_page_func'))
    if request.method == 'POST':
        receiver_name = request.form.get("receiver_name")
        account_type = request.form.get("account_type")
        if account_type == "student current account":
            account_type_id = '123'
        if account_type == "savings account":
            account_type_id = '100'
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        transfer_value = request.form.get("transfer_value")
        transfer_value = int(float(transfer_value) * 100)

        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-")
        date = now.strftime("%Y-%m-%d")
        hours = now.strftime("%H")
        minutes = now.strftime("%M")

        time = (int(hours) * 60) + int(minutes)

        # Account number and sort code for the card payment account
        # demonstrating how it would work if set up on recievers card processor when paying
        account_num = "00213181"
        sort_code = "286376"

        try:
            db_connector = DbConnector()
            conn = db_connector.getConn()
            cursor = conn.cursor(buffered=True)

            cursor.execute("SELECT * FROM UserAccounts")
            row = cursor.fetchone()

            while row is not None:
                if row[2] == user_id:
                    transferer_account_num = row[0]
                    transferer_sort_code = row[1]
                    break

                else:
                    row = cursor.fetchone()

            # Determining whether transaction can go ahead by machine learning
            t_list = Transaction.fetch_transactions(transferer_account_num)
            new_transaction = MLTransaction(receiver_name, transfer_value, latitude, longitude, time)
            if len(t_list) < 5:
                print("not enough prior transactions")
            else:
                p_fraud = new_transaction.analyse_transaction(t_list)
                print("Probabiliy of fraud =", p_fraud)
                if p_fraud > 1:
                    return redirect(url_for('error_page.error_page_func', code="e7", src="card_payment.html"))

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

            ran = random.randrange(10 ** 80)
            myhex = "%016x" % ran
            myhex = myhex[:16]

            transaction_id = dt_string + myhex

            balance_change = transfer_value - transfer_value - transfer_value

            transaction_type = "card transfer"

            card_num_sending = 0000000000000000

            cursor.execute("INSERT INTO Transactions VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (transaction_id, transferer_account_num, account_num, transferer_sort_code, sort_code,
                            balance_change, date, time, transaction_type, card_num_sending, receiver_name,
                            longitude, latitude))

            conn.commit()
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
            return redirect(url_for('error_page.error_page_func', code="e2", src="accounts.html"))

        return redirect(url_for('account_page.accounts_page'))

    return render_template('card_payment.html')
