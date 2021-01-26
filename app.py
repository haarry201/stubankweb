from flask import Flask, render_template, session, redirect, url_for
from display_pool import display_pool
from manage_pools import manage_pools
from register_page import register_page
from account_page import account_page
from login_page import login_page
from bank_acc_application_page import bank_acc_application_page
from bank_transfer_page import bank_transfer_page
from expenditure_reports_page import expenditure_reports_page
from extra_info_page import extra_info_page
from error_page import error_page
from offer_page import offer_page
from manage_offers_page import manage_offers_page
from card_payment_page import card_payment_page
from manage_cards_page import manage_cards_page
from apply_new_card_page import apply_new_card_page
from admin_new_card_page import admin_new_card_page
from two_factor_auth_set_up_page import two_factor_auth_set_up_page
from two_factor_auth_verify_page import two_factor_auth_verify_page
from admin_home_page import admin_home_page
from account_settings_page import account_settings_page
from bank_transfer_internal_page import bank_transfer_internal_page
from stories_page import stories_page

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()  # generates secret key for unique session id
app.register_blueprint(login_page, url_prefix="/login.html")
app.register_blueprint(register_page, url_prefix="/register.html")
app.register_blueprint(account_page, url_prefix="/accounts.html")
app.register_blueprint(bank_acc_application_page, url_prefix="/bank_acc_application_page.html")
app.register_blueprint(bank_transfer_page, url_prefix="/bank_transfer.html")
app.register_blueprint(manage_pools, url_prefix="/manage_pools.html")
app.register_blueprint(display_pool, url_prefix="/display_pool.html")
app.register_blueprint(expenditure_reports_page, url_prefix="/reports/")
app.register_blueprint(extra_info_page, url_prefix="/extrainfo/")
app.register_blueprint(error_page, url_prefix="/error.html")
app.register_blueprint(offer_page, url_prefix="/offers.html")
app.register_blueprint(manage_offers_page, url_prefix="/manage_offers.html")
app.register_blueprint(card_payment_page, url_prefix="/card_payment.html")
app.register_blueprint(manage_cards_page, url_prefix="/manage_cards_page.html")
app.register_blueprint(apply_new_card_page, url_prefix="/apply_new_card_page.html")
app.register_blueprint(admin_new_card_page, url_prefix="/new_card.html")
app.register_blueprint(two_factor_auth_verify_page, url_prefix="/two_factor_verification.html")
app.register_blueprint(two_factor_auth_set_up_page, url_prefix="/two_factor_set_up.html")
app.register_blueprint(admin_home_page, url_prefix="/admin_home.html")
app.register_blueprint(account_settings_page, url_prefix="/account_settings.html")
app.register_blueprint(bank_transfer_internal_page, url_prefix="/bank_transfer_internal.html")
app.register_blueprint(stories_page, url_prefix="/stories_page.html")





@app.route('/')
def index_page():
    if 'name' in session:
        session.pop('name')  # removes stored session attributes as logging out
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('error_page.error_page_func',code="e5", src="index.html"))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
