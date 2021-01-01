from flask import Blueprint, render_template, session
from controllers.DbConnector import DbConnector
from datetime import date, timedelta

report_7days = Blueprint('report_7days', __name__, template_folder='templates')


@report_7days.route('/')
def reports_7days():
    db_connector = DbConnector()
    conn = db_connector.getConn()
    db_connector.closeConn(conn)
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM Transactions")  # gets all data stored in Transactions table

    dates = []
    today = date.today()
    dates.append(str(today.day) + "/" + str(today.month))

    for i in range(6):
        today = today - timedelta(days=1)
        dates.append(str(today.day) + "/" + str(today.month))

    row = cursor.fetchone()  # fetches first row of table

    values = []
    for d in dates:
        total = 0
        while row is not None:
            if d in row[6]:
                total += row[5]
        values.append(total)

    legend = 'Expenditure report for last 7 days'
    return render_template('report_7days.html', values=values, labels=dates, legend=legend)