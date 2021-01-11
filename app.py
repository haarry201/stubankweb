from flask import Flask, render_template, request
from manage_pools import manage_pools
from register_page import register_page
from account_page import account_page
from login_page import login_page
from bank_acc_application_page import bank_acc_application_page

app = Flask(__name__)
app.register_blueprint(login_page, url_prefix="/login.html")
app.register_blueprint(register_page, url_prefix="/register.html")
app.register_blueprint(account_page, url_prefix="/accounts.html")
app.register_blueprint(bank_acc_application_page, url_prefix="/bank_application.html")
app.register_blueprint(manage_pools, url_prefix="/manage_pools.html")


@app.route('/')
def index_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
