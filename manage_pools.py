import hashlib
import os
import random
import string
import binascii

import expenditure_reports
from flask import Blueprint, render_template, session, request

manage_pools = Blueprint('manage_pools', __name__, template_folder='templates')


@manage_pools.route('/', methods=['GET', 'POST'])
def manage_pools_func():
    return render_template('manage_pools.html')  # returns the html page


def get_user_id():  # this code was reused from expenditure_reports.get_info()
    user_id = ''
    conn = expenditure_reports.get_conn()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM UserInfo")  # gets all data stored in UserInfo table
    row = cursor.fetchone()
    while row is not None:
        if row[5] == session['name']:
            user_id = row[0]
    return user_id  # returns the user id of the current user


@manage_pools.route('/create_money_pool', methods=['GET', 'POST'])
def create_money_pool():
    if request.method == "POST":
        conn = expenditure_reports.get_conn()  # use existing function to get database connection
        pool_id = ''.join(  # generate a random id for the pool to be used as the pk
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        pool_name = request.form.get("pool_name")  # get values from the web page
        pool_password = request.form.get("pool_password")

        # generate random 16 digit hex to use as primary key for UserInfo table
        otp_secret_key = random.randint(10000000, 99999999)  # generate one-time password
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')  # generate salt for password hashing
        pwd = hashlib.pbkdf2_hmac('sha512', pool_password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwd)  # hash password using salt, this is what is stored in database

        user_id = get_user_id()
        account_nums = expenditure_reports.get_info()

        #query = "INSERT INTO PoolAccounts " \
                #"VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        #args = (pool_id, )
        return render_template('manage_pools.html')


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
