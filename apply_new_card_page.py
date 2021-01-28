from flask import Blueprint, render_template, session, redirect, url_for, request
from controllers.DbConnector import DbConnector
from mysql.connector import Error
from datetime import datetime
from random import choice
from classes.CardInfo import CardInfo
from manage_cards_page import get_info
import string

'''
File name: apply_new_card_page.py
Author: Harry Kenny
Credits: Harry Kenny
Date created: 23/01/2021
Date last modified: 25/01/2021
Python version: 3.7
Purpose: Back-end file for allowing the user to apply for a new card and add it to their account.
'''

apply_new_card_page = Blueprint('apply_new_card_page', __name__, template_folder='templates')


@apply_new_card_page.route('/', methods=['GET', 'POST'])
def apply_new_card_page_func():
    try:
        # redirects user appropriately based on 2FA status, or whether they are an admin or not
        if 'user_id' in session:
            if session['needs_auth'] == True:
                return redirect(url_for('login_page.login_page_func'))
            elif session['user_role'] == 'User':
                pass
            else:
                return redirect(url_for('admin_home_page.admin_home_page_func'))
        else:
            return redirect(url_for('login_page.login_page_func'))
    except:
        return redirect(url_for('login_page.login_page_func'))
    if request.method == "POST":
        user_id = session['user_id']
        chars = string.digits
        card_type = request.form.get("all_cards")
        card_number = ''.join(choice(chars) for _ in range(16))

        now = datetime.now()
        start_date = now.strftime("%Y-%m-%d")

        year = now.strftime("%Y")
        expiry_year = int(year) + 3
        expiry_date = str(expiry_year) + (now.strftime("-%m-%d"))

        pin_number = ''.join(choice(chars) for _ in range(4))

        try:
            db_connector = DbConnector()
            conn = db_connector.getConn()
            cursor = conn.cursor(buffered=True)

            cursor.execute("INSERT INTO UserCards VALUES (%s, %s, %s, %s, %s, %s)", (card_number, user_id, card_type,
                                                                                     start_date, expiry_date,
                                                                                     pin_number))
            conn.commit()

        except Error as error:
            print(error)
            return redirect(url_for('error_page.error_page_func', code="e2"))

        all_user_cards, all_possible_cards = get_info(cursor, user_id)

        cursor.close()
        conn.close()


        return render_template('manage_cards.html', all_user_cards=all_user_cards, all_possible_cards=all_possible_cards)

    try:
        db_connector = DbConnector()
        conn = db_connector.getConn()
        cursor = conn.cursor()

        card_types = []

        cursor.execute("SELECT * FROM CardInfo")
        result = cursor.fetchall()
        for row in result:
            card = CardInfo(row[0], row[1])
            card_types.append(card)

    except Error as e:
        print(e)
        return redirect(url_for('error_page.error_page_func', code="e2"))

    return render_template('apply_card.html', card_types=card_types)
