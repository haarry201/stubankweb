from flask import Flask, render_template
from register_page import register_page
from account_page import account_page

app = Flask(__name__)
app.register_blueprint(register_page, url_prefix="/register.html")
app.register_blueprint(account_page, url_prefix="/accounts.html")


@app.route('/')
def index_page():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
