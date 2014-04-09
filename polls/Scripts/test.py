import kmeans
import random

"""
X=[0]*4
X[0]=[0,1]
X[1]=[1,0]
X[2]=[4,5]
X[3]=[5,4]
"""
X=[]

for i in range(3000):
    local=[random.random(),random.random()]
    X.append(local)


kmeans.ClusterKMeans(X)
