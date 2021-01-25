from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from controllers.DbConnector import DbConnector
from mysql.connector import MySQLConnection, Error
from controllers.DbConnector import DbConnector
from controllers.Offer import Offer
from datetime import datetime

admin_home_page = Blueprint('admin_home_page', __name__, template_folder='templates')


@admin_home_page.route('/')
def admin_home_page_func():
    try:
        user_role = session.get('user_role')
        print(user_role)
    except Error as e:
        print("error, no session key set")
    if user_role == ("Admin" or "Offer_Admin"):
        return render_template('/admin_pages/admin_home.html')
    else:
        return redirect(url_for('error_page.error_page_foo', code="e6", src="index.html"))
