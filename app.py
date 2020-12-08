from flask import Flask, render_template, request
from register_page import register_page
from account_page import account_page
from login_page import login_page

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
            return render_template("error.html", msg="Please ensure that all text boxes are filled in", src="register.html")
        else:
            return render_template("accounts.html")


@app.route('/login', methods=["POST"])
def login_check():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        security_question = request.form.get("security_question")
        security_answer = request.form.get("security_answer")
        if email == '' or password == '' or security_question == '--' or security_answer == '':
            return render_template("error.html", msg="Please ensure that all text boxes are filled in", src="login.html")

if __name__ == '__main__':
    app.run()
