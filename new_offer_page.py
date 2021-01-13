from flask import Flask, Blueprint, render_template, request, session
from mysql.connector import MySQLConnection, Error
from controllers.DbConnector import DbConnector
from controllers.Offer import Offer

new_offer_page = Blueprint('new_offer_page', __name__, template_folder='templates')


@new_offer_page.route('/')
def new_offer_page_func():
    db_connector = DbConnector()
    conn = db_connector.getConn()
    if request.method == "POST":

        print("hello world")
    offer = Offer("Enter this code in the promotional code area during checkout in order to benefit from "
                            "35% Off purchases made via the adidas App.",
                   "Adidas",
                   "https://www.myunidays.com/GB/en-GB/partners/adidas35/access/online",
                   "https://images.unidays.world/i/18f8fbd4-b793-4e4c-9e84-b0c98cc0a136?format=raw",
                   "10/12/2020",
                   "20/12/2020",
                   "Unidays",
                   "35% Off"
            )
    all_offers = []
    all_offers.append(offer)
    return render_template('new_offer.html', title='Home', all_offers=all_offers)