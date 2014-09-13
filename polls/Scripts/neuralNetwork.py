from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.structure.modules   import SigmoidLayer

from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal
import datetime
from datetime import timedelta
import calendar
import random

class neuralNetwork():
    
    fnn=None
    iterations=50
    training_data=[]
    trndata=[]
    tstdata=[]
    time_change = timedelta(hours=2)
    num_of_places=0
    places_indexes={}
    global_place_index=0
    last_visit_map={}
    
    def __init__(self, places,num_of_plac):
        self.num_of_places=num_of_plac
        self.training_data=self.__prepareTrainingData(places,num_of_plac)
        self.tstdata, self.trndata = self.training_data.splitWithProportion( 0.2 )
        self.trndata._convertToOneOfMany( )
        self.tstdata._convertToOneOfMany( )
        
    def train(self):
        
        self.__trainNetwork(self.trndata, self.tstdata)
        
    def predict(self,place,timestamp):
        sample=self.__prepare_features(place,timestamp)
        griddata = ClassificationDataSet(2,1, nb_classes=self.num_of_places)
        griddata.addSample(sample, [0])
        griddata._convertToOneOfMany()  
        out = self.fnn.activateOnDataset(griddata)
        index=out.argmax(axis=1)
        result=None
        for key in self.places_indexes:
            if self.places_indexes[key]==index:
                result=key
        return result
        
    def __prepareTrainingData(self,places,num_of_places):
        
        alldata = ClassificationDataSet(2, 1, nb_classes=self.num_of_places)
        previous_feature_vector=None
        previous_place=None
        counter=0
               
        for location_event in places:
            if location_event.place!=None:
                current_timestamp=location_event.timestamp
                new_feature_vector=self.__prepare_features(location_event.place,current_timestamp)
                new_place=self.__prepare_place(location_event.place)
                #if previous_feature_vector!=None and previous_place!=None and location_event.place.name!=previous_place.name:
                if previous_feature_vector!=None:
                    counter+=1
                    
                    if location_event.place.name=="2":
                        print previous_feature_vector
                        print location_event.place.name
                        for i in range(1):
                            alldata.appendLinked(previous_feature_vector,[new_place])

                previous_feature_vector=new_feature_vector
                previous_place=location_event.place
                self.last_visit_map[location_event.place]=current_timestamp
                
        previous_feature_vector=None
        previous_place=None
        probiability_of_static=float(counter)/float(len(places))
        probiability_of_static=0.5
        for location_event in places:
            if location_event.place!=None:
                current_timestamp=location_event.timestamp
                new_feature_vector=self.__prepare_features(location_event.place,current_timestamp)
                new_place=self.__prepare_place(location_event.place)
                rand=random.random()
                if previous_feature_vector!=None and rand<=probiability_of_static:
                    counter+=1
                    
                    if location_event.place.name=="1":
                        print new_feature_vector
                        print location_event.place.name
                        for i in range(1):
                            alldata.appendLinked(previous_feature_vector,[new_place])
                previous_feature_vector=new_feature_vector
                previous_place=new_place
                self.last_visit_map[location_event.place]=current_timestamp
        return alldata
        
    def __prepare_features(self,place,timestamp):
        
        time_event=datetime.datetime.fromtimestamp(timestamp / 1e3)+self.time_change
        weekday=float(time_event.weekday())/7.0
        hour=float(time_event.hour)/24.0
        last_delta=0
        if place in self.last_visit_map:
            last_time=datetime.datetime.fromtimestamp(self.last_visit_map[place] / 1e3)+self.time_change
            last_delta=float(min(168,(time_event-last_time).seconds/3600))/168.0 # number of hours during one week
        place_num=float(self.__prepare_place(place))/float(self.num_of_places-1)
        
        return [hour,weekday]
        
    def __prepare_place(self,tuple_data):
        
        if tuple_data!=None:
            if tuple_data.name in self.places_indexes:
                return self.places_indexes[tuple_data.name]
            
            self.places_indexes[tuple_data.name]=self.global_place_index
            self.global_place_index+=1
            return self.places_indexes[tuple_data.name]
        else:
            return None
            
    
    def __trainNetwork(self,trndata,tstdata):
        
        self.fnn = buildNetwork( trndata.indim, 2, trndata.outdim, outclass=SigmoidLayer )
        trainer = BackpropTrainer( self.fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01,learningrate=0.01)
        
        for i in range(self.iterations):
            trainer.trainEpochs( 1 )
            trnresult = percentError( trainer.testOnClassData(),trndata['class'] )
            tstresult = percentError( trainer.testOnClassData(dataset=tstdata ), tstdata['class'] )
            print "epoch: %4d" % trainer.totalepochs, "  train error: %5.2f%%" % trnresult,"  test error: %5.2f%%" % tstresult
        