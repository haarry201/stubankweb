import datetime
import random
import mysql.connector

from flask import Flask, Blueprint, render_template, request, redirect, url_for
from mysql.connector import MySQLConnection, Error
from controllers.DbConnector import DbConnector
from controllers.PasswordManager import PasswordManager

direct_debit = Blueprint('direct_debit', __name__, template_folder='templates')


@direct_debit.route('/', methods=['GET', 'POST'])
def direct_debit_func():
    if request.method == 'POST':
        # requesting form
        account_name = request.form.get("accountName")
        account_type = request.form.get("accountType")
        if account_type == "Student Current Account":
            account_type_id = '123'
        if account_type == "Savings Account":
            account_type_id = '100'
        email = request.form.get("email")
        account_num_sending = request.form.get("accountNumSending")
        account_num_receiving = request.form.get("accountNumReceiving")
        sort_code_sending = request.form.get("sortCodeSending")
        sort_code_receiving = request.form.get("sortCodeReceiving")
        recurrence_frequency = request.form.get("frequency")
        amount = request.form.get("amount")
        transfer_value = int(float(amount) * 100)

        # Account number and sort code for the card payment account for demonstration
        account_num = "00213181"
        sort_code = "286376"

        # Generating random recurring transaction ID
        ran = random.randrange(10 ** 80)
        hex_num = "%016x" % ran
        hex_num = hex_num[:16]
        recurring_transaction_id = hex_num

        # Defining date and time of transaction
        now = datetime.datetime.now()
        datetime_formatted = now.strftime("%d-%m-%Y")

        try:
            db_connector = DbConnector()
            conn = db_connector.getConn()
            db_connector.closeConn(conn)
            cursor = conn.cursor(buffered=True)

            cursor.execute("INSERT INTO RecurringTransactions VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                           (recurring_transaction_id, account_num_sending, account_num_receiving, sort_code_sending,
                            sort_code_receiving, datetime_formatted, recurrence_frequency,  ))


        except Error as error:
            print(error)
            return redirect(url_for('error_page.error_page_foo', code="e2", src="accounts.html"))

    return render_template('direct_debit.html')
