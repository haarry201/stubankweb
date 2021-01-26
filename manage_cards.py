from flask import Blueprint, render_template, session, redirect, url_for, request
from controllers.DbConnector import DbConnector
from mysql.connector import MySQLConnection, Error
from controllers.Card import Card


manage_cards = Blueprint('manage_cards', __name__, template_folder='templates')


@manage_cards.route('/', methods=['GET', 'POST'])
def manage_cards_func():
    user_id = session['user_id']
    all_user_cards = []

    try:
        db_connector = DbConnector()
        conn = db_connector.getConn()
        db_connector.closeConn(conn)
        cursor = conn.cursor(buffered=True)

        cursor.execute("SELECT * FROM UserCards")
        result = cursor.fetchall()
        for row in result:
            if row[1] == user_id:
                user_card = Card(row[0], row[2], row[3], row[4], row[5])
                all_user_cards.append(user_card)

    except Error as e:
        print(e)
        return redirect(url_for('error_page.error_page_foo', code="e2", src="index.html"))

    return render_template('manage_cards.html', all_user_cards=all_user_cards)


def view_card_info():
    return

