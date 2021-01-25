from flask import Blueprint, render_template, session

'''
File name: extra_info.py
Author: Rhys Minchin
Credits: Rhys Minchin
Date created: 13/01/2021
Date last modified: 25/01/2021
Python version: 3.7
Purpose: This provides the back-end for any additional information displayed on the homepage/other pages throughout the
         project. The functionality is here for: contacting the team, providing additional information about the
         available StuBank accounts, and providing extra information about the Team 35.
'''

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