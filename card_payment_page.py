from flask import Blueprint, render_template, request, redirect, url_for, session

from classes.UserBankAccount import UserBankAccount
from controllers.DbConnector import DbConnector
from mysql.connector import Error
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
def card_payment_page_func():
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
        account_info = request.form.get("account_sender_info")
        account_info_split = account_info.split(",")
        transferer_account_num = account_info_split[0]
        transferer_sort_code = account_info_split[1]
        receiver_name = request.form.get("receiver_name")
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
        receiver_account_num = "00213181"
        receiver_sort_code = "286376"

        try:
            db_connector = DbConnector()
            conn = db_connector.getConn()
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM UserAccounts WHERE AccountNum = (%s) AND SortCode = (%s)",
                           (transferer_account_num, transferer_sort_code))
            result = cursor.fetchall()
            for row in result:
                current_user_balance = int(row[5])
                current_user_overdraft = int(row[4])
                potential_balance = current_user_balance - transfer_value
                print(current_user_overdraft)
                if potential_balance < min(0, current_user_overdraft * -1):
                    return redirect(
                        url_for('error_page.error_page_func', code="e11", src="card_payment_page_func.html"))

            cursor.execute("UPDATE UserAccounts SET CurrentBalance = CurrentBalance - (%s) WHERE AccountNum = (%s) AND"
                           " SortCode = (%s)", (transfer_value, transferer_account_num, transferer_sort_code))

            cursor.execute("SELECT * FROM UserAccounts WHERE AccountNum = (%s) AND SortCode = (%s)",
                           (receiver_account_num, receiver_sort_code))
            result = cursor.fetchall()

            for row in result:
                receiver_user_id = row[2]
                transferee_value_current = int(row[5])
                new_transferee_value = transferee_value_current + transfer_value
                cursor.execute("UPDATE UserAccounts SET CurrentBalance = (%s) WHERE"
                               " AccountNum = (%s) AND SortCode = (%s)",
                               (new_transferee_value, receiver_account_num, receiver_sort_code))

            cursor.execute("SELECT * FROM UserInfo WHERE UserID = (%s)", (receiver_user_id,))
            result = cursor.fetchall()
            for row in result:
                receiver_name = row[5] + " " + row[6]

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
                    return redirect(url_for('error_page.error_page_func', code="e7", src="card_payment_page_func.html"))

            cursor.execute("INSERT INTO Transactions VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (transaction_id, transferer_account_num, receiver_account_num, transferer_sort_code,
                            receiver_sort_code,
                            balance_change, date, time, transaction_type, card_num_sending, receiver_name,
                            longitude, latitude))

            conn.commit()
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
            return redirect(url_for('error_page.error_page_func', code="e2", src="accounts.html"))

        return redirect(url_for('account_page.account_page_func'))

    users_accounts = []
    db_connector = DbConnector()
    conn = db_connector.getConn()
    cursor = conn.cursor(buffered=True)

    cursor.execute(
        "SELECT * FROM UserAccounts,UserAccountInfo WHERE UserID = (%s) AND UserAccounts.AccountTypeID = UserAccountInfo.AccountTypeID",
        (user_id,))
    result = cursor.fetchall()
    for row in result:
        print(row)
        user_bank_account = UserBankAccount(row[0], row[1], row[5], row[4], row[8], row[3])
        users_accounts.append(user_bank_account)
    cursor.close()
    conn.close()
    return render_template('card_payment.html',users_accounts=users_accounts)
