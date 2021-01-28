from mysql.connector import Error
from flask import Flask, Blueprint, render_template, session, redirect, url_for, request
from controllers.DbConnector import DbConnector

'''
File name: all_transactions_page.py
Author: Jacob Scase
Credits: Jacob Scase
Date created: 27/01/2021
Date last modified: 27/01/2021
Python version: 3.7
Purpose: Back-end file to show all the users transactions once logged in. Page will take longer to load and will be
         larger as more transactions are processed
'''

all_transactions_page = Blueprint('all_transactions_page', __name__, template_folder='templates')


@all_transactions_page.route('/', methods=['GET', 'POST'])
def all_transactions_page_func():
    try:
        # redirects user appropriately based on 2FA status, or whether they are an admin or not
        if 'user_id' in session:
            if session['needs_auth'] == True:
                return redirect(url_for('login_page.login_page_func'))
            elif session['user_role'] == 'User':
                user_id = session['user_id']
                pass
            else:
                return redirect(url_for('admin_home_page.admin_home_page_func'))
        else:
            return redirect(url_for('login_page.login_page_func'))
    except:
        return redirect(url_for('login_page.login_page_func'))
    try:
        # Trying to get the previous page, and increment it by 1 if
        page_num = 1
        try:
            page_num = int(request.args.get('page_num'))
            if page_num < 1:
                page_num = 1
        except:
            pass

        number_of_transactions_to_start_at = (page_num - 1) * 50
        number_of_transactions_to_end_at = page_num * 50
        # Will display 50 transactions at a time
        # Paging of transactions only displays when number of transactions above 50
        db_connector = DbConnector()
        conn = db_connector.getConn()
        cursor = conn.cursor(buffered=True)

        cursor.execute(
            "SELECT * FROM UserAccounts,Transactions WHERE UserID = (%s) AND UserAccounts.AccountNum = Transactions.AccountNumSending",
            (user_id,))
        result = cursor.fetchall()
        transactions = []
        for row in result:
            account_type = row[3]
            transaction_date = row[12].strftime('%d/%m/%Y')
            transaction_amount = int(row[11]) * -1
            transaction_type = row[14]
            recipient_name = row[16]
            new_transaction = {"date": transaction_date, "amount": transaction_amount, "t_type": transaction_type,
                               "recipient": recipient_name, "a_type": account_type}
            transactions.append(new_transaction)
        user_account_info_dict = {}
        cursor.execute("SELECT * FROM UserAccountInfo")
        result = cursor.fetchall()
        for row in result:
            user_account_info_dict[row[0]] = row[2]
        cursor.close()
        conn.close()
        transactions_to_display = transactions[number_of_transactions_to_start_at:number_of_transactions_to_end_at]
    except Error as error:
        print(error)
        return redirect(url_for('error_page.error_page_func', code="e2"))
    if page_num - 1 == 0:
        prior_page_num = 1
    else:
        prior_page_num = page_num - 1
    return render_template('all_transactions.html', transactions=transactions_to_display, page_num=page_num,
                           next_page_num=page_num + 1, prior_page_num=prior_page_num,
                           user_account_info_dict=user_account_info_dict)
