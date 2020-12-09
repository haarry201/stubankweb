from flask import Flask, render_template, request
from register_page import register_page
from account_page import account_page
from login_page import login_page
from controllers.DbConnector import DbConnector
from mysql.connector import MySQLConnection, Error
import random, string
import hashlib, binascii, os

app = Flask(__name__)
app.register_blueprint(login_page, url_prefix="/login.html")
app.register_blueprint(register_page, url_prefix="/register.html")
app.register_blueprint(account_page, url_prefix="/accounts.html")


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/create_account', methods=["POST"])
def account_validation():
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

            db_connector = DbConnector()
            conn = db_connector.getConn()
            db_connector.closeConn(conn)
            cursor = conn.cursor()
            cursor.execute(query, args)
            conn.commit()
            cursor.close()
            conn.close()

            return render_template("accounts.html", user=first_name)


@app.route('/login', methods=["POST"])
def login_check():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        security_question = request.form.get("security_question")
        security_answer = request.form.get("security_answer")
        try:
            db_connector = DbConnector()
            conn = db_connector.getConn()
            db_connector.closeConn(conn)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM UserInfo")

            row = cursor.fetchone()

            while row is not None:
                if email == row[1] and (check_password(password, row)):
                    return render_template("accounts.html", user="Success")
                else:
                    row = cursor.fetchone()

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()

        return render_template("accounts.html", user="Failure")


def check_password(password, data):
    pwd = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), data[3], 100000)
    pwdhash = binascii.hexlify(pwd).decode('ascii')
    print(pwdhash + " : " + data[2])
    print(str(len(pwdhash)) + " : " + str(len(data[2])))
    return pwdhash == data[2]


if __name__ == '__main__':
    app.run()
