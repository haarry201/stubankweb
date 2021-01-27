from flask import Blueprint, render_template, request

'''
File name: error.py
Author: Rhys Minchin
Credits: Rhys Minchin, Jacob Scase
Date created: 10/12/2020
Date last modified: 25/01/2021
Python version: 3.7
Purpose: Any error that occurs throughout the running of the program will redirect the user here. An appropriate error
         message will show and the user can then be returned to where they were so they can try again.
'''

error_page = Blueprint('error_page', __name__, template_folder='templates')


@error_page.route('/')
def error_page_func():
    print()
    code = "e5"
    src = "index.html"
    try:
        code = request.args['code']
        src = request.args['src']  # gets information from error request to show user correct error information
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
                   "e10": "Error, this account appears to be in use",
                   "e11": "Error, you do not have the balance to process this transaction"
                   }  # error codes and description of what caused the error
    return render_template('error.html', error_codes=error_codes, code=code, src=src)
