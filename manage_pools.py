from flask import Blueprint, render_template

manage_pools = Blueprint('manage_pools', __name__, template_folder='templates')


@manage_pools.route('/', methods=['GET', 'POST'])
def manage_pools_func():

    return render_template('manage_pools.html')


def money_pools():
    return


def create_money_pool():
    return


def access_money_pool():
    return


def leave_money_pool():
    return


def deposit_to_money_pool():
    return


def withdraw_from_money_pool():
    return


def delete_money_pool():
    return
