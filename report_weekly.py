from flask import Blueprint, render_template, session
from controllers.DbConnector import DbConnector
from datetime import date, timedelta

report_weekly = Blueprint('report_weekly', __name__, template_folder='templates')


@report_weekly.route('/')
def reports_weekly():
    db_connector = DbConnector()
    conn = db_connector.getConn()
    db_connector.closeConn(conn)
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM Transactions")  # gets all data stored in Transactions table

    today = date.today()
    mondays = []
    if today.weekday() == 0:
        mondays.append(today)  # if today is a monday

    while len(mondays) < 4:  # finds dates of past 4 mondays
        today = today - timedelta(days=1)
        if today.weekday() == 0:
            mondays.append(today)

    print(mondays)
    values = [10, 4, 8, 9]
    dates = ["01/01", "02/01", "03/01", "04/01"]

    legend = 'Expenditure report for last 4 weeks'
    return render_template('report_weekly.html', values=values, labels=dates, legend=legend)