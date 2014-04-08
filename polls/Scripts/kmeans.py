from sklearn.cluster import KMeans
import numpy as np

"""
dataToCluster: shape(n_samples,m_dimensions)
"""
def ClusterKMeans(dataToCluster):

    results=[]
    fs, Sk = findK(1,dataToCluster)
    for i in range(2,20):
        fs, Sk = findK(i,dataToCluster,Sk)
        results.append(fs)
    print results
    k_means=KMeans(n_clusters=3, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances=True, verbose=0, random_state=None, copy_x=True, n_jobs=1)
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
        #print mu
        #print clusters
        
        """
        sum=0   
        for i in range(local_K):
            for c in clusters[i]:
                sum+=np.linalg.norm(mu[i]-c)**2

        Sk=sum
        """
        Sk = sum([np.linalg.norm(mu[i]-c)**2 \
                 for i in range(local_K) for c in clusters[i]])
        #print Sk
        #print "___"
        if local_K == 1:
            fs = 1
        elif Skm1 == 0:
            fs = 1
        else:
            fs = Sk/(a(local_K,Nd)*Skm1)
            #print a(local_K,Nd)
            #fs = Sk/(Skm1)
        return fs, Sk   

def find_groups(k_means,dataToCluster,local_K):
    clusters={}
    labels=k_means.labels_
    for i in range(local_K):
        clusters[i]=[]
    for i in range(len(labels)):
        label=labels[i]
        clusters[label].append(dataToCluster[i])
    return clusters
        
