from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from controllers.DbConnector import DbConnector
from mysql.connector import MySQLConnection, Error
from controllers.DbConnector import DbConnector
from controllers.Offer import Offer
from datetime import datetime

admin_home_page = Blueprint('admin_home_page', __name__, template_folder='templates')


@admin_home_page.route('/')
def admin_home_page_func():
    db_connector = DbConnector()
    conn = db_connector.getConn()
    all_offers = []
    try:
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM Offers")  # gets all data stored in UserInfo table
        result = cursor.fetchall()
        for row in result:
            new_offer = Offer(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            all_offers.append(new_offer)
    except Error as e:
        print(e)
        return redirect(url_for('error_page.error_page_foo', code="e2", src="index.html"))

    finally:
        cursor.close()
        conn.close()
    return render_template('/admin_pages/admin_home.html')