from flask import Flask, Blueprint, render_template
from controllers.DbConnector import DbConnector

offer_page = Blueprint('offer_page', __name__, template_folder='templates')


@offer_page.route('/')
def offer_page_func():
    db_connector = DbConnector()
    conn = db_connector.getConn()
    db_connector.closeConn(conn)
    user = {'username': 'Hello World'}
    return render_template('offers.html', title='Home', user=user)