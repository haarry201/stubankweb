from flask import Blueprint, render_template


manage_cards = Blueprint('manage_cards', __name__, template_folder='templates')


@manage_cards.route('/', methods=['GET', 'POST'])
def manage_cards_func():

    return render_template('manage_cards.html')

def view_card_info():
    return

def apply_new_card():
    return

