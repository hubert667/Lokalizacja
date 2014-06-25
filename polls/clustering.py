from polls.models import *
from Scripts import kmeans
import time
import datetime
from datetime import timedelta
import operator

#only for data from SDCF
def ClusterData(user_id):
    
    locations_list = Lokalizacja.objects.filter(user=user_id)
    location_data=[]
    for loc in locations_list:
        location_data.append([float(loc.x),float(loc.y)])
    __doClusters(user_id, location_data)
    
        

def ClusterDataAware(user_id,time_start,time_end):
    """
    Clusters data after it find optimal K
    """
    
    locations_list = Locations.objects.filter(device_id=user_id,timestamp__gte=time_start,timestamp__lte=time_end)
    location_data=[]
    for loc in locations_list:
        location_data.append([float(loc.double_latitude),float(loc.double_longitude)])
    
    __doClusters(user_id, location_data)
        

def SmartClusterData(user_id,time_start,time_end):
    """
    Cluster localization data using additional techniques for improving performace
    """
    locations_list =GetStaticLocations(user_id, time_start, time_end)
    location_data=[]
    for loc in locations_list:
        location_data.append([float(loc.double_latitude),float(loc.double_longitude)])
    
    __doClusters(user_id, location_data)
    
def GetStaticLocations(user_id, time_start, time_end):
    locations_list = Locations.objects.filter(device_id=user_id, timestamp__gte=time_start, timestamp__lte=time_end)
    static_location_list=[]
    for location in locations_list:
        local_a=location.timestamp-timedelta(minutes=5).total_seconds()*1e+3
        local_b=location.timestamp+timedelta(minutes=5).total_seconds()*1e+3
        activities=PluginGoogleActivityRecognition.objects.filter(device_id=user_id,timestamp__gte=local_a,timestamp__lte=local_b,activity_type__lte=2)
        if not activities.exists():
            static_location_list.append(location)
    return static_location_list
    
def __doClusters(user_id, location_data):
    clusters_centers = kmeans.FindKAndClusterKMeans(location_data)
    Clusters.objects.filter(device_id=user_id).delete()
    current_time=time.time()
    name=1;
    for cluster in clusters_centers:
        p = Clusters(double_latitude=str(cluster[0]), double_longitude=str(cluster[1]), device_id=user_id, ts=current_time,name=str(name))
        name+=1
        p.save()
        

    
    