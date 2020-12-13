from flask import Flask, Blueprint, render_template
from controllers.DbConnector import DbConnector

bank_acc_application_page = Blueprint('account_application_page', __name__, template_folder='templates')


@bank_acc_application_page.route('/<page>')
def bank_application(page):
    db_connector = DbConnector()
    conn = db_connector.getConn()
    db_connector.closeConn(conn)
    user = {'username': 'Hello World'}
    return render_template('accounts.html', title='Home', user=user)