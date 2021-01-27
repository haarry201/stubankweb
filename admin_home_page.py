from flask import Blueprint, render_template, request, session, redirect, url_for
from mysql.connector import Error
from controllers.DbConnector import DbConnector

'''
File name: admin_home_page.py
Author: Jacob Scase
Credits: Jacob Scase
Date created: 21/01/2021
Date last modified: 25/01/2021
Python version: 3.7
Purpose: Back-end file for the admin home page, allows admins to add and remove other admins privelages, will redirect
         the user if not an admin to the error page. 
'''

admin_home_page = Blueprint('admin_home_page', __name__, template_folder='templates')


@admin_home_page.route('/', methods=['GET', 'POST'])
def admin_home_page_func():
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
    try:
        user_role = session.get('user_role')
    except Error as e:
        print("error, no session key set")
    if request.method == "POST":
        try:
            db_connector = DbConnector()
            conn = db_connector.getConn()
            if 'delete' in request.form:
                user_role = 'User'
                user_email = request.form.get('delete')
            else:
                user_email = request.form.get('email')
                user_role = 'Admin'
            cursor = conn.cursor()
            # cursor.execute("DELETE * FROM Offers WHERE OfferID = %s", offer_id)
            cursor.execute("UPDATE UserInfo SET UserRole = (%s) WHERE EmailAddress = (%s)", (user_role, user_email))
            conn.commit()
            cursor.close()
        except Error as error:
            return redirect(url_for('error_page.error_page_func', code="e2", src="index.html"))
    admin_users = []
    db_connector = DbConnector()
    conn = db_connector.getConn()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT EmailAddress FROM UserInfo WHERE UserRole != 'User'")
    result = cursor.fetchall()  # fetches first row of table
    for row in result:
        admin_users.append(row[0])
    return render_template('/admin_pages/admin_home.html', admin_users=admin_users)
