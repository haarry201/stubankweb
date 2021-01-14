from flask import Flask, Blueprint, render_template, request, session
from controllers.DbConnector import DbConnector
from mysql.connector import MySQLConnection, Error
from controllers.DbConnector import DbConnector
from controllers.Offer import Offer
from datetime import datetime

offer_page = Blueprint('offer_page', __name__, template_folder='templates')


@offer_page.route('/')
def offer_page_func():
    db_connector = DbConnector()
    conn = db_connector.getConn()
    all_offers = []
    try:
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM Offers")  # gets all data stored in UserInfo table

        result = cursor.fetchall()
        for row in result:
            print(row)
            print(row[0])
            new_offer = Offer(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            all_offers.append(new_offer)
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
    return render_template('offers.html', title='Home', all_offers=all_offers)