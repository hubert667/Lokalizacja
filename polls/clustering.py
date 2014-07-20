from polls.models import *
from Scripts import kmeans
import time
import datetime
from datetime import timedelta
import operator
import places
import constans

#only for data from SDCF
def ClusterData(user_id):
    
    locations_list = Lokalizacja.objects.filter(user=user_id)
    location_data=[]
    for loc in locations_list:
        location_data.append([float(loc.x),float(loc.y)])
    __doClusters(user_id, location_data)
    
        

def ClusterDataAware(user_id,time_start,time_end):
    """
    Clusters data after it finds optimal K
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
    __mergeCloseOnes(user_id)
    places_mapping=places.placesMap(user_id)
    places_mapping.doMapping(time_start, time_end)
    __removeVisitedOnce(user_id)
    places_mapping=places.placesMap(user_id)
    #places_mapping.doMapping(None, None)
    places_mapping.doMapping(time_start, time_end)
    
def GetStaticLocations(user_id, time_start, time_end):
    locations_list = Locations.objects.filter(device_id=user_id, timestamp__gte=time_start, timestamp__lte=time_end,accuracy__lte=constans.min_accuracy)
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
        
def  __removeVisitedOnce(user_id):
    
    places=Places.objects.filter(device_id=user_id).order_by('timestamp')
    new_places=[]
    visited_once=[]  
    previous_place=None 
    for locationEvent in places:
        place=locationEvent.place
        if place!=None:
            if previous_place!=place.name: #trip
                if place in visited_once and place not in new_places:
                    new_places.append(place)
                    print "append2  "+place.name
                elif place not in visited_once:
                    visited_once.append(place)
                    print "append1  "+place.name
            previous_place=place.name
    clusters=Clusters.objects.filter(device_id=user_id)
    for cluster in clusters:
        if cluster not in new_places:
            print "removed"+ cluster.name
            cluster.delete()
    print len(new_places)

def __average(num1,num2):
    return (float(num1)+float(num2))/2.0

def  __mergeCloseOnes(user_id):
    
    places_mapping=places.placesMap(user_id)
    clusters=Clusters.objects.filter(device_id=user_id)
    while(__merge_Once(clusters,places_mapping)):
        clusters=Clusters.objects.filter(device_id=user_id)
    return

        
def __merge_Once(clusters,places_mapping):
    
    
    for cluster1 in clusters:
        for cluster2 in clusters:
            if cluster1!=cluster2:
                distance=places_mapping.calc_distance(cluster1.double_latitude, cluster1.double_longitude, cluster2.double_latitude, cluster2.double_longitude)
                if distance<=constans.distance_threshold_merge:
                    new_cluster= Clusters(double_latitude=str(__average(cluster1.double_latitude,cluster2.double_latitude)), double_longitude=str(__average(cluster1.double_longitude,cluster2.double_longitude)), device_id=cluster1.device_id, ts=cluster1.ts,name=str(cluster1.name))
                    print "merged "+str(new_cluster)
                    cluster1.delete()
                    cluster2.delete()
                    new_cluster.save()
                    return True
    return False
    
    