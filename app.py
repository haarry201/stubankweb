from flask import Flask, render_template, session
from register_page import register_page
from account_page import account_page
from login_page import login_page
from expenditure_reports import expenditure_reports
import secrets
secret_key = secrets.token_hex(16)


app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key  # generates secret key for unique session id
app.register_blueprint(login_page, url_prefix="/login.html")
app.register_blueprint(register_page, url_prefix="/register.html")
app.register_blueprint(account_page, url_prefix="/accounts.html")
app.register_blueprint(expenditure_reports, url_prefix="/reports/")


@app.route('/')
def index_page():
    if 'name' in session:
        session.pop('name')  # removes stored session attributes as logging out
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
