from flask import Flask, render_template, request, session, redirect, url_for
from display_pool import display_pool
from manage_pools import manage_pools
from register_page import register_page
from account_page import account_page
from login_page import login_page
from bank_acc_application_page import bank_acc_application_page
from bank_transfer_page import bank_transfer_page
from expenditure_reports import expenditure_reports
from extra_info import extra_info
from error_page import error_page
from offer_page import offer_page
from new_offer_page import new_offer_page
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()  # generates secret key for unique session id
app.register_blueprint(login_page, url_prefix="/login.html")
app.register_blueprint(register_page, url_prefix="/register.html")
app.register_blueprint(account_page, url_prefix="/accounts.html")
app.register_blueprint(bank_acc_application_page, url_prefix="/bank_application.html")
app.register_blueprint(bank_transfer_page, url_prefix="/bank_transfer.html")
app.register_blueprint(manage_pools, url_prefix="/manage_pools.html")
app.register_blueprint(display_pool, url_prefix="/display_pool.html")
app.register_blueprint(expenditure_reports, url_prefix="/reports/")
app.register_blueprint(extra_info, url_prefix="/extrainfo/")
app.register_blueprint(error_page, url_prefix="/error.html")
app.register_blueprint(offer_page, url_prefix="/offers.html")
app.register_blueprint(new_offer_page, url_prefix="/new_offer.html")



@app.route('/')
def index_page():
    if 'name' in session:
        session.pop('name')  # removes stored session attributes as logging out
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('error_page.error_page_foo',code="e5", src="index.html"))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
