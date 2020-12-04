from flask import Flask, render_template
from account_page import account_page

app = Flask(__name__)
app.register_blueprint(account_page)

@app.route('/')
def index_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
