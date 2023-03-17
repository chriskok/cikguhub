from django.shortcuts import  render, redirect
from django.db.models import Case, When
from django.http import HttpResponse
from django.contrib import messages
from sklearn.cluster import KMeans

import json
import numpy as np
import pandas as pd

def clustering(X, k):
    kmeans = KMeans(n_clusters=k).fit(X)
    labels = kmeans.labels_
    return labels

def illustrate_cluster(labels, one_hot_df):
    clustered_groups = one_hot_df.copy()
    clustered_groups['cluster'] = labels
    
    cluster_means = clustered_groups.groupby('cluster').mean() # get cluster means
    cluster_counts = clustered_groups.groupby('cluster').count() # get cluster counts
    consider = cluster_means[['experience', 'teaching_level', 'roles_T']] # list of features we could highlight
    # we want to highlight the features for each cluster that are furthest from the mean
    highlight = consider.columns[np.argsort(np.array(abs((consider - np.mean(consider, axis=0))\
                                                         /np.mean(consider, axis=0))))[:, -2:]]
    cluster_msgs = {}
    for i in range(len(cluster_means)):
        msg = f"{cluster_counts.iloc[i]['experience']} people, "
        
        for h in highlight[i]:
            value = cluster_means.iloc[i][h]
            if 'roles_T' in h: msg = msg + f'{round(100*value)}% are teachers, '
            elif 'experience' in h: msg = msg + f'average experience is {round(value, 2)} years, '
            elif 'teaching_level' in h: msg = msg + f'Average school level is {round(value)}, '
            else: msg = msg + str(h) +  str(cluster_means.iloc[i][h])
        
        cluster_msgs[f'Cluster {i}'] = msg
    return cluster_msgs
    
X = np.array(one_hot_um)
labels = clustering(X, 4)
cluster_msgs = illustrate_cluster(labels, one_hot_um)