from flask import Flask, Blueprint, render_template, session, redirect, url_for
from controllers.DbConnector import DbConnector
import expenditure_reports
from datetime import date, timedelta

account_page = Blueprint('account_page', __name__, template_folder='templates')


@account_page.route('/')
def accounts_page():
    try:
        if 'user_id' in session:
            pass
        else:
            return redirect(url_for('login_page.login_page_func'))
    except:
        return redirect(url_for('login_page.login_page_func'))
    conn = expenditure_reports.get_conn()
    accounts = expenditure_reports.get_info()  # uses previously written functionality to get all accounts owned by user
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM UserAccounts")  # gets all data stored in UserAccounts table
    row = cursor.fetchone()
    found_savings = False
    found_current = False
    savings_acc = ''; current_acc = ''
    while row is not None:
        if str(row[0]) in accounts:
            if str(row[3]) == '100':
                savings_bal_pence = int(row[5])
                savings_bal_pounds = savings_bal_pence/100  # if account is a 'savings' account, sets savings balance
                savings_acc = str(row[0])
                found_savings = True
            else:
                current_bal_pence = int(row[5])
                current_bal_pounds = current_bal_pence/100  # if account is a 'student' account, sets student balance
                current_acc = str(row[0])
                found_current = True
        row = cursor.fetchone()
    if not found_savings:
        savings_bal = 'N/A'
    else:
        savings_bal = format(savings_bal_pounds, '.2f')  # rounds to 2dp to display as amount of money

    if not found_current:
        current_bal = 'N/A'
    else:
        current_bal = format(current_bal_pounds, '.2f')  # rounds to 2dp to display as amount of money

    cursor.execute("SELECT * FROM Transactions ORDER BY Date DESC")
    row = cursor.fetchone()
    transactions = []

    today = date.today()
    two_weeks = today - timedelta(days=14)  # gets date from 2 weeks ago as boundary for 'recent' transactions
    t_day = str(today.day); w_day = str(two_weeks.day)
    t_month = str(today.month); w_month = str(two_weeks.month)
    if today.day < 10:
        t_day = "0" + t_day
    if today.month < 10:
        t_month = "0" + t_month
    if two_weeks.day < 10:
        w_day = "0" + w_day
    if two_weeks.month < 10:
        w_month = "0" + w_month
    today = str(today.year) + "-" + t_month + "-" + t_day
    two_weeks = str(two_weeks.year) + "-" + w_month + "-" + w_day
    b_year = today[0:4]; e_year = two_weeks[0:4]
    b_month = today[5:7]; e_month = two_weeks[5:7]
    b_day = today[8:10]; e_day = two_weeks[8:10]
    start_boundary = date(int(b_year), int(b_month), int(b_day))
    end_boundary = date(int(e_year), int(e_month), int(e_day))  # sets start and end boundaries as dates for comparison to database
    while row is not None:
        source = ''; t_type = ''
        date_of_transaction = str(row[6])
        year = date_of_transaction[0:4]
        month = date_of_transaction[5:7]
        day = date_of_transaction[8:10]
        date_to_check = date(int(year), int(month), int(day))
        # recipient, account source, transaction type, amount, date
        if str(row[1]) in accounts and (end_boundary <= date_to_check <= start_boundary):  # primary conditions to meet
            recipient = str(row[10])
            transactions.append(recipient)
            if str(row[1]) == current_acc:
                source = "Current Account"
            elif str(row[1]):
                source = "Savings Account"
            transactions.append(source)

            if "direct" in str(row[8]).lower():
                t_type = "Direct Transfer"
            elif "card" in str(row[8]).lower():
                t_type = "Card Payment"
            elif "recurring" in str(row[8]).lower():
                t_type = "Recurring Transaction"
            transactions.append(t_type)

            amount = (abs(row[5])/100)
            amount = "%.2f" % amount
            transactions.append(amount)
            year = date_of_transaction[0:4]
            month = date_of_transaction[5:7]
            day = date_of_transaction[8:10]
            transaction_date = day + "/" + month + "/" + year
            transactions.append(transaction_date)
        row = cursor.fetchone()

    if 'name' in session:
        return render_template('accounts.html', title='Home', user=session['name'], savings=savings_bal, current=current_bal, transactions=transactions)
    else:
        return redirect(url_for('error_page.error_page_foo',code="e1", src="index.html"))
