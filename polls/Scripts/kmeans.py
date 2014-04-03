from sklearn.cluster import KMeans

"""
dataToCluster: shape(n_samples,m_dimensions)
"""
def ClusterKMeans(dataToCluster):

    k_means=KMeans(n_clusters=3, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances=True, verbose=0, random_state=None, copy_x=True, n_jobs=1)
    k_means.fit(dataToCluster)
    return k_means.cluster_centers_
