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
    accounts = get_info()  # gets all accounts owned by user that is currently logged in
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    dates = []  # dates to output in report, in dd/mm format
    dates_to_check = []  # dates to check database with, in mm-dd format
    today = date.today()

    for i in range(7):
        dates.append(str(today.day) + "/" + str(today.month))
        day = str(today.day)
        month = str(today.month)
        if today.day < 10:
            day = "0" + day
        if today.month < 10:
            month = "0" + month
        dates_to_check.append(str(today.year) + "-" + month + "-" + day)
        today = today - timedelta(days=1)  # gets yesterday's date

    cursor.execute("SELECT * FROM Transactions")  # selects all transactions from transactions table
    row = cursor.fetchone()  # fetches first row of table

    values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    biggest = 0
    end = dates_to_check[0]; begin = dates_to_check[6]
    b_year = begin[0:4]; e_year = end[0:4]
    b_month = begin[5:7]; e_month = end[5:7]
    b_day = begin[8:10]; e_day = end[8:10]
    start_date = date(int(b_year), int(b_month), int(b_day))
    end_date = date(int(e_year), int(e_month), int(e_day))  # gets boundary dates to use as check while reading from database
    while row is not None:
        date_of_transaction = str(row[6])
        year = date_of_transaction[0:4]
        month = date_of_transaction[5:7]
        day = date_of_transaction[8:10]
        date_to_check = date(int(year), int(month), int(day))
        print(str(start_date) + " " + str(date_to_check) + " " + str(end_date) + str(start_date <= date_to_check <= end_date))
        if str(row[1]) in accounts and (start_date <= date_to_check <= end_date):  # primary conditions to meet
            if str(row[6]) == dates_to_check[0]:
                values[0] += abs(row[5])
            elif str(row[6]) == dates_to_check[1]:
                values[1] += abs(row[5])
            elif str(row[6]) == dates_to_check[2]:
                values[2] += abs(row[5])
            elif str(row[6]) == dates_to_check[3]:
                values[3] += abs(row[5])
            elif str(row[6]) == dates_to_check[4]:
                values[4] += abs(row[5])
            elif str(row[6]) == dates_to_check[5]:
                values[5] += abs(row[5])
            elif str(row[6]) == dates_to_check[6]:
                values[6] += abs(row[5])  # if statements to decide which 'bar' if graph data fits into
            else:
                print(str(row[6]))

            if abs(row[5]) > biggest: biggest = abs(row[5])  # if this transaction bigger, resets 'biggest' variable

        row = cursor.fetchone()

    dates.reverse()
    values.reverse()  # reverses arrays to show in chronological order least->most recent on graph

    if biggest == 0:
        biggest2 = "N/A"
    else:
        biggest2 = "£" + str(biggest)

    legend = 'Expenditure report for last 7 days'
    return render_template('report_final.html', values=values, labels=dates, legend=legend, big=biggest2)


@report_building.route('/weekly')
def reports_weekly():
    accounts = get_info()  # gets all user owned accounts
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    today = date.today()
    mondays = []
    if today.weekday() == 0:
        mondays.append(str(today.year) + "-" + str(today.month) + "-" + str(today.day))   # if today is a monday, adds to array

    while len(mondays) < 4:  # finds dates of past 4 mondays to use as graph headings
        today = today - timedelta(days=1)
        if today.weekday() == 0:  # .weekday returns 0 if Monday, 1 if Tuesday etc.
            mondays.append(str(today.year) + "-" + str(today.month) + "-" + str(today.day))

    totals = [0.0, 0.0, 0.0, 0.0]
    biggest = 0
    cursor.execute("SELECT * FROM Transactions")  # selects all transactions from transactions table
    row = cursor.fetchone()  # fetches first row of table

    while row is not None:
        if str(row[1]) in accounts:  # checks if account that did transaction is owned by currently logged in user
            date_of_transaction = str(row[6])
            year = date_of_transaction[0:4]
            month = date_of_transaction[5:7]
            day = date_of_transaction[8:10]
            date_to_check = date(int(year), int(month), int(day))
            monday1 = mondays[0].split("-"); week4 = date(int(monday1[0]), int(monday1[1]), int(monday1[2]))
            monday2 = mondays[1].split("-"); week3 = date(int(monday2[0]), int(monday2[1]), int(monday2[2]))
            monday3 = mondays[2].split("-"); week2 = date(int(monday3[0]), int(monday3[1]), int(monday3[2]))
            monday4 = mondays[3].split("-"); week1 = date(int(monday4[0]), int(monday4[1]), int(monday4[2]))
            # gets boundary dates for checking which week a transaction falls into
            today = date.today(); week_today = date(today.year, today.month, today.day)
            if week1 <= date_to_check <= week_today:  # if transaction was within the last 4 days
                if week1 <= date_to_check < week2:
                    totals[0] += abs(row[5])
                elif week2 <= date_to_check < week3:
                    totals[1] += abs(row[5])
                elif week3 <= date_to_check < week4:
                    totals[2] += abs(row[5])
                else:
                    totals[3] += abs(row[5])
                if abs(row[5]) > biggest: biggest = abs(row[5])
        row = cursor.fetchone()

    dates = []
    for m in mondays:
        format_date = m.split("-")
        dates.append("w.b. " + format_date[2] + "/" + format_date[1])  # puts 'mondays' in format for graph headings

    dates.reverse()  # reverses array to show in chronological order least->most recent on graph

    if biggest == 0:
        biggest2 = "N/A"
    else:
        biggest2 = "£" + str(biggest)

    legend = 'Expenditure report for last 4 weeks'
    return render_template('report_final.html', values=totals, labels=dates, legend=legend, big=biggest2)


