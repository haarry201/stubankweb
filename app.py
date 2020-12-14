from flask import Flask, render_template, request
from register_page import register_page
from account_page import account_page
from login_page import login_page
from admin_new_card import admin_new_card_page

app = Flask(__name__)
app.register_blueprint(login_page, url_prefix="/login.html")
app.register_blueprint(register_page, url_prefix="/register.html")
app.register_blueprint(account_page, url_prefix="/accounts.html")
app.register_blueprint(admin_new_card_page, url_prefix="/new_card.html")


@app.route('/')
def index_page():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", msg = e)

if __name__ == '__main__':
    app.run()
