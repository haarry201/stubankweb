import random, string
import hashlib, binascii, os

from flask import Blueprint, render_template, request, session, redirect, url_for
from controllers.DbConnector import DbConnector
from mysql.connector import Error

from controllers.TwoFactorAuthentication import TwoFactorAuthentication

'''
File name: register_page.py
Author: Rhys Minchin
Credits: Rhys Minchin
Date created: 08/12/2020
Date last modified: 25/01/2021
Python version: 3.7
Purpose: This provides the back-end for the register page. It gets the information from the registration form and 
         processes it in order to determine what happens next. If there is a registration error, the user is forwarded 
         to the error page and an appropriate error message is given. If not, the user is forwarded to the accounts
         homepage.
'''

register_page = Blueprint('register_page', __name__, template_folder='templates')


@register_page.route('/', methods=['GET', 'POST'])
def register_page_func():
    if request.method == "POST":
        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        first_line_of_address = request.form.get("first_line_of_address")
        second_line_of_address = request.form.get("second_line_of_address")
        postcode = request.form.get("postcode")
        security_question = request.form.get("security_question")
        security_answer = request.form.get("security_answer")  # gets all input information from registration form
        all_info = first_name.lower() + last_name.lower() + email.lower() + password.lower() + \
                   first_line_of_address.lower() + second_line_of_address.lower() + postcode.lower() + \
                    security_question.lower() + security_answer.lower()
        cont = check_input(all_info)
        if cont:
            user_role = "User"
            if first_name == '' or last_name == '' or email == '' or password == '' or first_line_of_address == '' or second_line_of_address == '' or postcode == '' or security_question == '--' or security_answer == '':
                return redirect(url_for('error_page.error_page_func', code="e3"))
            elif len(password) < 6:
                return redirect(url_for('error_page.error_page_func', code="e4"))
                # redirects to error page with appropriate error message if there is an error
            else:
                db_connector = DbConnector()
                conn = db_connector.getConn()
                cursor = conn.cursor(buffered=True)
                cursor.execute("SELECT EmailAddress FROM UserInfo WHERE EmailAddress = (%s)", (email,))  # checks if email already exists
                result = cursor.fetchall()
                for row in result:
                    print(row)
                    if row[0].lower() == email.lower():
                        #User with email already exists
                        return redirect(url_for('error_page.error_page_func', code="e10"))
                user_id = ''.join(
                    random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
                # generate random 16 digit hex to use as primary key for UserInfo table
                two_fa_manager = TwoFactorAuthentication()
                otp_secret_key = two_fa_manager.get_random_secret_key()            # generate one-time password
                salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')  # generate salt for password hashing
                pwd = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
                pwdhash = binascii.hexlify(pwd)  # hash password using salt, this is what is stored in database
                using_2fa = 0

                query = "INSERT INTO UserInfo " \
                        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                args = (user_id, email, pwdhash, salt, otp_secret_key, first_name, last_name, first_line_of_address,
                        second_line_of_address, postcode, security_question, security_answer, user_role, using_2fa)

                try:
                    db_connector = DbConnector()
                    conn = db_connector.getConn()
                    cursor = conn.cursor()
                    cursor.execute(query, args)  # inserts data into database
                    conn.commit()  # commits changes
                    cursor.close()
                    conn.close()
                    session['needs_auth'] = False
                    session['secret_auth_key'] = otp_secret_key
                    session['two_factor_enabled'] = False
                    session['email'] = email
                    session['name'] = first_name
                    session['user_role'] = user_role
                    session['user_id'] = user_id
                    # initialises session attributes
                except Error as error:
                    print(error)
                    return redirect(url_for('error_page.error_page_func', code="e2"))  # sent to error page with appropriate message
                return redirect(url_for('account_page.account_page_func'))  # user logged in and sent to homepage
        else:
            return redirect(url_for('error_page.error_page_func', code="e14"))  # if bad input detected, input blocked
    return render_template('register.html')

def check_input(data):
    bad_words = ["insert", "into", "where", "script", "delete", "input", "select", "from"]
    chars = set('<>!{}*')
    if any((c in chars) for c in data):
        return False  # if any bad characters, returns False
    else:
        data_words = data.split(" ")
        for d in data_words:
            if d in bad_words:
                return False  # if any SQL keywords detected, returns False

    return True  # if no bad input detected, returns True