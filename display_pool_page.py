import binascii
import hashlib
import mysql

import expenditure_reports_page
from flask import Blueprint, render_template, request, session, url_for, redirect
from manage_pools_page import get_member_firstnames

'''
File name: display_pool_page.py
Author: Chris Harvey
Credits: Chris Harvey
Date created: 10/01/2020
Date last modified: 25/01/2021
Python version: 3.7
Purpose: Back-end file for allowing users to display their pools.
'''

display_pool_page = Blueprint('display_pool_page', __name__, template_folder='templates')


@display_pool_page.route('/', methods=['GET', 'POST'])
def display_pool_page_func():
    """
    main function - returns template with info to draw HTML table and other variables needed for the HTML page
    :return: displays the display_pool.html page or register.html if the user has no pools
    """
    if not session.get("entered_pool_id"):  # if entered pool id has not been initialised
        entered_pool_id = request.form.get("pool_to_view")
        session["entered_pool_id"] = entered_pool_id  # set entered pool id
    conn = expenditure_reports_page.get_conn()  # uses existing function for getting a db connection
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM PoolAccounts")  # gets all data stored in PoolAccounts table
    row = cursor.fetchone()

    pool = []
    while row is not None:
        if row[0] == session['entered_pool_id']:  # if entered pool id equals pool id in database
            members_firstnames = get_member_firstnames(row[0])  # get data from database
            member_ids = get_member_ids(row[0])
            pool_balance = row[1]
            pool_name = row[2]
            owner = row[5]
            date_created = row[6]
            pool_join_code = row[7]
            pool.append(pool_name + "," + session.get("entered_pool_id") + "," + str(
                pool_balance) + "," + members_firstnames + "," + member_ids + "," + date_created + "," + owner)  # array
            # of comma separated strings used for drawing HTML table
        row = cursor.fetchone()
    if len(pool) == 0:  # if entered pool id is not in database
        return redirect(url_for('error_page.error_page_func',code="e1"))
    return render_template('display_pool.html', pool=pool, pool_name=pool_name, pool_join_code=pool_join_code)


@display_pool_page.route('/deposit_money_pool', methods=['GET', 'POST'])
def deposit_money_pool():
    """
    gets data from HTML page and calls function to deposit money into a pool
    :return: displays either accounts.html or register.html depending on the request method
    """
    if request.method == "POST":
        account_number = int(request.form.get("account_number"))  # gets values from the web page
        sort_code = int(request.form.get("sort_code"))
        amount = request.form.get("amount")

        withdraw_and_deposit(account_number, sort_code, amount, True)  # calls function with True to set it to deposit

        return render_template('accounts.html')
    return render_template('register.html')


@display_pool_page.route('/withdraw_money_pool', methods=['GET', 'POST'])
def withdraw_money_pool():
    """
    gets data from HTML page and calls function to withdraw money from a pool
    :return: displays either accounts.html or register.html depending on the request method
    """
    if request.method == "POST":
        account_number = int(request.form.get("account_number"))  # gets values from the web page
        sort_code = int(request.form.get("sort_code"))
        amount = request.form.get("amount")

        withdraw_and_deposit(account_number, sort_code, amount, False)  # calls function with False to set it to
        # withdraw

        return render_template('accounts.html')
    return render_template('register.html')


@display_pool_page.route('/leave_money_pool', methods=['GET', 'POST'])
def leave_money_pool():
    """
    removes the current user from the pool
    :return: displays either manage_pools.html or register.html depending on the request method
    """
    if request.method == "POST":
        conn = expenditure_reports_page.get_conn()  # use existing function to get database connection
        cursor = conn.cursor()
        query = "DELETE FROM UserPools WHERE UserID = %s AND PoolID = %s"  # deletes relation to remove user from pool
        user_id = session.get("user_id")  # gets data to use as args for the MySQL query
        pool_id = session.get("entered_pool_id")
        cursor.execute(query, (user_id, pool_id))  # execute query
        conn.commit()
        cursor.close()
        conn.close()  # close connection

        return render_template('accounts.html')
    return render_template('register.html')


