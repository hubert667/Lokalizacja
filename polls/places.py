from polls.models import *
from Scripts import kmeans
import time
import datetime
import collections
from datetime import timedelta
from math import cos, sin, asin, sqrt, radians
import operator
import constans

#only for data from SDCF
class placesMap:
    
    user_id=0;
    time_period=0;
    places_map={}
    present_sample=collections.Counter()
    max_distance=100
    period=15
    
    def __init__(self,user_id):
        """
        period- period in minutes
        """
        self.user_id=user_id
        self.time_period=self.period*60*1e+3
    
    def doMapping(self,time_start,time_end):
        
        if time_start!=None and time_end!=None:
            locations_list = Locations.objects.filter(device_id=self.user_id,timestamp__gte=time_start,timestamp__lte=time_end)
        else:
            locations_list = Locations.objects.filter(device_id=self.user_id)

        self.__mapToSamples(locations_list)
        self.__saveToDatabase()
        
    def __mapToSamples(self,location_data):
        """
        maps samples to places
        """
        
        places=Clusters.objects.filter(device_id=self.user_id)
        places_counts={}
        for place in places:
            places_counts[place]=collections.Counter()
            
        for loc in location_data:
            closest_place=self.__find_closest(loc,places)
            time=int(loc.timestamp/self.time_period)
            self.present_sample[time]+=1
            if closest_place is not None:
                places_counts[closest_place][time]+=1
        for time in self.present_sample:
            max_val=0
            chosen_place=None
            for place in places:
                res=places_counts[place][time]
                if res>max_val:
                    max_val=res
                    chosen_place=place
            self.places_map[time]=chosen_place  
                    
        
        
    def __find_closest(self,location,places):
        """
        returns None if no place is the distance of max_distance
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
        
            
    def __saveToDatabase(self):
 
        Places.objects.filter(device_id=self.user_id).delete()
        #locations_list = Locations.objects.filter(device_id=user_id,timestamp__gte=time_start,timestamp__lte=time_end)
        for timestamp in self.places_map:
            new_timestamp=timestamp*self.time_period
            place=Places(timestamp=new_timestamp,device_id=self.user_id,place=self.places_map[timestamp])
            place.save()

    def GetUserPlaces(self,time_start,time_end,predictor=None):
        
        if time_start!=None and time_end!=None:
            places=Places.objects.filter(device_id=self.user_id,timestamp__gte=time_start,timestamp__lte=time_end).order_by('timestamp')
        else:
            places=Places.objects.filter(device_id=self.user_id).order_by('timestamp')
        
        predictedLocation=None
        #locations_list = Locations.objects.filter(device_id=user_id,timestamp__gte=time_start,timestamp__lte=time_end)
        places_local=[]
        time_change = constans.time_change
        previously_predicted=""
        previous_place=""
        total_number=0.0
        correct_predict=0.0
        for locationEvent in places:
            new_timestamp=locationEvent.timestamp
            place=locationEvent.place
            if place!=None:
                if predictor!=None:
                    predictedLocation=predictor.predictLocation(self.user_id,place,new_timestamp)
                new_time= datetime.datetime.fromtimestamp(new_timestamp / 1e3)+time_change
                if (place.name!=previous_place and previous_place!="" ) or False:
                    if place.name!=previously_predicted:
                        places_local.append([new_time,place,previously_predicted,"       BAD"])
                        total_number+=1.0
                    else:
                        places_local.append([new_time,place,previously_predicted,"       GOOD"])
                        correct_predict+=1.0
                        total_number+=1.0
                previously_predicted=predictedLocation
                previous_place=place.name
        return [places_local,correct_predict/total_number]
        
        
        
        
        
        
        
