from flask import Flask, Blueprint, render_template, session
from controllers.DbConnector import DbConnector

expenditure_reports = Blueprint('expenditure_reports', __name__, template_folder='templates')


@expenditure_reports.route('/')
def reports():
    db_connector = DbConnector()
    conn = db_connector.getConn()
    db_connector.closeConn(conn)
    return render_template('reports.html', user=session['name'])