@display_pool_page.route('/add_user_to_money_pool', methods=['GET', 'POST'])
def add_user_to_money_pool():
    """
    displays a join code to the user for them to share with another user
    :return: displays either display_pool.html or register.html depending on the request method
    """
    if request.method == "POST":
        return render_template('display_pool.html')
    return render_template('register.html')


@display_pool_page.route('/remove_user_from_money_pool', methods=['GET', 'POST'])
def remove_user_from_money_pool():
    """
    removes a user from the pool with a specified pool id if the entered password is correct
    :return: displays either accounts.html or register.html depending on the request method
    """
    if request.method == "POST":
        entered_pool_password = request.form.get("pool_password")  # get values from web page
        userid_to_remove = request.form.get("id_to_remove")
        pool_id = session.get("entered_pool_id")

        if check_entered_password(entered_pool_password, pool_id):  # if entered password equals password in database
            conn = expenditure_reports_page.get_conn()
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM UserPools")  # gets all data stored in UserPools table
            row = cursor.fetchone()
            while row is not None:
                if row[0] == pool_id and row[1] == userid_to_remove:  # if pool id and user id to remove match database
                    cursor.close()
                    cursor = conn.cursor()
                    query = "DELETE FROM UserPools WHERE UserID = %s AND PoolID = %s"  # delete relation between user
                    # and pool
                    cursor.execute(query, (userid_to_remove, pool_id))  # execute query
                    conn.commit()
                    cursor.close()
                    conn.close()  # close connection
                    return render_template('accounts.html')
                row = cursor.fetchone()
            conn.close()
            return redirect(url_for('error_page.error_page_func', code="e2"))
        else:
            return redirect(url_for('error_page.error_page_func', code="e1"))

    return render_template('register.html')


@display_pool_page.route('/delete_money_pool', methods=['GET', 'POST'])
def delete_money_pool():
    """
    deletes the pool if the password entered is correct
    :return: displays either accounts.html or register.html depending on the request method and the entered password
    """
    if request.method == "POST":
        pool_id = session.get("entered_pool_id")  # get values from web page
        pool_password = request.form.get("pool_password")
        if check_entered_password(pool_password, pool_id):  # if entered password equals password in database
            try:
                conn = expenditure_reports_page.get_conn()  # get connection
                conn.autocommit = False  # needed for the transaction
                cursor = conn.cursor()

                query = "DELETE FROM UserPools WHERE PoolID = %s"  # first query to update UserPools
                cursor.execute(query, (pool_id,))  # execute first query

                query = "DELETE FROM PoolAccounts WHERE PoolID = %s"  # second query to update PoolAccounts
                cursor.execute(query, (pool_id,))  # execute second query

                conn.commit()  # commit changes
            except mysql.connector.Error as error:
                return redirect(url_for('error_page.error_page_func', code="e7"))
                conn.rollback()  # if there is an error rollback the changes
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()  # close connection
        else:
            return redirect(url_for('error_page.error_page_func', code="e1"))

            return render_template('accounts.html')
    return render_template('register.html')


def get_member_ids(pool_id):
    """
    gets the id's of all members for a specified pool id
    :param pool_id: specified pool id
    :return: all id's for members in a specified pool
    """
    conn = expenditure_reports_page.get_conn()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM UserPools")  # gets all data stored in UserPools table
    row = cursor.fetchone()

    members_ids = ""
    while row is not None:
        if row[0] == pool_id:  # if pool id equals pool id in database
            if len(members_ids) == 0:  # do this for first member id
                members_ids += row[1]
            else:  # do this otherwise
                members_ids += ", " + row[1]
        row = cursor.fetchone()
    cursor.close()
    if len(members_ids) != 0:
        return members_ids  # return comma separated string with all member id's in the pool
    else:
        return redirect(url_for('error_page.error_page_func', code="e2"))


