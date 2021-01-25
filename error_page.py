from flask import Flask, Blueprint, render_template, session, redirect, url_for, request
from controllers.DbConnector import DbConnector

error_page = Blueprint('error_page', __name__, template_folder='templates')


@error_page.route('/')
def error_page_foo():
    print()
    code = "e5"
    src = "index.html"
    try:
        code = request.args['code']
        src = request.args['src']
    except:
        print()
    error_codes = {"e1": "These login credentials do not match an existing user, please try again",
                   "e2": "An unexpected error occurred, please try again",
                   "e3": "Please ensure that all text boxes are filled in",
                   "e4": "Password is too short, please try another one",
                   "e5": "404 Not Found",
                   "e6": "Unauthorised Access",
                   "e7": "There appears to be an error with this transaction, your account has been locked ",
                   "e8": "Verification Error!",
                   "e9": "Error, Email address already in use",
                   "e10": "Error, this account appears to be in use"
                   }
    return render_template('error.html', error_codes=error_codes,code=code, src=src)
