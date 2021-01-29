import binascii
import hashlib
import os
import random
import string
from datetime import datetime

import expenditure_reports_page
from flask import Blueprint, render_template, session, request, redirect, url_for

'''
File name: manage_pools_page.py
Author: Chris Harvey
Credits: Chris Harvey
Date created: 10/01/2020
Date last modified: 25/01/2021
Python version: 3.7
Purpose: Back-end file for allowing users to manage their pools.
'''

manage_pools_page = Blueprint('manage_pools_page', __name__, template_folder='templates')


@manage_pools_page.route('/', methods=['GET', 'POST'])
def manage_pools_page_func():
    """
    main function - returns template with info to draw HTML table
    :return: displays the manage_pools.html page
    """
    pools = []
    pool_ids = get_pool_ids(get_user_id())  # array of all pool id's the current user is in

    if len(pool_ids) > 0:
        for pool_id in pool_ids:
            conn = expenditure_reports_page.get_conn()
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM PoolAccounts")  # gets all data stored in PoolAccounts table
            row = cursor.fetchone()

            while row is not None:
                if row[0] == pool_id:  # if pool is one the user is in
                    pool_name = row[2]  # gets data from PoolAccounts table
                    pool_balance = row[1]
                    pool_date = row[6]
                    pool_owner = row[5]
                    members_firstnames = get_member_firstnames(pool_id)  # comma separated string of all member firstnames
                    # in the current pool

                    pools.append(pool_name + "," + pool_id + "," + str(pool_balance) + "," + members_firstnames + "," +
                                 pool_date + "," + pool_owner)  # array of comma separated strings used for drawing HTML
                    # table
                row = cursor.fetchone()
            cursor.close()
            conn.close()

    return render_template('manage_pools.html', pools=pools)


@manage_pools_page.route('/create_money_pool', methods=['GET', 'POST'])
def create_money_pool():
    """
    gets entered data for creating pool, hashes password and inputs data into MySQL database
    :return: displays either accounts.html or register.html depending on the request method
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
        pool_pwdhash = binascii.hexlify(pool_pwd)  # hash password using salt
        pool_owner_name = session['name']  # sets the pool owner name to the firstname of the current user
        date = datetime.today().strftime('%d/%m/%Y')  # gets the current date

        pool_balance = 0
        user_id = get_user_id()  # gets the current user's id

        query = "INSERT INTO PoolAccounts " \
                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"  # query to create pool
        args = (pool_id, pool_balance, pool_name, pool_pwdhash, pool_salt, pool_owner_name, date, pool_join_code)
        execute_query(query, args)

        query = "INSERT INTO UserPools " \
                "VALUES(%s, %s)"  # query to create relation between current user and pool
        args = (pool_id, user_id)
        execute_query(query, args)

        return render_template('accounts.html')
    return render_template('register.html')


@manage_pools_page.route('/join_money_pool', methods=['GET', 'POST'])
def join_money_pool():
    """
    gets join code and checks against database value
    :return: displays either accounts.html or register.html depending on the request method
    """
    if request.method == "POST":
        entered_join_id = request.form.get("join_code")  # get values from the web page
        user_id = get_user_id()
        conn = expenditure_reports_page.get_conn()  # uses existing function for getting a db connection
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM PoolAccounts")  # gets all data stored in UserPools table
        row = cursor.fetchone()

        while row is not None:
            if row[7] == entered_join_id:  # if entered join id corresponds to a pool in the database
                pool_id = row[0]  # gets data from database
                query = "INSERT INTO UserPools " \
                        "VALUES(%s, %s)"  # creates relation between user and pool
                args = (pool_id, user_id)
                execute_query(query, args)
                cursor.close()
                return render_template('accounts.html')
            row = cursor.fetchone()
        cursor.close()
        return redirect(url_for('error_page.error_page_func', code="e1"))
    return render_template('register.html')


def get_user_id():
    """
    gets the user id of the current user
    :return: user id of the current user
    """
    conn = expenditure_reports_page.get_conn()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM UserInfo")  # gets all data stored in UserInfo table
    row = cursor.fetchone()
    while row is not None:
        if row[5] == session['name']:  # if current users name corresponds to a user in the database
            user_id = row[0]
            return user_id  # returns the user id of the current user
        row = cursor.fetchone()
    return redirect(url_for('error_page.error_page_func', code="e2"))


def get_pool_ids(user_id):
    """
    gets all the pool id's for the current user's pools
    :param user_id: entered user id
    :return: pool id's for all the current user's pools
    """
    pool_ids = []
    conn = expenditure_reports_page.get_conn()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM UserPools")  # gets all data stored in UserPools table
    row = cursor.fetchone()
    while row is not None:
        if row[1] == user_id:  # if user id corresponds to a relation in the database
            pool_ids.append(row[0])
        row = cursor.fetchone()
    if len(pool_ids) != 0:
        return pool_ids  # returns all the pool id's for the user's pools
    else:
        return []
    return redirect(url_for('error_page.error_page_func', code="e2"))


def get_member_firstnames(pool_id):
    """
    gets the firstnames of all members for a specified pool id
    :param pool_id: entered pool id
    :return: firstnames of all members of a specified pool
    """
    conn = expenditure_reports_page.get_conn()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM UserPools")  # gets all data stored in UserPools table
    row = cursor.fetchone()

    members_ids = []
    while row is not None:
        if row[0] == pool_id:  # if pool id corresponds to a relation in the database
            members_ids.append(row[1])  # adds user id to array
        row = cursor.fetchone()
    cursor.close()

    for member_id in members_ids:
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM UserInfo")  # gets all data stored in UserInfo table
        row = cursor.fetchone()

        members_firstnames = ""
        while row is not None:
            if row[0] == member_id:  # if member id corresponds to a user in the database
                if len(members_firstnames) == 0:  # do for first member firstname
                    members_firstnames += row[5]
                else:  # otherwise do this
                    members_firstnames += ", " + row[5]
            row = cursor.fetchone()
        cursor.close()
    if len(members_firstnames) != 0:
        return members_firstnames  # returns the firstnames of all members in the pool
    return redirect(url_for('error_page.error_page_func', code="e2"))


def execute_query(query, args):
    """
    executes a MySQL query with a specified query and args
    :param query: MySQL query to execute
    :param args: args for the query
    :return: executes MySQL query on database
    """
    conn = expenditure_reports_page.get_conn()  # use existing function to get database connection
    cursor = conn.cursor()
    cursor.execute(query, args)  # execute query
    conn.commit()
    cursor.close()
    conn.close()  # close connection
