import random
import controllers.LocationAnalysis as LocationAnalysis
import controllers.ValueAnalysis as ValueAnalysis
from controllers.DbConnector import DbConnector

'''
    File name: Transaction.py
    Author: Jacob Scase
    Credits: Jacob Scase
    Date created: 15/12/2020
    Date last modified: 21/01/2021
    Python Version: 3.7
    Purpose: Class to store transactions, with a method to analyse that transaction in comparison to the rest
    of a users transactions. Methods also to fetch transactions from a certain account number.
'''

def gen_values():
    t_list = []
    place_list = ["Asda", "Tesco", "Morrisons", "Sainsburys", "Newcastle University", "Boots", "Costa", "Starbucks",
                  "Food Place"]
    for x in range(1000000):
        # Generate 100 transactions of different values in different places
        t_lat = 54.9 + (random.random() / 10)
        t_long = -1.6 + (random.random() / 10)
        t_place = random.choice(place_list)
        t_value = round(random.uniform(-1000, 0.01), 2)
        # Between 8am and 10pm
        t_time = random.randint(480, 1320)
        new_transaction = MLTransaction(t_place, t_value, t_lat, t_long, t_time)
        t_list.append(new_transaction)

    # York
    # new_transaction_y = MLTransaction("Tesco", 50.00, 53.904338, -1.059040, 1080)
    #
    # # Leeds
    # new_transaction_le = MLTransaction("Tesco", 50.00, 53.783372, -1.537014, 1080)
    #
    # # Liverpool
    # new_transaction_li = MLTransaction("Tesco", 50.00, 53.374808, -3.023611, 1080)
    #
    # # Durham
    # new_transaction_du = MLTransaction("Tesco", 50.00, 54.773900, -1.584489, 1080)
    # t_list.append(new_transaction_y)
    # t_list.append(new_transaction_le)
    # t_list.append(new_transaction_li)
    # t_list.append(new_transaction_du)
    return t_list


def fetch_transactions(transferer_account_num):
    t_list = []
    # Get database connection information
    db_connector = DbConnector()
    conn = db_connector.getConn()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM Transactions WHERE AccountNumSending = (%s) OR AccountNumReceiving = (%s)",
                   (transferer_account_num, transferer_account_num))
    row = cursor.fetchone()
    while row is not None:
        # For each row(each transaction) parse data out of it
        # Bal change convert from pennies into pounds
        transaction_bal_change = abs(row[5] / 100)
        transaction_time = int(row[7])
        transaction_recipient = str(row[10])
        transaction_longitude = float(row[11])
        transaction_latitude = float(row[12])
        previous_transaction = MLTransaction(transaction_recipient, transaction_bal_change, transaction_latitude,
                                             transaction_longitude, transaction_time)
        t_list.append(previous_transaction)
        row = cursor.fetchone()
    cursor.close()
    conn.close()
    return t_list


class MLTransaction:
    def __init__(self, recipient_name, balance_change, latitude, longitude, time):
        self.recipient_name = recipient_name
        self.balance_change = balance_change
        self.latitude = latitude
        self.longitude = longitude
        self.time = time

    def analyse_transaction(self, transaction_list):
        p_fraud = 0
        is_abnormal_location = LocationAnalysis.location_analysis(self, transaction_list)
        print("From Location this could be an anomaly: = ", is_abnormal_location)
        if is_abnormal_location:
            p_fraud += 0.4
        suspicion_value_from_value_analysis = ValueAnalysis.analyse_values(self, transaction_list)
        print("From value and place this could be an anomaly: = ", suspicion_value_from_value_analysis)
        p_fraud += suspicion_value_from_value_analysis
        print("Overall suspicion level of fraud = : ", p_fraud)
        return p_fraud
