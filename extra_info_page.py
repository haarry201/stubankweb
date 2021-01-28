from flask import Blueprint, render_template

'''
File name: extra_info_page.py
Author: Rhys Minchin
Credits: Rhys Minchin
Date created: 13/01/2021
Date last modified: 25/01/2021
Python version: 3.7
Purpose: This provides the back-end for any additional information displayed on the homepage/other pages throughout the
         project. The functionality is here for: contacting the team, providing additional information about the
         available StuBank accounts, and providing extra information about the Team 35.
'''

extra_info_page = Blueprint('extra_info_page', __name__, template_folder='templates')


# reads the url and passes through to the template with the appropriate command, so the correct info is shown
@extra_info_page.route('/contact')
def contact():
    return render_template('extra_info.html', command="Contact")


@extra_info_page.route('/accounts')
def accounts():
    return render_template('extra_info.html', command="Accounts")


@extra_info_page.route('/aboutus')
def about_us():
    return render_template('extra_info.html', command="About Us")
