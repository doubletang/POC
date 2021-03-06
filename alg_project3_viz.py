"""
Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""

# Flavor of Python - desktop or CodeSkulptor
DESKTOP = True

import math
import random
import urllib2
import alg_cluster
import matplotlib.pyplot as plt


# conditional imports
import M3      # desktop project solution
import alg_clusters_matplotlib



###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering
    
    Note that method may return num_clusters or num_clusters + 1 final clusters
    """
    
    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters
    
    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)
            
    return cluster_list
                
def compute_distortion(cluster_list, data_table):
    distortion = 0
    for cluster in cluster_list:
        error = cluster.cluster_error(data_table)
        distortion += error
    return distortion
#####################################################################
# Code to load cancer data, compute a clustering and 
# visualize the results


def run_example(method, arg):
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    data_table = load_data_table(DATA_896_URL)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
#     cluster_list = sequential_clustering(singleton_list, 15)    
#     print "Displaying", len(cluster_list), "sequential clusters"
# 
    if method == 'h':
        cluster_list = M3.hierarchical_clustering(singleton_list, arg[0])
        print '\n'
        print "Displaying", len(cluster_list), "hierarchical clusters"
    elif method == 'k':

        cluster_list = M3.kmeans_clustering(singleton_list, arg[0], arg[1]) 
        print '\n'
        print "Displaying", len(cluster_list), "k-means clusters"
    
    return compute_distortion(cluster_list, data_table)

            
    # draw the clusters using matplotlib or simplegui

#     alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)

h = []
k = []    
for n in range(6, 21):
    h.append(run_example('h', [n]))
    k.append(run_example('k', [n, 5]))
    
plt.plot(range(6, 21), h, '-r', label='hierarchical clustering')
plt.plot(range(6, 21), k, '-b', label='k-means clustering')
plt.legend(loc='upper right')
plt.xlabel('Number of output clusters')
plt.ylabel('Distortion')
plt.title('The comparing the distortion (the 896 county data)')
plt.show()


             
    





    





  
        






        





