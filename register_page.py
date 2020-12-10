from flask import Flask, Blueprint, render_template
from controllers.DbConnector import DbConnector

register_page = Blueprint('register_page', __name__, template_folder='templates')


@register_page.route('/')
def register_page_func():
    db_connector = DbConnector()
    conn = db_connector.getConn()
    db_connector.closeConn(conn)
    user = {'username': 'Hello World'}
    return render_template('register.html', title='Home', user=user)