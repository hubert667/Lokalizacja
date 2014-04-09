from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

"""
Part of the code cames from the Data Science Blog
http://datasciencelab.wordpress.com/2014/01/21/selection-of-k-in-k-means-clustering-reloaded/
"""
def ClusterKMeans(dataToCluster):

    results=[]
    fs, Sk = findK(1,dataToCluster)
    results.append(fs)
    for i in range(2,19):
        fs, Sk = findK(i,dataToCluster,Sk)
        results.append(fs)
    print results
    res_clusters=choose_clusters(results,dataToCluster)
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
        sum=0   
        for i in range(local_K):
            for c in clusters[i]:
                sum+=np.linalg.norm(mu[i]-c)**2
        Sk=sum
        """
        Sk = sum([np.linalg.norm(mu[i]-c)**2 \
                 for i in range(local_K) for c in clusters[i]])
        """
        print Sk
        #print "___"
        if local_K == 1:
            fs = 1
        elif Skm1 == 0:
            fs = 1
        else:
            fs = Sk/(a(local_K,Nd)*Skm1)
            print a(local_K,Nd)
            #fs = Sk/(Skm1)
        return fs, Sk   

def choose_clusters(results,X):
    fig = plt.figure(figsize=(40,10))
    x = range(1, len(results)+1)
    ax2 = fig.add_subplot(132)
    ax2.set_ylim(0, 1.2)
    ax2.plot(x, results, 'ro-', alpha=0.6)
    ax2.set_xlabel('Number of clusters K', fontsize=15)
    ax2.set_ylabel('value of f(K)', fontsize=15) 
    plt.savefig('detK_N%s.png' % (str(len(X))),bbox_inches='tight', dpi=100)
    result_K= np.where(results == min(results))[0][0] + 1
    return result_K

def find_groups(k_means,dataToCluster,local_K):
    clusters={}
    labels=k_means.labels_
    for i in range(local_K):
        clusters[i]=[]
    for i in range(len(labels)):
        label=labels[i]
        clusters[label].append(dataToCluster[i])
    return clusters
        
