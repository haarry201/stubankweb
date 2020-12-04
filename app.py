from flask import Flask
from newWeb import simple_page

app = Flask(__name__)
app.register_blueprint(simple_page)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
