from Scripts import hmm
from polls.models import Places,Clusters

class hmmFramework():
    
    preditcors={}
    currently_in_progress={}
    error="Previous training not ended"
    errorStat="Training not ended or wrong user id"
    
    def __init__(self):
        None
        
        
    def train(self,user_id,time_start,time_end):
        if (user_id in self.preditcors) and self.currently_in_progress[user_id]==True:
            return self.error
        
        self.currently_in_progress[user_id]=True
        try:
            places=Places.objects.filter(device_id=user_id,timestamp__gte=time_start,timestamp__lte=time_end).order_by('timestamp')      
            clusters=Clusters.objects.filter(device_id=user_id)
            num_of_places=len(clusters)
            print len(clusters)
            self.preditcors[user_id]=hmm.hmmModel(places,num_of_places);
            self.preditcors[user_id].train()
        finally:
            self.currently_in_progress[user_id]=False
            
        return "Successfully trained!"
            
    def predictLocation(self,user_id,place,timestamp):

        if (user_id in self.preditcors)==False or  (user_id in self.currently_in_progress and self.currently_in_progress[user_id]==True):
            return self.errorStat
         
        next_location=self.preditcors[user_id].predict(place,timestamp)
         
        return next_location
        
    