from flask import Flask, Blueprint, render_template
from controllers.DbConnector import DbConnector

login_page = Blueprint('login_page', __name__, template_folder='templates')


@login_page.route('/')
def login_page_func():
    db_connector = DbConnector()
    conn = db_connector.getConn()
    db_connector.closeConn(conn)
    user = {'username': 'Hello World'}
    return render_template('login.html', title='Home', user=user)