def check_entered_password(entered_password, pool_id):
    """
    hashes a specified password and checks it against the password in the database
    :param entered_password: password entered by user in HTML page
    :param pool_id: pool id for a specified pool
    :return: True if the entered password matches the password in the database
    """
    conn = expenditure_reports_page.get_conn()  # uses existing function for getting a db connection
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM PoolAccounts")  # gets all data stored in PoolAccounts table
    row = cursor.fetchone()
    while row is not None:
        stored_password = row[3]  # get data from database
        salt = row[4]
        pool_pwdhash = hashlib.pbkdf2_hmac('sha512', entered_password.encode('utf-8'), salt.encode('ascii'),
                                           100000)  # hash entered password to check it against stored password
        pool_pwdhash = binascii.hexlify(pool_pwdhash).decode('ascii')
        if row[0] == pool_id and pool_pwdhash == stored_password:  # if pool id and entered password match database
            conn.close()  # close connection
            return True  # return True if password is correct
        row = cursor.fetchone()
    conn.close()  # close connection
    return False  # return False if password is incorrect


def withdraw_and_deposit(account_number, sort_code, amount, withdraw_or_deposit):
    """
    dual-purpose function that can withdraw or deposit from the pool depending on the specified values
    :param account_number: account number entered by user
    :param sort_code: sort code entered by user
    :param amount: deposit/withdraw amount entered by user
    :param withdraw_or_deposit: True if deposit, False if withdraw
    :return: displays manage_pools.html
    """
    int_amount = int(float(amount) * 100)  # convert amount into database format
    pool_id = session.get("entered_pool_id")
    pool_balance = ""
    conn = expenditure_reports_page.get_conn()  # uses existing function for getting a db connection

    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM PoolAccounts")  # gets all data stored in PoolAccounts table
    row = cursor.fetchone()
    while row is not None:
        if row[0] == pool_id:  # if pool id matches database
            pool_balance = row[1]
        row = cursor.fetchone()
    cursor.close()

    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM UserAccounts")  # gets all data stored in UserAccounts table
    row = cursor.fetchone()
    while row is not None:
        if row[0] == str(account_number) and row[1] == str(sort_code):
            if withdraw_or_deposit:  # for depositing into pool
                account_overdraft = row[4]  # get data from database
                account_balance = row[5]
                new_pool_balance = pool_balance + int_amount
                if account_balance + account_overdraft - int_amount > 0:  # checking user can afford the deposit
                    new_account_balance = account_balance - int_amount
            else:  # for withdrawing from pool
                account_balance = row[5]  # get data from database
                new_account_balance = account_balance + int_amount
                if pool_balance > int_amount:  # checking if the user can withdraw the amount from the pool
                    new_pool_balance = pool_balance - int_amount
            account_number = str(account_number)  # convert to string for inserting into database
            sort_code = str(sort_code)
            try:
                conn = expenditure_reports_page.get_conn()  # get connection
                conn.autocommit = False  # needed for transaction
                cursor = conn.cursor()

                query = "UPDATE UserAccounts SET CurrentBalance = %s WHERE AccountNum = %s AND SortCode = %s"  # first
                # query to update UserAccounts
                args = (new_account_balance, account_number, sort_code)
                cursor.execute(query, args)  # execute first query

                query = "UPDATE PoolAccounts SET PoolBalance = %s WHERE PoolID = %s"  # second query to update
                # PoolAccounts
                args = (new_pool_balance, pool_id)
                cursor.execute(query, args)  # execute second query

                conn.commit()  # commit the changes
            except mysql.connector.Error as error:
                return redirect(url_for('error_page.error_page_func', code="e7"))
                conn.rollback()  # if there is an error rollback the changes
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()  # close connection
            return render_template('manage_pools.html')
        row = cursor.fetchone()

    return redirect(url_for('error_page.error_page_func', code="e1"))