import random, string
import hashlib, binascii, os

from flask import Flask, Blueprint, render_template, request, session
from controllers.DbConnector import DbConnector
from mysql.connector import MySQLConnection, Error

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
        security_answer = request.form.get("security_answer")
        if first_name == '' or last_name == '' or email == '' or password == '' or first_line_of_address == '' or second_line_of_address == '' or postcode == '' or security_question == '--' or security_answer == '':
            return render_template("error.html", msg="Please ensure that all text boxes are filled in",
                                   src="register.html")
        elif len(password) < 6:
            return render_template("error.html", msg="Password is too short, please try another one",
                                   src="register.html")
        else:
            user_id = ''.join(
                random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
            # generate random 16 digit hex to use as primary key for UserInfo table
            otp_secret_key = random.randint(10000000, 99999999)  # generate one-time password
            salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')  # generate salt for password hashing
            pwd = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
            pwdhash = binascii.hexlify(pwd)  # hash password using salt, this is what is stored in database

            query = "INSERT INTO UserInfo " \
                    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            args = (user_id, email, pwdhash, salt, otp_secret_key, first_name, last_name, first_line_of_address,
                    second_line_of_address, postcode, security_question, security_answer)

            try:
                db_connector = DbConnector()
                conn = db_connector.getConn()
                db_connector.closeConn(conn)
                cursor = conn.cursor()
                cursor.execute(query, args)
                conn.commit()
                cursor.close()
                conn.close()
                session['name'] = first_name
            except Error as error:
                print(error)
                return render_template("error.html", msg="An unexpected error occurred, please try again",
                                       src="register.html")

            return render_template("accounts.html", user=session['name'])
    return render_template('register.html')