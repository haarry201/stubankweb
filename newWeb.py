from flask import Flask, Blueprint

simple_page = Blueprint('simple_page', __name__, template_folder='templates')
@simple_page.route('/<page>')
def show(page):
    return 'Hello World!'