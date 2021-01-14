from flask import Flask, Blueprint, render_template, request, session
from mysql.connector import MySQLConnection, Error
from controllers.DbConnector import DbConnector
from controllers.Offer import Offer
from datetime import datetime

new_offer_page = Blueprint('new_offer_page', __name__, template_folder='templates')


@new_offer_page.route('/')
def new_offer_page_func():
    db_connector = DbConnector()
    conn = db_connector.getConn()
    if request.method == "POST":
        print("hello world")
        offer_img_url = request.form.get("img-url")
        offer_origin_site = request.form.get("offer-origin-site")
        offer_title = request.form.get("offer-title")
        offer_add_date = datetime.today().strftime('%d-%m-%Y-')
        offer_exp_date = request.form.get("offer-exp-date")
        offer_description = request.form.get("offer-description")
        offer_url = request.form.get("offer-url")
        new_offer = Offer(offer_description, offer_url, offer_img_url, offer_add_date, offer_exp_date,
                          offer_origin_site, offer_title)
        #Add new offer to DB
    offer = Offer("Enter this code in the promotional code area during checkout in order to benefit from "
                  "35% Off purchases made via the adidas App.",
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
