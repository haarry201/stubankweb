from flask import Flask, Blueprint, render_template,request
from mysql.connector import MySQLConnection, Error
from controllers.DbConnector import DbConnector
from controllers.PasswordManager import PasswordManager

direct_debit = Blueprint('direct_debit', __name__, template_folder='templates')


@direct_debit.route('/', methods=['GET', 'POST'])
def direct_debit_func():
    return render_template('direct_debit.html')