from flask import Flask, Blueprint, render_template, session
from controllers.DbConnector import DbConnector
from datetime import date, timedelta

report_building = Blueprint('report_building', __name__, template_folder='templates')


def get_conn():
    db_connector = DbConnector()
    conn = db_connector.getConn()
    db_connector.closeConn(conn)
    return conn


def get_info():
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

    return accounts


@report_building.route('/7days')
def reports_7days():
    accounts = get_info()  # gets all user owned accounts
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    dates = []
    today = date.today()
    dates.append(str(today.day) + "/" + str(today.month))

    for i in range(6):
        today = today - timedelta(days=1)  # gets yesterday's date
        dates.append(str(today.day) + "/" + str(today.month))

    cursor.execute("SELECT * FROM Transactions")  # selects all transactions from transactions table
    row = cursor.fetchone()  # fetches first row of table

    values = []
    biggest = 0
    for d in dates:
        total = 0
        while row is not None:
            if d in row[6] and row[1] in accounts:  # checking so only correct transactions shown on graph
                total += row[5]  # adds transaction price to running total
                if row[5] > biggest: biggest = row[5]
            row = cursor.fetchone()
        values.append(total)

    dates.reverse()
    values.reverse()  # reverses arrays to show in chronological order least->most recent on graph

    if biggest == 0:
        biggest = "N/A"

    legend = 'Expenditure report for last 7 days'
    return render_template('report_final.html', values=values, labels=dates, legend=legend, big=biggest)


@report_building.route('/weekly')
def reports_weekly():
    accounts = get_info()  # gets all user owned accounts
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    today = date.today()
    mondays = []
    if today.weekday() == 0:
        mondays.append(today)  # if today is a monday, adds to array

    while len(mondays) < 4:  # finds dates of past 4 mondays to use as graph headings
        today = today - timedelta(days=1)
        if today.weekday() == 0:  # .weekday returns 0 if Monday, 1 if Tuesday etc.
            mondays.append(today)

    totals = []
    biggest = 0
    cursor.execute("SELECT * FROM Transactions")  # selects all transactions from transactions table
    row = cursor.fetchone()  # fetches first row of table

    for m in mondays:
        days = [str(m.day) + "/" + str(m.month) + "/" + str(m.year)]
        for i in range(6):
            today = today - timedelta(days=1)  # gets yesterday's date
            days.append(str(today.day) + "/" + str(today.month) + "/" + str(today.year))

        total = 0
        while row is not None:
            if row[6] in days and row[1] in accounts:  # checking so only correct transactions shown on graph
                total += row[5]  # adds transaction price to running total
                if row[5] > biggest: biggest = row[5]
            row = cursor.fetchone()
        totals.append(total)

    dates = []
    for m in mondays:
        dates.append("w.b. " + str(m.day) + "/" + str(m.month))  # puts 'mondays' in format for graph headings

    dates.reverse()
    totals.reverse()  # reverses arrays to show in chronological order least->most recent on graph

    if biggest == 0:
        biggest = "N/A"

    legend = 'Expenditure report for last 4 weeks'
    return render_template('report_final.html', values=totals, labels=dates, legend=legend, big=biggest)


@report_building.route("/yearly")
def reports_yearly():
    accounts = get_info()
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    years = []
    today = date.today()
    years.append(str(today.month) + "/" + str(today.year))

    for i in range(11):
        today = today - timedelta(days=30)
        years.append(str(today.month) + "/" + str(today.year))

    totals = []
    biggest = 0
    cursor.execute("SELECT * FROM Transactions")  # selects all transactions from transactions table
    row = cursor.fetchone()  # fetches first row of table

    for y in years:
        day = str(today.day) + "/" + y
        total = 0
        while row is not None:
            if row[6] in day and row[1] in accounts:  # checking so only correct transactions shown on graph
                total += row[5]  # adds transaction price to running total
                if row[5] > biggest: biggest = row[5]
            row = cursor.fetchone()
        totals.append(total)

    years.reverse()
    totals.reverse()  # reverses arrays to show in chronological order least->most recent on graph

    if biggest == 0:
        biggest = "N/A"

    legend = 'Expenditure report for last 12 months'
    return render_template('report_final.html', values=totals, labels=years, legend=legend, big=biggest)