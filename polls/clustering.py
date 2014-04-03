from polls.models import *
from Scripts import kmeans
import time

def ClusterData(user_id):
    
    locations_list = Lokalizacja.objects.filter(user=user_id)
    location_data=[]
    for loc in locations_list:
        location_data.append([float(loc.x),float(loc.y)])
    clusters_centers=kmeans.ClusterKMeans(location_data)
    previous_clusters=Clusters.objects.filter(user=user_id).delete()
    for cluster in clusters_centers:
        p = Clusters(x=str(cluster[0]), y=str(cluster[1]),user=user_id,ts=time.time())
        p.save()
    