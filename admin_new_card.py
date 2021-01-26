from flask import Blueprint, render_template, request, redirect, url_for
from mysql.connector import Error
from controllers.DbConnector import DbConnector
from classes import CardInfo

'''
File name: admin_new_card.py
Author: Jacob Scase
Credits: Jacob Scase, Harry Kenny
Date created: 14/12/2020
Date last modified: 25/01/2021
Python version: 3.7
Purpose: Back-end file for allowing the admin to add new types of cards
'''

admin_new_card = Blueprint('admin_new_card', __name__, template_folder='templates')


@admin_new_card.route('/', methods=['GET', 'POST'])
def admin_new_card_func():
    allcards = []
    print("here")
    try:
        db_connector = DbConnector()
        conn = db_connector.getConn()
        cursor = conn.cursor()
        if request.method == "POST":

            cursor.execute("SELECT CardTypeID FROM CardInfo ORDER BY CardTypeID DESC LIMIT 1;")
            row = cursor.fetchone()
            last_id = row[0]
            new_number = int(last_id) + 1
            new_id = str(new_number).zfill(3)

            desc = request.form.get("description")
            card = CardInfo.CardInfo(new_id, desc)
            query = "INSERT INTO CardInfo " \
                    "VALUES(%s, %s)"
            args = (card.type_id, card.desc)
            cursor.execute(query, args)
            conn.commit()
        query = ("SELECT * FROM CardInfo")
        cursor.execute(query)
        row = cursor.fetchall()  # fetches all rows of table
        print("here2")
        if row:
            print("here3")
            print(row)
            for item in row:
                print(item)
                card = CardInfo.CardInfo(item[1], item[0])
                allcards.append(card)
                # checks input data against stored data
                print("here4")

        conn.close()
        return render_template('new_card.html', all_cards=allcards)
    except Error as e:
        print(e)
        return redirect(url_for('error_page.error_page_func', code="e6", src="index.html"))
    finally:
        cursor.close()
        conn.close()
        # closes connection

