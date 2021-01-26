from flask import Blueprint, render_template

display_pool = Blueprint('display_pool', __name__, template_folder='templates')


@display_pool.route('/', methods=['GET', 'POST'])
def display_pool_func():

    return render_template('display_pool.html')