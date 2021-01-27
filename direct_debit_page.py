from datetime import datetime, timedelta
import random

from cryptography.fernet import Fernet

from flask import Flask, Blueprint, render_template, request, redirect, url_for
from mysql.connector import MySQLConnection, Error

from controllers.DbConnector import DbConnector

direct_debit = Blueprint('direct_debit', __name__, template_folder='templates')


@direct_debit.route('/', methods=['GET', 'POST'])
def direct_debit_func():
    if request.method == 'POST':
        # requesting form
        account_num_sending = request.form.get("accountNumSending")
        account_num_receiving = request.form.get("accountNumReceiving")
        sort_code_sending = request.form.get("sortCodeSending")
        sort_code_receiving = request.form.get("sortCodeReceiving")
        recurrence_frequency = request.form.get("frequency")
        weekly_recurrence_frequency = request.form.get("weekly")
        every_four_weeks_recurrence_frequency = request.form.get("everyFourWeeks")
        monthly_recurrence_frequency = request.form.get("monthly")
        annual_recurrence_frequency = request.form.get("annually")
        date_of_first_payment = request.form.get("paymentDate")
        reference = request.form.get("reference")
        amount = request.form.get("amount")
        transfer_value = int(float(amount) * 100)

        # Generating random recurring transaction ID
        ran = random.randrange(10 ** 80)
        hex_num = "%016x" % ran
        hex_num = hex_num[:16]
        recurring_transaction_id = hex_num

        # Generating key
        key = Fernet.generate_key()

        # Encode
        id = recurring_transaction_id.encode()  # Convert to bytes
        f = Fernet(key)
        encrypted_id = f.encrypt(id)

        # Decrypt
        f2 = Fernet(key)
        decrypted_id = f2.decrypt(encrypted_id)

        # Decode id
        recurring_transaction_id_secure = decrypted_id.decode()

        # Defining date and time of transaction
        datetime_now = datetime.now()
        transaction_date = datetime_now.strftime("%d-%m-%Y")

        # Defining the payment frequencies
        weekly_payment = timedelta(weeks=1)
        every_four_weeks_payment = timedelta(weeks=4)
        monthly_payment = timedelta(days=30)
        annual_payment = timedelta(days=365)

        # Defining next payment dates
        next_payment_date_weekly = date_of_first_payment + weekly_payment
        next_payment_date_every_four_weeks = date_of_first_payment + every_four_weeks_payment
        next_payment_date_monthly = date_of_first_payment + monthly_payment
        next_payment_date_annual = date_of_first_payment + annual_payment

        # Formatting dates
        next_payment_date_weekly_formatted = next_payment_date_weekly.strftime("%d-%m-%Y")
        next_payment_date_every_four_weeks_formatted = next_payment_date_every_four_weeks.strftime("%d-%m-%Y")
        next_payment_date_monthly_formatted = next_payment_date_monthly.strftime("%d-%m-%Y")
        next_payment_date_annual_formatted = next_payment_date_annual.strftime("%d-%m-%Y")

        # Defining next payment dates based on the recurring payment option selected by user
        if recurrence_frequency == weekly_recurrence_frequency:
            next_payment_date = next_payment_date_weekly_formatted
        elif recurrence_frequency == every_four_weeks_recurrence_frequency:
            next_payment_date = next_payment_date_every_four_weeks_formatted
        elif recurrence_frequency == monthly_recurrence_frequency:
            next_payment_date = next_payment_date_monthly_formatted
        elif recurrence_frequency == annual_recurrence_frequency:
            next_payment_date = next_payment_date_annual_formatted

        # Connecting to database
        try:
            db_connector = DbConnector()
            conn = db_connector.getConn()
            db_connector.closeConn(conn)
            cursor = conn.cursor(buffered=True)

            cursor.execute("SELECT * FROM RecurringTransactions")
            row = cursor.fetchone()

            while row is not None:
                if row[1] == account_num_sending and row[3] == sort_code_sending:
                    account_num_receiving = row[2]
                    recurring_transfer_value = int(row[7])
                    recurring_current_balance = recurring_transfer_value + transfer_value
                    cursor.execute("UPDATE RecurringTransactions SET CurrentBalance = (%s) WHERE"
                                   " AccountNum = (%s) AND SortCode = (%s)",
                                   (recurring_current_balance, account_num_sending, sort_code_sending))
                    balance_change = amount - amount - amount
                    cursor.execute("UPDATE RecurringTransactions SET BalanceChange = (%s) WHERE"
                                   " TransferValue = (%s)",
                                   (balance_change, amount))
                    if next_payment_date == datetime_now:
                        cursor.execute("UPDATE RecurringTransactions SET CurrentBalance = (%s) WHERE"
                                       " AccountNum = (%s) AND SortCode = (%s)",
                                       (recurring_current_balance, account_num_sending, sort_code_sending))
                        cursor.execute("UPDATE RecurringTransactions SET BalanceChange = (%s) WHERE"
                                       " TransferValue = (%s)",
                                       (balance_change, amount))
                    break
                else:
                    row = cursor.fetchone()

            cursor.execute("INSERT INTO RecurringTransactions VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (recurring_transaction_id_secure, account_num_sending, account_num_receiving,
                            sort_code_sending, sort_code_receiving, transaction_date, next_payment_date, amount,
                            balance_change, recurrence_frequency, reference, recurring_current_balance))
            conn.commit()
            cursor.close()
            conn.close()

        except Error as error:
            print(error)
            return redirect(url_for('error_page.error_page_foo', code="e2", src="accounts.html"))

    return render_template('direct_debit.html')
