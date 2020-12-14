from flask import Flask, Blueprint, render_template, request, session
from mysql.connector import MySQLConnection, Error
from controllers.DbConnector import DbConnector
from controllers.PasswordManager import PasswordManager
from classes import CardInfo

admin_new_card_page = Blueprint('admin_new_card', __name__, template_folder='templates')


@admin_new_card_page.route('/', methods=['GET', 'POST'])
def admin_new_card_func():
    allcards = []
    print("here")
    try:
        db_connector = DbConnector()
        conn = db_connector.getConn()
        cursor = conn.cursor()
        if request.method == "POST":
            desc = request.form.get("description")
            card = CardInfo.CardInfo(desc, "001")
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
        return render_template("error.html", msg="There seems to be an error adding a card, please try again or contact the system administrator", src="login.html")
    finally:
        cursor.close()
        conn.close()
        # closes connection

