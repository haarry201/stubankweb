import binascii
import hashlib
import os
import random
import string
from datetime import datetime

import expenditure_reports_page
from flask import Blueprint, render_template, session, request

manage_pools = Blueprint('manage_pools', __name__, template_folder='templates')


@manage_pools.route('/', methods=['GET', 'POST'])
def manage_pools_func():
    """

    :return:
    """
    pools = []
    pool_ids = get_pool_ids(get_user_id())

    for pool_id in pool_ids:
        conn = expenditure_reports_page.get_conn()
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM PoolAccounts")  # gets all data stored in PoolAccounts table
        row = cursor.fetchone()

        while row is not None:
            if row[0] == pool_id:
                pool_name = row[2]
                pool_balance = row[1]
                pool_date = row[6]
                pool_owner = row[5]
                members_firstnames = get_member_firstnames(pool_id)

                pools.append(pool_name + "," + pool_id + "," + str(pool_balance) + "," + members_firstnames + "," +
                             pool_date + "," + pool_owner)
            row = cursor.fetchone()
        cursor.close()
        conn.close()

    return render_template('manage_pools.html', pools=pools)  # returns the html page


@manage_pools.route('/create_money_pool', methods=['GET', 'POST'])
def create_money_pool():
    """

    :return:
    """
    if request.method == "POST":
        pool_id = ''.join(  # generate a random id for the pool to be used as the pk
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        pool_join_code = ''.join(  # generate a random id for the pool to be used as the join code
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        pool_name = request.form.get("pool_name")  # get values from the web page
        pool_password = request.form.get("pool_password")

        pool_salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')  # generate salt for password hashing
        pool_pwd = hashlib.pbkdf2_hmac('sha512', pool_password.encode('utf-8'), pool_salt, 100000)
        pool_pwdhash = binascii.hexlify(pool_pwd)  # hash password using salt, this is what is stored in database
        pool_owner_name = session['name']
        date = datetime.today().strftime('%d/%m/%Y')

        pool_balance = 0
        user_id = get_user_id()

        query = "INSERT INTO PoolAccounts " \
                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        args = (pool_id, pool_balance, pool_name, pool_pwdhash, pool_salt, pool_owner_name, date, pool_join_code)
        execute_query(query, args)

        query = "INSERT INTO UserPools " \
                "VALUES(%s, %s)"
        args = (pool_id, user_id)
        execute_query(query, args)

        return render_template('accounts.html')
    return render_template('register.html')


@manage_pools.route('/join_money_pool', methods=['GET', 'POST'])
def join_money_pool():
    """

    :return:
    """
    if request.method == "POST":
        entered_join_id = request.form.get("join_code")  # get values from the web page
        user_id = get_user_id()
        conn = expenditure_reports_page.get_conn()  # uses existing function for getting a db connection
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM PoolAccounts")  # gets all data stored in UserPools table
        row = cursor.fetchone()

        while row is not None:
            if row[7] == entered_join_id:
                pool_id = row[0]
                query = "INSERT INTO UserPools " \
                        "VALUES(%s, %s)"
                args = (pool_id, user_id)
                execute_query(query, args)
            row = cursor.fetchone()
        cursor.close()
        return render_template('accounts.html')
    return render_template('register.html')


def get_user_id():
    """

    :return:
    """
    conn = expenditure_reports_page.get_conn()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM UserInfo")  # gets all data stored in UserInfo table
    row = cursor.fetchone()
    while row is not None:
        if row[5] == session['name']:
            user_id = row[0]
            return user_id  # returns the user id of the current user


def get_pool_ids(user_id):
    """

    :param user_id:
    :return:
    """
    pool_ids = []
    conn = expenditure_reports_page.get_conn()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM UserPools")  # gets all data stored in UserInfo table
    row = cursor.fetchone()
    while row is not None:
        if row[1] == user_id:
            pool_ids.append(row[0])
        row = cursor.fetchone()
    return pool_ids  # returns all the pool id's for the user's pools


def get_member_firstnames(pool_id):
    """

    :param pool_id:
    :return:
    """
    conn = expenditure_reports_page.get_conn()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM UserPools")  # gets all data stored in UserPools table
    row = cursor.fetchone()

    members_ids = []
    while row is not None:
        if row[0] == pool_id:
            members_ids.append(row[1])
        row = cursor.fetchone()
    cursor.close()

    for member_id in members_ids:
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM UserInfo")  # gets all data stored in UserPools table
        row = cursor.fetchone()

        members_firstnames = ""
        while row is not None:
            if row[0] == member_id:
                if len(members_firstnames) == 0:
                    members_firstnames += row[5]
                else:
                    members_firstnames += ", " + row[5]
            row = cursor.fetchone()
        cursor.close()
    return members_firstnames


def execute_query(query, args):
    """

    :param query:
    :param args:
    :return:
    """
    conn = expenditure_reports_page.get_conn()  # use existing function to get database connection
    cursor = conn.cursor()
    cursor.execute(query, args)
    conn.commit()
    cursor.close()
    conn.close()
