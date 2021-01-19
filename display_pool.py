from flask import Flask, Blueprint, render_template,request
from mysql.connector import MySQLConnection, Error
from controllers.DbConnector import DbConnector
from controllers.PasswordManager import PasswordManager

display_pool = Blueprint('display_pool', __name__, template_folder='templates')


@display_pool.route('/', methods=['GET', 'POST'])
def display_pool_func():

    return render_template('display_pool.html')