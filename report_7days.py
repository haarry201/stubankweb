from flask import Blueprint, render_template, session
from controllers.DbConnector import DbConnector

report_7days = Blueprint('report_7days', __name__, template_folder='templates')


@report_7days.route('/')
def reports_7days():
    db_connector = DbConnector()
    conn = db_connector.getConn()
    db_connector.closeConn(conn)
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('report_7days.html', values=values, labels=labels, legend=legend)