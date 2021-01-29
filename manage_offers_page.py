from flask import Blueprint, render_template, request, session, redirect, url_for
from mysql.connector import Error
from controllers.DbConnector import DbConnector
from classes.Offer import Offer
from datetime import datetime

'''
File name: manage_offers_page.py
Author: Jacob Scase
Credits: Jacob Scase
Date created: 25/12/2020
Date last modified: 25/01/2021
Python version: 3.7
Purpose: Back-end file for allowing admins to add, and remove offers 
'''

manage_offers_page = Blueprint('manage_offers_page', __name__, template_folder='templates')


@manage_offers_page.route('/', methods=['GET', 'POST'])
def manage_offers_page_func():
    try:
        # redirects user appropriately based on 2FA status, or whether they are an admin or not
        if 'user_id' in session:
            if session['needs_auth'] == True:
                return redirect(url_for('login_page.login_page_func'))
            elif session['user_role'] == 'Admin':
                user_id = session['user_id']
                user_role = session['user_role']
            else:
                return redirect(url_for('admin_home_page.admin_home_page_func'))
        else:
            return redirect(url_for('login_page.login_page_func'))
    except:
        return redirect(url_for('login_page.login_page_func'))
    db_connector = DbConnector()
    conn = db_connector.getConn()
    if request.method == "POST":
        if 'delete' in request.form:
            # Deleting offer
            offer_id = int(request.form.get('delete'))
            cursor = conn.cursor()
            # cursor.execute("DELETE * FROM Offers WHERE OfferID = %s", offer_id)
            cursor.execute("DELETE FROM Offers WHERE OfferID = %s",(offer_id,))
            conn.commit()
            cursor.close()
        else:
            #Adding offer
            offer_img_url = request.form.get("img-url")
            offer_origin_site = request.form.get("offer-origin-site")
            offer_title = request.form.get("offer-title")
            offer_add_date = datetime.today().strftime('%Y-%m-%d')
            offer_exp_date = request.form.get("offer-exp-date")
            offer_description = request.form.get("offer-description")
            offer_url = request.form.get("offer-url")
            # Add new offer to DB
            query = "INSERT INTO Offers(OfferDescription, OfferURL, OfferImageURL, OfferAddDate, OfferExpiryDate, OfferOriginSite, OfferTitle) " \
                    "VALUES(%s, %s, %s, %s, %s, %s, %s)"
            args = (
            offer_description, offer_url, offer_img_url, offer_add_date, offer_exp_date, offer_origin_site, offer_title)

            try:
                db_connector = DbConnector()
                conn = db_connector.getConn()
                cursor = conn.cursor()
                cursor.execute(query, args)
                conn.commit()
                cursor.close()
            except Error as error:
                print(error)
                return redirect(url_for('error_page.error_page_func', code="e2"))
    all_offers = []
    try:
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM Offers")  # gets all data stored in UserInfo table

        result = cursor.fetchall()
        for row in result:
            new_offer = Offer(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            all_offers.append(new_offer)
    except Error as error:
        print(error)
        return redirect(url_for('error_page.error_page_func', code="e2"))
    finally:
        cursor.close()
        conn.close()
    return render_template('admin_pages/manage_offers.html', title='Home', all_offers=all_offers)