@report_building.route("/yearly")
def reports_yearly():
    accounts = get_info()  # gets all user owned accounts
    conn = get_conn()
    cursor = conn.cursor(buffered=True)
    today = date.today()
    dates = []
    for i in range(12):
        if today.month < 10:
            dates.append(str(today.year) + "-0" + str(today.month) + "-01")
        else:
            dates.append(str(today.year) + "-" + str(today.month) + "-01")
        today = date(today.year, today.month, 1)
        today = today - timedelta(days=1)

    totals = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    biggest = 0
    cursor.execute("SELECT * FROM Transactions")  # selects all transactions from transactions table
    row = cursor.fetchone()  # fetches first row of table

    while row is not None:
        if str(row[1]) in accounts:  # checks if account that did transaction is owned by currently logged in user
            date_of_transaction = str(row[6])
            year = date_of_transaction[0:4]
            month = date_of_transaction[5:7]
            day = date_of_transaction[8:10]
            date_to_check = date(int(year), int(month), int(day))
            first1 = dates[0].split("-"); month12 = date(int(first1[0]), int(first1[1]), int(first1[2]))
            first2 = dates[1].split("-"); month11 = date(int(first2[0]), int(first2[1]), int(first2[2]))
            first3 = dates[2].split("-"); month10 = date(int(first3[0]), int(first3[1]), int(first3[2]))
            first4 = dates[3].split("-"); month9 = date(int(first4[0]), int(first4[1]), int(first4[2]))
            first5 = dates[4].split("-"); month8 = date(int(first5[0]), int(first5[1]), int(first5[2]))
            first6 = dates[5].split("-"); month7 = date(int(first6[0]), int(first6[1]), int(first6[2]))
            first7 = dates[6].split("-"); month6 = date(int(first7[0]), int(first7[1]), int(first7[2]))
            first8 = dates[7].split("-"); month5 = date(int(first8[0]), int(first8[1]), int(first8[2]))
            first9 = dates[8].split("-"); month4 = date(int(first9[0]), int(first9[1]), int(first9[2]))
            first10 = dates[9].split("-"); month3 = date(int(first10[0]), int(first10[1]), int(first10[2]))
            first11 = dates[10].split("-"); month2 = date(int(first11[0]), int(first11[1]), int(first11[2]))
            first12 = dates[11].split("-"); month1 = date(int(first12[0]), int(first12[1]), int(first12[2]))
            # gets boundary dates for checking which week a transaction falls into
            today = date.today(); month_today = date(today.year, today.month, today.day)
            if month1 <= date_to_check <= month_today:  # if transaction was within the last 4 days
                if month1 <= date_to_check < month2:
                    totals[0] += abs(row[5])
                elif month2 <= date_to_check < month3:
                    totals[1] += abs(row[5])
                elif month3 <= date_to_check < month4:
                    totals[2] += abs(row[5])
                elif month4 <= date_to_check < month5:
                    totals[3] += abs(row[5])
                elif month5 <= date_to_check < month6:
                    totals[4] += abs(row[5])
                elif month6 <= date_to_check < month7:
                    totals[5] += abs(row[5])
                elif month7 <= date_to_check < month8:
                    totals[6] += abs(row[5])
                elif month8 <= date_to_check < month9:
                    totals[7] += abs(row[5])
                elif month9 <= date_to_check < month10:
                    totals[8] += abs(row[5])
                elif month10 <= date_to_check < month11:
                    totals[9] += abs(row[5])
                elif month11 <= date_to_check < month12:
                    totals[10] += abs(row[5])
                else:
                    totals[11] += abs(row[5])
                if abs(row[5]) > biggest: biggest = abs(row[5])
        row = cursor.fetchone()

    dates_display = []
    for d in dates:
        format_date = d.split("-")
        dates_display.append(format_date[0] + "/" + format_date[1])  # puts dates in format for graph headings

    dates_display.reverse() # reverses array to show in chronological order least->most recent on graph

    if biggest == 0:
        biggest2 = "N/A"
    else:
        biggest2 = "£" + str(biggest)

    legend = 'Expenditure report for last 12 months'
    return render_template('report_final.html', values=totals, labels=dates_display, legend=legend, big=biggest2)