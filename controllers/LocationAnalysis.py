import copy
from geopy import distance
from pyclustering.cluster.clique import clique
import numpy as np

'''
    File name: LocationAnalysis.py
    Author: Jacob Scase
    Credits: Jacob Scase
    Date created: 15/12/2020
    Date last modified: 18/12/2020
    Python Version: 3.7
    Purpose: File to analyse a group of transactions based on location. Uses the Clique clustering algorithm to create 
             clusters of locations of transactions and compares it to the the location of the transaction being 
             processed. Uses the geosidic distance calculation to measure the distance between the minimum possible 
             value and the max possible value to determine what range the user usually makes transactions in to 
             determine how varied their shopping habits usually are to help when identifying unusual activity. When
             clustering, the transaction to be compared is checked to see if it is a cluster on its own and therefore we
             can determine whether it is in an abnormal location for the user, taking into account their usual spread
             of transactions.
'''

# Latidude/Longitude level of precision
# 0dp = 102.47km
# 1dp = 10.247km
# 2dp = 1.0247km
# 3dp = 0.10247km

def dist_between_two_coords(coord1, coord2):
    coords_lim1 = (round(coord1[0], 3), round(coord1[1], 3))
    coords_lim2 = (round(coord2[0], 3), round(coord2[1], 3))
    print(distance.distance(coords_lim1, coords_lim2).km, "km")
    return distance.distance(coords_lim1, coords_lim2).km


def location_analysis(newTransaction, transaction_list):
    t_arr_lat = []
    t_arr_long = []
    copy_of_transaction_list = copy.copy(transaction_list)
    copy_of_transaction_list.append(newTransaction)
    for item in copy_of_transaction_list:
        t_arr_lat.append(item.latitude)
        t_arr_long.append(item.longitude)

    f0 = np.array(t_arr_lat).astype(np.float)  # Latitude
    f1 = np.array(t_arr_long).astype(np.float)  # Longitude
    data = np.array([f1, f0])
    data = data.T
    data_M = np.array(data)


    # print(np.quantile(f0, 0.001, axis=0))
    # print("LATITUDE QUANTILE")
    # print(np.quantile(f0, 0.999, axis=0))

    # print(np.quantile(f1, 0.001, axis=0))
    # print("LONGITUDE QUANTILE")
    # print(np.quantile(f1, 0.999, axis=0))
    poss_min = [f0.min(), f1.min()]
    poss_max = [f0.max(), f1.max()]
    # Get distance from max possible distance and min possible to see what range they usually buy stuff in
    max_possible_dist = dist_between_two_coords(poss_min, poss_max)

    # Create CLIQUE algorithm for processing


    interval_length = round(max_possible_dist / 4)
    # print("il = ", interval_length)

    # Define the number of grid cells in each dimension
    #Defaults to 1 interval if few transactions provided
    intervals = max(1,interval_length)

    # Density threshold
    threshold = 0

    clique_instance = clique(data_M, intervals, threshold)

    # Start the clustering process and get the results
    clique_instance.process()
    clique_cluster = clique_instance.get_clusters()  # allocated clusters

    # Points considered as outliers (noise points)
    noise = clique_instance.get_noise()
    # print("noise=", noise)
    # CLIQUE formed grid unit
    cells = clique_instance.get_cells()

    # Display the grid formed by the algorithm
    # clique_visualizer.show_grid(cells, data_M)
    # # Display clustering results
    # clique_visualizer.show_clusters(data_M, clique_cluster, noise)  # show clustering results

    # print("Amount of clusters:", len(clique_cluster))
    # print(clique_cluster)
    for cluster in clique_cluster:
        if len(cluster) < 2:
            # if there are less than 2 in the cluster, means that they have only purchased something in that cluster once
            cluster_val_lat = f0[cluster[0]]
            cluster_val_lon = f1[cluster[0]]
            # print(cluster_val_lat, cluster_val_lon)
            # print("small cluster")
            if cluster_val_lat == newTransaction.latitude and cluster_val_lon == newTransaction.longitude:
                # if the new transaction is one of these values in a cluster on its own then they haven't bought
                # anything in this area before so could possibly be anomaly
                # print("The new one could be an anomaly")
                return True
    return False
