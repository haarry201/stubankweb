from flask import Blueprint, render_template, request, redirect, url_for, session
from controllers.DbConnector import DbConnector
from random import *
from mysql.connector import Error

'''
File name: bank_acc_application_page.py
Author: Harry Kenny
Credits: Harry Kenny, Jacob Scase
Date created: 13/12/2020
Date last modified: 25/01/2021
Python version: 3.7
Purpose: Back-end file for allowing the user to apply for a bank account
'''

bank_acc_application_page = Blueprint('bank_acc_application_page', __name__, template_folder='templates')


@bank_acc_application_page.route('/', methods=['GET', 'POST'])
def bank_acc_application_page_func():
    try:
        # redirects user appropriately based on 2FA status, or whether they are an admin or not
        if 'user_id' in session:
            if session['needs_auth'] == True:
                return redirect(url_for('login_page.login_page_func'))
            elif session['user_role'] == 'User':
                pass
            else:
                return redirect(url_for('admin_home_page.admin_home_page_func'))
        else:
            return redirect(url_for('login_page.login_page_func'))
    except:
        return redirect(url_for('login_page.login_page_func'))
    if request.method == 'POST':
        account_type = request.form.get("account type")
        # determines account type id and the overdraft depending of which account type the user selected
        if account_type == "student current account":
            account_type_id = '123'
            agreed_overdraft = 150000
        elif account_type == "savings account":
            account_type_id = '100'
            agreed_overdraft = 0
        else:
            return redirect(url_for('error_page.error_page_func', code="e2"))

        # gets the user's email from the session object
        email = session['email']
        # randomly generates an account number and sort code for the account
        account_num = ''.join(["{}".format(randint(0, 9)) for num in range(0, 8)])
        sort_code = ''.join(["{}".format(randint(0, 9)) for num in range(0, 6)])

        current_balance = 0


        try:
            db_connector = DbConnector()
            conn = db_connector.getConn()
            cursor = conn.cursor(buffered=True)

            cursor.execute ("SELECT * FROM UserInfo")
            row = cursor.fetchone()
            while row is not None:
                if row[1] == email:
                        user_id = row[0]
                        break
                else:
                    row = cursor.fetchone()

            # inserts data into the Accounts table in the database
            cursor.execute("INSERT INTO Accounts VALUES (%s, %s)", (account_num, sort_code))

            # inserts data into the UserAccounts table in the database
            cursor.execute("INSERT INTO UserAccounts VALUES (%s, %s, %s, %s, %s, %s)", (account_num, sort_code,\
                            user_id, account_type_id, agreed_overdraft, current_balance))



            conn.commit()
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
            return redirect(url_for('error_page.error_page_func',code="e2"))

        return redirect(url_for('account_page.account_page_func'))

    return render_template('bank_application.html')
