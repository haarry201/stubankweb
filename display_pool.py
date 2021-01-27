import binascii
import hashlib

import mysql

import expenditure_reports_page
from flask import Blueprint, render_template, request, session
from manage_pools import get_member_firstnames

display_pool = Blueprint('display_pool', __name__, template_folder='templates')


@display_pool.route('/', methods=['GET', 'POST'])
def display_pool_func():
    if not session.get("entered_pool_id"):
        entered_pool_id = request.form.get("pool_to_view")
        session["entered_pool_id"] = entered_pool_id
    conn = expenditure_reports_page.get_conn()  # uses existing function for getting a db connection
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM PoolAccounts")  # gets all data stored in UserPools table
    row = cursor.fetchone()

    pool = []
    while row is not None:
        if row[0] == session['entered_pool_id']:
            members_firstnames = get_member_firstnames(row[0])
            member_ids = get_member_ids(row[0])
            pool_balance = row[1]
            pool_name = row[2]
            owner = row[5]
            date_created = row[6]
            pool_join_code = row[7]
            pool.append(pool_name + "," + session.get("entered_pool_id") + "," + str(
                pool_balance) + "," + members_firstnames + "," + member_ids + "," + date_created + "," + owner)
        row = cursor.fetchone()
    if len(pool) == 0:
        return render_template('register.html')
    return render_template('display_pool.html', pool=pool, pool_name=pool_name, pool_join_code=pool_join_code)


@display_pool.route('/deposit_money_pool', methods=['GET', 'POST'])
def deposit_money_pool():
    if request.method == "POST":
        return render_template('display_pool.html')
    return render_template('register.html')


@display_pool.route('/withdraw_money_pool', methods=['GET', 'POST'])
def withdraw_money_pool():
    if request.method == "POST":
        return render_template('display_pool.html')
    return render_template('register.html')


@display_pool.route('/leave_money_pool', methods=['GET', 'POST'])
def leave_money_pool():
    if request.method == "POST":
        conn = expenditure_reports_page.get_conn()
        cursor = conn.cursor()
        query = "DELETE FROM UserPools WHERE UserID = %s AND PoolID = %s"
        user_id = session.get("user_id")
        pool_id = session.get("entered_pool_id")
        cursor.execute(query, (user_id, pool_id))
        conn.commit()
        cursor.close()
        conn.close()

        return render_template('manage_pools.html')
    return render_template('register.html')


@display_pool.route('/add_user_to_money_pool', methods=['GET', 'POST'])
def add_user_to_money_pool():
    if request.method == "POST":
        return render_template('display_pool.html')
    return render_template('register.html')


@display_pool.route('/remove_user_from_money_pool', methods=['GET', 'POST'])
def remove_user_from_money_pool():
    if request.method == "POST":
        entered_pool_password = request.form.get("pool_password")
        userid_to_remove = request.form.get("id_to_remove")
        pool_id = session.get("entered_pool_id")
        conn = expenditure_reports_page.get_conn()  # uses existing function for getting a db connection
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM PoolAccounts")  # gets all data stored in UserPools table
        row = cursor.fetchone()
        while row is not None:
            stored_password = row[3]
            salt = row[4]

            pool_pwdhash = hashlib.pbkdf2_hmac('sha512', entered_pool_password.encode('utf-8'), salt.encode('ascii'),
                                               100000)
            pool_pwdhash = binascii.hexlify(pool_pwdhash).decode('ascii')

            if row[0] == pool_id and pool_pwdhash == stored_password:
                cursor.close()
                cursor = conn.cursor(buffered=True)
                cursor.execute("SELECT * FROM UserPools")  # gets all data stored in UserPools table
                row = cursor.fetchone()
                while row is not None:
                    if row[0] == pool_id and row[1] == userid_to_remove:
                        cursor.close()
                        cursor = conn.cursor()
                        query = "DELETE FROM UserPools WHERE UserID = %s AND PoolID = %s"
                        cursor.execute(query, (userid_to_remove, pool_id))
                        conn.commit()
                        cursor.close()
                        conn.close()
                    row = cursor.fetchone()
                conn.close()
            row = cursor.fetchone()

        return render_template('accounts.html')
    return render_template('register.html')


@display_pool.route('/delete_money_pool', methods=['GET', 'POST'])
def delete_money_pool():
    if request.method == "POST":
        pool_id = session.get("entered_pool_id")
        try:
            conn = expenditure_reports_page.get_conn()
            conn.autocommit = False
            cursor = conn.cursor()

            query = "DELETE FROM UserPools WHERE PoolID = %s"
            cursor.execute(query, (pool_id,))

            query = "DELETE FROM PoolAccounts WHERE PoolID = %s"
            cursor.execute(query, (pool_id,))

            conn.commit()
        except mysql.connector.Error as error:
            print("Failed to delete pool: {}".format(error))
            conn.rollback()
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        return render_template('accounts.html')
    return render_template('register.html')


def get_member_ids(pool_id):
    conn = expenditure_reports_page.get_conn()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM UserPools")  # gets all data stored in UserPools table
    row = cursor.fetchone()

    members_ids = ""
    while row is not None:
        if row[0] == pool_id:
            if len(members_ids) == 0:
                members_ids += row[1]
            else:
                members_ids += ", " + row[1]
        row = cursor.fetchone()
    cursor.close()
    return members_ids
