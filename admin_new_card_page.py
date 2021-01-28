from flask import Blueprint, render_template, request, redirect, url_for, session
from mysql.connector import Error
from controllers.DbConnector import DbConnector
from classes import CardInfo

'''
File name: admin_new_card_page.py
Author: Jacob Scase
Credits: Jacob Scase, Harry Kenny
Date created: 14/12/2020
Date last modified: 28/01/2021
Python version: 3.7
Purpose: Back-end file for allowing the admin to add new types of cards
'''

admin_new_card_page = Blueprint('admin_new_card_page', __name__, template_folder='templates')


@admin_new_card_page.route('/', methods=['GET', 'POST'])
def admin_new_card_page_func():
    try:
        # redirects user appropriately based on 2FA status, or whether they are an admin or not
        if 'user_id' in session:
            if session['needs_auth'] == True:
                return redirect(url_for('login_page.login_page_func'))
            elif session['user_role'] == 'Admin':
                pass
            else:
                return redirect(url_for('admin_home_page.admin_home_page_func'))
        else:
            return redirect(url_for('login_page.login_page_func'))
    except:
        return redirect(url_for('login_page.login_page_func'))
    allcards = []
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
        if row:
            for item in row:
                card = CardInfo.CardInfo(item[0], item[1])
                allcards.append(card)
                # checks input data against stored data
        conn.close()
        return render_template('admin_pages/new_card.html', all_cards=allcards)
    except Error as e:
        print(e)
        return redirect(url_for('error_page.error_page_func', code="e6", src="index.html"))
    finally:
        cursor.close()
        conn.close()
        # closes connection

