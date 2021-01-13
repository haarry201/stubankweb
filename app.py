from flask import Flask, render_template, request, session
from manage_pools import manage_pools
from register_page import register_page
from account_page import account_page
from login_page import login_page
from bank_acc_application_page import bank_acc_application_page
from bank_transfer_page import bank_transfer_page
from offer_page import offer_page
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()  # generates secret key for unique session id
app.register_blueprint(login_page, url_prefix="/login.html")
app.register_blueprint(register_page, url_prefix="/register.html")
app.register_blueprint(account_page, url_prefix="/accounts.html")
app.register_blueprint(bank_acc_application_page, url_prefix="/bank_application.html")
app.register_blueprint(bank_transfer_page, url_prefix="/bank_transfer.html")
app.register_blueprint(manage_pools, url_prefix="/manage_pools.html")
app.register_blueprint(offer_page, url_prefix="/offers.html")


@app.route('/')
def index_page():
    if 'name' in session:
        session.pop('name')  # removes stored session attributes as logging out
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
