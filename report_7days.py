from flask import Blueprint, render_template, session
from controllers.DbConnector import DbConnector
from datetime import date, timedelta

report_7days = Blueprint('report_7days', __name__, template_folder='templates')


@report_7days.route('/')
def reports_7days():
    account_id = ''
    db_connector = DbConnector()
    conn = db_connector.getConn()
    db_connector.closeConn(conn)
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM UserInfo")  # gets all data stored in UserInfo table
    row = cursor.fetchone()
    while row is not None:
        if row[5] == session['name']:
            account_id = row[0]  # gets currently logged in user's account id to use while searching UserAccounts
        row = cursor.fetchone()

    accounts = []
    cursor.execute("SELECT * FROM UserAccounts")  # gets all data stored in UserAccounts table
    row = cursor.fetchone()
    while row is not None:
        if row[2] == account_id:
            accounts.append(row[0])  # all account numbers owned by same user stored in accounts
        row = cursor.fetchone()

    dates = []
    today = date.today()
    dates.append(str(today.day) + "/" + str(today.month))

    for i in range(6):
        today = today - timedelta(days=1)  # gets yesterday's date
        dates.append(str(today.day) + "/" + str(today.month))

    cursor.execute("SELECT * FROM Transactions")  # selects all transactions from transactions table
    row = cursor.fetchone()  # fetches first row of table

    values = []
    for d in dates:
        total = 0
        while row is not None:
            if d in row[6] and row[1] in accounts:  # checking so only correct transactions shown on graph
                total += row[5]  # adds transaction price to running total
            row = cursor.fetchone()
        values.append(total)

    dates.reverse()
    values.reverse()  # reverses arrays to show in chronological order least->most recent on graph

    legend = 'Expenditure report for last 7 days'
    return render_template('report_7days.html', values=values, labels=dates, legend=legend)