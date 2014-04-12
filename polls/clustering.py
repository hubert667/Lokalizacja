from polls.models import *
from Scripts import kmeans
import time

#only for data from SDCF
def ClusterData(user_id):
    
    locations_list = Lokalizacja.objects.filter(user=user_id)
    location_data=[]
    for loc in locations_list:
        location_data.append([float(loc.x),float(loc.y)])
    doClusters(user_id, location_data)
        

def ClusterDataAware(user_id,time_start,time_end):
    """
    Clusters data after it find optimal K
    """
    
    locations_list = Locations.objects.filter(device_id=user_id,timestamp__gte=time_start,timestamp__lte=time_end)
    location_data=[]
    for loc in locations_list:
        location_data.append([float(loc.double_latitude),float(loc.double_longitude)])
    
    doClusters(user_id, location_data)
        
def SmartClusterData(user_id,time_start,time_end):
    """
    Cluster localization data using additional techniques for improving performace
    """
    locations_list = Locations.objects.filter(device_id=user_id,timestamp__gte=time_start,timestamp__lte=time_end)
    location_data=[]
    for loc in locations_list:
        location_data.append([float(loc.double_latitude),float(loc.double_longitude)])
    
    doClusters(user_id, location_data)
    
def doClusters(user_id, location_data):
    clusters_centers = kmeans.FindKAndClusterKMeans(location_data)
    Clusters.objects.filter(user=user_id).delete()
    for cluster in clusters_centers:
        p = Clusters(x=str(cluster[0]), y=str(cluster[1]), user=user_id, ts=time.time())
        p.save()
    
    
    
    