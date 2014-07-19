from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import datetime
import polls.constans

"""
Part of the code is from the Data Science Blog
http://datasciencelab.wordpress.com/2014/01/21/selection-of-k-in-k-means-clustering-reloaded/
"""
def FindKAndClusterKMeans(dataToCluster):

    results=[]
    fs, Sk = findK(1,dataToCluster)# 1 offset. 0 index means 1 cluster
    results.append(fs)
    for i in range(2,25):
        fs, Sk = findK(i,dataToCluster,Sk)
        results.append(fs)
    
    res_clusters=choose_clusters(results,dataToCluster)
    #res_clusters=3
    k_means=KMeans(n_clusters=res_clusters, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances=True, verbose=0, random_state=None, copy_x=True, n_jobs=1)
    k_means.fit(dataToCluster)
    return k_means.cluster_centers_

def findK( local_K, dataToCluster,Skm1=0):
        X = dataToCluster
        Nd = len(X[0])
        a = lambda k, Nd: 1 - 3.0/(4.0*Nd) if k == 2 else a(k-1, Nd) + (1.0-a(k-1, Nd))/6.0
        #self.find_centers(local_K, method='++')
        #mu, clusters = self.mu, self.clusters
        k_means=KMeans(n_clusters=local_K, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances=True, verbose=0, random_state=None, copy_x=True, n_jobs=1)
        k_means.fit(dataToCluster)
        mu=k_means.cluster_centers_
        clusters=find_groups(k_means,dataToCluster,local_K)
        local_sum=0   
        for i in range(local_K):
            for c in clusters[i]:
                local_sum+=np.linalg.norm(mu[i]-c)**2
        Sk=local_sum
        """
        Sk = sum([np.linalg.norm(mu[i]-c)**2 \
                 for i in range(local_K) for c in clusters[i]])
        """
        #print "___"
        if local_K == 1:
            fs = 1
        elif Skm1 == 0:
            fs = 1
        else:
            fs = Sk/(a(local_K,Nd)*Skm1)
            #fs = Sk/(Skm1)
        return fs, Sk   

def choose_clusters(results,X):
    
    local_min_threshold=0.1 #for choosing local minimum in the graph
    fig = plt.figure(figsize=(40,10))
    x = range(1, len(results)+1)
    ax2 = fig.add_subplot(132)
    ax2.set_ylim(0, 1.2)
    ax2.plot(x, results, 'ro-', alpha=0.6)
    ax2.set_xlabel('Number of clusters K', fontsize=15)
    ax2.set_ylabel('value of f(K)', fontsize=15) 
    plt.savefig('detK_N%s.png' % (str(len(X))+str(datetime.datetime.now()+polls.constans.time_change)),bbox_inches='tight', dpi=100)
    
    #result_K= np.where(results == min_val(results))[0][0] + 1
    result_K=None
    min_val=1000
    max_val=-1000
    for i in range(1,len(results)-1):
        if results[i]>max_val:
            max_val=results[i]
        if results[i]<min_val:
            min_val=results[i]
        if results[i]<results[i-1] and results[i]<results[i+1] and ( max_val==min_val or (max_val-results[i])/(max_val-min_val)>local_min_threshold):
            result_K=i
    print result_K+1
    return result_K+1

def find_groups(k_means,dataToCluster,local_K):
    clusters={}
    labels=k_means.labels_
    for i in range(local_K):
        clusters[i]=[]
    for i in range(len(labels)):
        label=labels[i]
        clusters[label].append(dataToCluster[i])
    return clusters
        
