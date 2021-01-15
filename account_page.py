from flask import Flask, Blueprint, render_template, session, redirect, url_for
from controllers.DbConnector import DbConnector

account_page = Blueprint('account_page', __name__, template_folder='templates')


@account_page.route('/')
def accounts_page():
    db_connector = DbConnector()
    conn = db_connector.getConn()
    db_connector.closeConn(conn)
    if 'name' in session:
        return render_template('accounts.html', title='Home', user=session['name'])
    else:
        return redirect(url_for('error_page.error_page_foo',code="e1", src="index.html"))
