from flask import Flask, Blueprint, render_template, request, session
from mysql.connector import MySQLConnection, Error
from controllers.DbConnector import DbConnector
from controllers.Offer import Offer
from datetime import datetime

new_offer_page = Blueprint('new_offer_page', __name__, template_folder='templates')


@new_offer_page.route('/', methods=['GET', 'POST'])
def new_offer_page_func():
    db_connector = DbConnector()
    conn = db_connector.getConn()
    if request.method == "POST":
        offer_img_url = request.form.get("img-url")
        offer_origin_site = request.form.get("offer-origin-site")
        offer_title = request.form.get("offer-title")
        offer_add_date = datetime.today().strftime('%Y-%m-%d')
        offer_exp_date = request.form.get("offer-exp-date")
        offer_description = request.form.get("offer-description")
        offer_url = request.form.get("offer-url")
        print(offer_description)
        new_offer = Offer(offer_description, offer_url, offer_img_url, offer_add_date, offer_exp_date,
                          offer_origin_site, offer_title)
        #Add new offer to DB
        query = "INSERT INTO Offers(OfferDescription, OfferURL, OfferImageURL, OfferAddDate, OfferExpiryDate, OfferOriginSite, OfferTitle) " \
                "VALUES(%s, %s, %s, %s, %s, %s, %s)"
        args = (offer_description, offer_url, offer_img_url, offer_add_date, offer_exp_date, offer_origin_site, offer_title)

        try:
            db_connector = DbConnector()
            conn = db_connector.getConn()
            cursor = conn.cursor()
            cursor.execute(query, args)
            conn.commit()
            cursor.close()
        except Error as error:
            print(error)
            return render_template("error.html", msg="An unexpected error occurred, please try again",
                                   src="register.html")
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

    return render_template('new_offer.html', title='Home', all_offers=all_offers)
