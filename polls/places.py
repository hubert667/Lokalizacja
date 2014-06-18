from polls.models import *
from Scripts import kmeans
import time
import datetime
import collections
from datetime import timedelta
from math import cos, sin, asin, sqrt, radians

#only for data from SDCF
class placesMap:
    
    user_id=0;
    time_period=0;
    places_map={}
    present_sample=collections.Counter()
    max_distance=50
    
    def __init__(self,user_id,period):
        """
        period- period in minutes
        """
        self.user_id=user_id
        self.time_period=period*60*1000
    
    def doMapping(self):
    
        locations_list = Locations.objects.filter(device_id=self.user_id)
#         location_data=[]
#         for loc in locations_list:
#             location_data.append([float(loc.x),float(loc.y),loc.ts])
        self.mapToSamples(locations_list)
        
    def mapToSamples(self,location_data):
        """
        maps samples to places
        """
        
        places=Clusters.objects.filter(user=self.user_id)
        places_counts={}
        for place in places:
            places_counts[place]=collections.Counter()
            
        for loc in location_data:
            closest_place=self.find_closest(loc,places)
            time=loc.timestamp/self.time_period
            self.present_sample[time]+=1
            if closest_place is not None:
                places_counts[closest_place][time]+=1
        for time in self.present_sample:
            max=0
            chosen_place=None
            for place in places:
                res=places_counts[place][time]
                if res>max:
                    max=res
                    chosen_place=place
            self.places_map[time]=chosen_place  
                    
        
        
    def find_closest(self,location,places):
        """
        returns null if no place is the distance of max_distance
        """
        
        closest=None
        min=1e+10
        for place in places:
            distance=self.calc_distance(location.double_latitude,location.double_longitude, place.double_latitude,place.double_longitude)
            if distance<min:
                min=distance
                if distance<self.max_distance:
                    closest=place
        return closest
        
        
        

    def calc_distance(self,lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees). Returns in meters
        
        This method is copied from http://gis.stackexchange.com/
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6371 * c
        return km*1000
        
            
        
        
        
        
        
        
        
        
