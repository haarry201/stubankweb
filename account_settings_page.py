from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from controllers.DbConnector import DbConnector
from mysql.connector import MySQLConnection, Error
from controllers.DbConnector import DbConnector
from controllers.Offer import Offer
from datetime import datetime

account_settings_page = Blueprint('account_settings_page', __name__, template_folder='templates')


@account_settings_page.route('/', methods=['GET', 'POST'])
def account_settings_page_func():
    try:
        if 'user_id' in session:
            if session['needs_auth'] == True:
                return redirect(url_for('login_page.login_page_func'))
            else:
                user_id = session['user_id']
        else:
            return redirect(url_for('login_page.login_page_func'))
    except:
        return redirect(url_for('login_page.login_page_func'))
    if request.method == "POST":
        print("aa")

    try:
        db_connector = DbConnector()
        conn = db_connector.getConn()
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM UserInfo WHERE UserID = (%s)",(user_id,))
    except Error as error:
        print(error)
        return redirect(url_for('error_page.error_page_foo', code="e2", src="accounts.html"))

    return render_template('account_settings.html')