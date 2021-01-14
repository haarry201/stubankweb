from flask import Blueprint, render_template, session

extra_info = Blueprint('extra_info', __name__, template_folder='templates')


@extra_info.route('/contact')
def contact():
    try:
        return render_template('extra_info.html', command="Contact", name=session['name'])
    except KeyError:
        return render_template('extra_info.html', command="Contact", name='')


@extra_info.route('/accounts')
def accounts():
    try:
        return render_template('extra_info.html', command="Accounts", name=session['name'])
    except KeyError:
        return render_template('extra_info.html', command="Accounts", name='')


@extra_info.route('/aboutus')
def about_us():
    try:
        return render_template('extra_info.html', command="About Us", name=session['name'])
    except KeyError:
        return render_template('extra_info.html', command="About Us", name='')