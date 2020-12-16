from flask import Flask, Blueprint, render_template,request
from controllers.DbConnector import DbConnector
from random import *

bank_acc_application_page = Blueprint('bank_acc_application_page', __name__, template_folder='templates')


@bank_acc_application_page.route('/<page>', methods=['GET', 'POST'])
def bank_application(page):
    if request.method == 'POST':
        account_type = request.form.get("account type")
        email = request.form.get("email")
        account_id = ''.join(["{}".format(randint(0, 9)) for num in range(0, 8)])
        sort_code = ''.join(["{}".format(randint(0, 9)) for num in range(0, 6)])
        agreed_overdraft = 1500
        current_balance = 0
        db_connector = DbConnector()
        conn = db_connector.getConn()
        db_connector.closeConn(conn)
        cursor = conn.cursor()

        cursor.execute ("SELECT * FROM UserInfo")
        row = cursor.fetchone()
        if row[1] == email:
                user_id = row[0]

        cursor.execute("INSERT INTO UserAccounts VALUES (%s, %s, %s, %s, %s, %s)", (account_id, sort_code,\
                            user_id, account_type, agreed_overdraft, current_balance))

        conn.commit()
        cursor.close()
        conn.close()





    return render_template('bank_application.html')