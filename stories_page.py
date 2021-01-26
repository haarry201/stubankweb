from flask import Blueprint, render_template, request, redirect, url_for, session

from controllers.DbConnector import DbConnector
from classes.StoryTransaction import StoryTransaction
from datetime import datetime


'''
File name: stories_page.py
Author: Jacob Scase
Credits: Jacob Scase
Date created: 26/01/2021
Date last modified: 26/01/2021
Python version: 3.7
Purpose: Back-end file for allowing the user to view their transaction information as stories
'''

stories_page = Blueprint('stories_page', __name__, template_folder='templates')


@stories_page.route('/', methods=['GET', 'POST'])
def stories_page_func():
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

    weekly_transactions = []
    week_prior_transactions = []
    monthly_transactions = []
    db_connector = DbConnector()
    conn = db_connector.getConn()
    cursor = conn.cursor(buffered=True)

    cursor.execute(
        "SELECT * FROM UserAccounts,Transactions WHERE UserID = (%s) AND UserAccounts.AccountNum = Transactions.AccountNumSending",
        (user_id,))
    result = cursor.fetchall()
    for row in result:
        # Parsing all datbase data into an object, then into different lists to be analysed
        transaction_date = row[12]
        transaction_amount = int(row[11])*-1
        today_date = datetime.today().date()
        days_between = (today_date - transaction_date).days
        transaction_time = row[13]
        transaction_recipient = row[16]
        new_transaction = StoryTransaction(transaction_date, transaction_recipient, transaction_amount, transaction_time)
        if days_between < 7:
            weekly_transactions.append(new_transaction)
        elif 14 > days_between >= 7:
            week_prior_transactions.append(new_transaction)
        if days_between < 30:
            monthly_transactions.append(new_transaction)
    amount_spent_in_week = 0
    spending_at_places = {}
    amount_spent_in_week_prior = 0
    amount_spent_in_month = 0
    for transaction in weekly_transactions:
        amount_spent_in_week += transaction.amount
        if transaction.recipient not in spending_at_places:
            spending_at_places[transaction.recipient] = transaction.amount
        else:
            spending_at_places[transaction.recipient] += transaction.amount
    for transaction in week_prior_transactions:
        amount_spent_in_week_prior += transaction.amount
    for transaction in monthly_transactions:
        amount_spent_in_month += transaction.amount
    cursor.close()
    conn.close()
    max_recipient_value = 0
    max_recipient_name = ""
    print(spending_at_places)
    for recipient in spending_at_places:
        print(spending_at_places[recipient])
        if spending_at_places[recipient] > max_recipient_value:
            max_recipient_value = spending_at_places[recipient]
            max_recipient_name = recipient
            print("A")
    return render_template('stories_page.html',amount_spent_in_week=amount_spent_in_week, amount_spent_in_week_prior=amount_spent_in_week_prior, amount_spent_in_month=amount_spent_in_month, max_recipient_value=max_recipient_value,max_recipient_name=max_recipient_name)
