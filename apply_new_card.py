from flask import Blueprint, render_template, session, redirect, url_for, request
from controllers.DbConnector import DbConnector
from mysql.connector import MySQLConnection, Error
from controllers.Card import Card
from datetime import datetime
import random
from random import choice
from classes.CardInfo import CardInfo
import string

apply_new_card = Blueprint('apply_new_card', __name__, template_folder='templates')


@apply_new_card.route('/', methods=['GET', 'POST'])
def apply_new_card_func():
    if request.method == "POST":
        user_id = session['userID']
        chars = string.digits
        card_type = request.form.get("card type")
        card_number = ''.join(choice(chars) for _ in range(16))

        now = datetime.now()
        start_date = now.strftime("%Y-%m-%d")

        year = now.strftime("%Y")
        expiry_year = int(year) + 3
        expiry_date = str(expiry_year) + (now.strftime("-%m-%d"))


        print(expiry_date)

        pin_number = ''.join(choice(chars) for _ in range(4))

        try:
            db_connector = DbConnector()
            conn = db_connector.getConn()
            db_connector.closeConn(conn)
            cursor = conn.cursor(buffered=True)

            cursor.execute("INSERT INTO UserCards VALUES (%s, %s, %s, %s, %s, %s)", (card_number, user_id, card_type,
                                                                                     start_date, expiry_date,
                                                                                     pin_number))

            conn.commit()
            cursor.close()
            conn.close()

        except Error as error:
            print(error)
            return redirect(url_for('error_page.error_page_foo', code="e2", src="accounts.html"))

        return render_template('manage_cards.html')

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
        return redirect(url_for('error_page.error_page_foo', code="e2", src="index.html"))

    return render_template('apply_card.html', card_types=card_types)
