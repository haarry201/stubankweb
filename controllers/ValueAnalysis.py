from sklearn.cluster import MeanShift, estimate_bandwidth
import numpy as np

'''
    File name: ValueAnalysis.py
    Author: Jacob Scase
    Credits: Jacob Scase
    Date created: 16/12/2020
    Date last modified: 18/12/2020
    Python Version: 3.7
    Purpose: File to analyse a group of transactions based on value. Uses the mean shift clustering procedure to
             determine clusters of usual values. In this instance, it clusters times to get clusters when a person
             usually purchases at a certain shop at certain times and then provides a prediction cluster of where
             it will be likely to be placed in. It then uses an interquartile bound check to check whether the value 
             would likely reside within the cluster and then potentially increases the probability of fraud if it
             does not lie in the predicted cluster. It does the same clustering prediction method for monetary values. 
             If the user has not shopped at that particular place before, then it adds to the suspicion value if the
             transaction amount is above a certain threshold as there is limited data available, and then takes all
             purchase time data and compares it against that.
             
'''


def get_clusters(arr):
    X = np.array(list(zip(arr, np.zeros(len(arr)))), dtype=np.int)
    bandwidth = estimate_bandwidth(X, quantile=0.1)
    if bandwidth == 0:
        bandwidth = None
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(X)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_
    # print(cluster_centers)
    labels_unique = np.unique(labels)
    n_clusters = len(labels_unique)
    return X, n_clusters, labels, ms


def analyse_values(new_transaction, t_list):
    shopped_at_place_before = False
    suspicion_value = 0
    t_arr = []
    name = []
    val = []
    time = []
    t_dict_arr = []
    for item in t_list:
        # Add all the t objects to the arrays
        t_arr.append([item.recipient_name, item.balance_change, item.time])
        name.append(item.recipient_name)
        if item.balance_change < 0:
            item.balance_change *= -1
        val.append(item.balance_change)
        time.append(item.time)
        # Add the first transaction to the list
        found = False
        for i in range(len(t_dict_arr)):
            # Adding the rest of the transactions to the list
            if t_dict_arr[i]["name"] == item.recipient_name:
                t_dict_arr[i]["properties"].append([item.balance_change, item.time])
                found = True
        if not found:
            t_dict_arr.append({"name": item.recipient_name, "properties": [[item.balance_change, item.time]]})
    for item in t_dict_arr:
        times = []
        amounts = []
        if item["name"] == new_transaction.recipient_name:
            shopped_at_place_before = True
            # If there has already been a transaction at this place before
            for value in item["properties"]:
                times.append(value[1])
                amounts.append(value[0])
            X, n_clusters, labels, ms = get_clusters(times)
            new_time_as_np = np.array(list(zip([new_transaction.time], np.zeros(1))), dtype=np.int)
            prediction_value = ms.predict(new_time_as_np)
            for k in range(n_clusters):
                my_members = labels == k
                if prediction_value == k:
                    time_values = X[my_members, 0].tolist()
                    time_values_with_new_t = np.array(time_values)
                    # Takes the cluster that the new transaction is most likely predicted to be in, and compares it to
                    # the values inside using an interquartile bound check to see whether it is likely to fit inside
                    # the cluster.

                    suspicious_time_place = iqr_bound_check(new_transaction.time, time_values_with_new_t)
                    print("sus time place",suspicious_time_place)
                    if suspicious_time_place:
                        suspicion_value += 0.25
                    suspicious_amount_for_place = iqr_bound_check(abs(new_transaction.balance_change),
                                                                  np.array(amounts))
                    print("sus amoiunt for place",suspicious_amount_for_place)
                    if suspicious_amount_for_place:
                        suspicion_value += 0.25
    if not shopped_at_place_before:
        if new_transaction.balance_change > 50000:
            ##Over 50000 pence i.e. £500
            suspicion_value += 0.3
        elif new_transaction.balance_change > 10000:
            ##Over 10000 pence i.e. £100
            suspicion_value += 0.2
        all_usual_times = np.array(time)
        suspicious_time_for_transaction = iqr_bound_check(abs(new_transaction.time), all_usual_times)
        if suspicious_time_for_transaction:
            suspicion_value += 0.2
        all_usual_values = np.array(val)
        suspicious_amount_for_transaction = iqr_bound_check(abs(new_transaction.balance_change), all_usual_values)
        if suspicious_amount_for_transaction:
            suspicion_value += 0.75
    return suspicion_value


def iqr_bound_check(new_transaction_value, poss_values_with_new_t):
    # Takes in a value from a transaction and compares it to a cluster of values, calculates the interquartile range
    # of these
    lower_quantile = np.quantile(poss_values_with_new_t, 0.25, axis=0)
    upper_quantile = np.quantile(poss_values_with_new_t, 0.75, axis=0)
    iqr = upper_quantile - lower_quantile
    lower_bound = lower_quantile - (1.5 * iqr)
    upper_bound = upper_quantile + (1.5 * iqr)
    if new_transaction_value > upper_bound or new_transaction_value < lower_bound:
        #Outside either bound so assumed not to be part of the cluster
        return True
    return False
