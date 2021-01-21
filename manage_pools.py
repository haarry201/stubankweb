from flask import Flask, Blueprint, render_template, session
import expenditure_reports
from controllers.DbConnector import DbConnector

manage_pools = Blueprint('manage_pools', __name__, template_folder='templates')


@manage_pools.route('/', methods=['GET', 'POST'])
def manage_pools_func():
    return render_template('manage_pools.html')  # returns the html page


def get_user_id():  # this code was reused from expenditure_reports.get_info()
    user_id = ''
    db_connector = DbConnector()  # gets db connection
    conn = db_connector.getConn()
    db_connector.closeConn(conn)
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM UserInfo")  # gets all data stored in UserInfo table
    row = cursor.fetchone()
    while row is not None:
        if row[5] == session['name']:
            user_id = row[0]
    return user_id  # returns the user id of the current user


@manage_pools.route('/create_money_pool')
def create_money_pool():
    try:
        return render_template('extra_info.html', command="Contact", name=session['name'])
    except KeyError:
        return render_template('extra_info.html', command="Contact", name='')
    #user_id = get_user_id()
    print("test")
    return


def access_money_pool():
    conn = expenditure_reports.get_conn()  # uses existing function for getting a db connection
    return


def leave_money_pool():
    conn = expenditure_reports.get_conn()  # uses existing function for getting a db connection
    return


def deposit_to_money_pool():
    conn = expenditure_reports.get_conn()  # uses existing function for getting a db connection
    return


def withdraw_from_money_pool():
    conn = expenditure_reports.get_conn()  # uses existing function for getting a db connection
    return


def delete_money_pool():
    conn = expenditure_reports.get_conn()  # uses existing function for getting a db connection
    return
