import datetime
import pytz
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
        reference = request.form.get("reference")
        amount = request.form.get("amount")
        transfer_value = int(float(amount) * 100)

        # Generating random recurring transaction ID
        ran = random.randrange(10 ** 80)
        hex_num = "%016x" % ran
        hex_num = hex_num[:16]
        recurring_transaction_id = hex_num

        # Defining timezone
        tz_uk = pytz.timezone('Europe/London')

        # Defining date and time of transaction
        datetime_uk = datetime.datetime.now(tz_uk)
        datetime_formatted = datetime_uk.strftime("%d-%m-%Y")

        # Defining the payment frequencies
        weekly_payment = datetime.timedelta(weeks=1)
        every_four_weeks_payment = datetime.timedelta(weeks=4)
        monthly_payment = datetime.timedelta(days=30)
        annual_payment = datetime.timedelta(days=365)

        try:
            db_connector = DbConnector()
            conn = db_connector.getConn()
            db_connector.closeConn(conn)
            cursor = conn.cursor(buffered=True)

            cursor.execute("SELECT * FROM UserInfo")
            row = cursor.fetchone()
            while row is not None:
                if row[1] == email:
                    user_id = row[0]
                    break
                else:
                    row = cursor.fetchone()

            cursor.execute("SELECT * FROM UserAccounts")
            row = cursor.fetchone()

            while row is not None:
                if row[2] == user_id and row[3] == account_type_id:
                    current_value = int(row[5])
                    new_value = current_value - transfer_value
                    cursor.execute("UPDATE UserAccounts SET CurrentBalance = (%s) WHERE UserID = (%s) AND"
                                   " AccountTypeID = (%s)", (new_value, user_id, account_type_id))
                    break

                else:
                    row = cursor.fetchone()

            cursor.execute("SELECT * FROM RecurringTransactions")
            row = cursor.fetchone()

            while row is not None:
                if row[1] == account_num_sending and row[3] == sort_code_sending:
                    account_num_receiving = row[2]
                    transferee_value_current = int(row[5])
                    new_transferee_value = transferee_value_current + transfer_value
                    cursor.execute("UPDATE UserAccounts SET CurrentBalance = (%s) WHERE"
                                   " AccountNum = (%s) AND SortCode = (%s)",
                                   (new_transferee_value, account_num_sending, sort_code_sending))
                    break

                else:
                    row = cursor.fetchone()

            cursor.execute("INSERT INTO RecurringTransactions VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                           (recurring_transaction_id, account_num_sending, account_num_receiving, sort_code_sending,
                            sort_code_receiving, datetime_formatted, recurrence_frequency, reference))
            conn.commit()
            cursor.close()
            conn.close()

        except Error as error:
            print(error)
            return redirect(url_for('error_page.error_page_foo', code="e2", src="accounts.html"))

    return render_template('direct_debit.html')
