from sklearn.cluster import MeanShift, estimate_bandwidth
import numpy as np


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
            print(item["name"], new_transaction.recipient_name)
            print("shopped here before")
            shopped_at_place_before = True
            # If there has already been a transaction at this place before
            for value in item["properties"]:
                times.append(value[1])
                amounts.append(value[0])
            X, n_clusters, labels, ms = get_clusters(times)
            new_time_as_np = np.array(list(zip([new_transaction.time], np.zeros(1))), dtype=np.int)
            prediction_value = ms.predict(new_time_as_np)
            # print("Cluster prediction:", prediction_value)
            for k in range(n_clusters):
                my_members = labels == k
                if prediction_value == k:
                    time_values = X[my_members, 0].tolist()
                    time_values_with_new_t = np.array(time_values)

                    # IQR Method
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
        print("NOT SHOPPED HERE BEFORE")
        # print(val)
        if new_transaction.balance_change > 500:
            suspicion_value += 0.3
        elif new_transaction.balance_change > 100:
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
    lower_quantile = np.quantile(poss_values_with_new_t, 0.25, axis=0)
    upper_quantile = np.quantile(poss_values_with_new_t, 0.75, axis=0)
    iqr = upper_quantile - lower_quantile
    lower_bound = lower_quantile - (1.5 * iqr)
    upper_bound = upper_quantile + (1.5 * iqr)
    print("bounds =")
    print(lower_bound, upper_bound)
    if new_transaction_value > upper_bound or new_transaction_value < lower_bound:
        # print("outside both bounds")
        return True
    return False
