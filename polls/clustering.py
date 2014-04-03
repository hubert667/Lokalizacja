from polls.models import *
from Scripts import kmeans

def ClusterData():
    
    locations_list = Lokalizacja.objects.all()
    location_data=[]
    for loc in locations_list:
        location_data.append([float(loc.x),float(loc.y)])
    clusters_centers=kmeans.ClusterKMeans(location_data)
    for cluster in clusters_centers:
        p = Clusters(x=str(cluster[0]), y=str(cluster[1]))
        p.save()
    