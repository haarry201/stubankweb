'''
    File name: Offer.py
    Author: Jacob Scase
    Credits: Jacob Scase
    Date created: 13/01/2021
    Date last modified: 25/01/2021
    Python Version: 3.7
    Purpose: Class to store Offers that the user will see displayed on the offers page
'''
class Offer:
    def __init__(self, description, url, img_url, add_date, expiry_date, origin_site, offer_title, offer_id):
        self.description = description
        self.url = url
        self.img_url = img_url
        self.add_date = add_date
        self.expiry_date = expiry_date
        self.origin_site = origin_site
        self.offer_title = offer_title
        self.offer_id = offer_id
