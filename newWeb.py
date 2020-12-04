from flask import Flask, Blueprint
from controllers.DbConnector import DbConnector

simple_page = Blueprint('simple_page', __name__, template_folder='templates')
@simple_page.route('/<page>')
def show(page):
    db_connector = DbConnector()
    conn = db_connector.getConn()
    db_connector.closeConn(conn)
    return 'We Have Connected'