from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer

from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal
import datetime
from datetime import timedelta
import calendar
import random
import numpy as np
from sklearn import hmm

class hmmModel():
    
    markovModel=None
    iterations=50
    training_data=[]
    time_change = timedelta(hours=2)
    num_of_places=0
    places_indexes={}
    global_place_index=0
    last_visit_map={}
    transition_matrix=[]
    
    def __init__(self, places,num_of_plac):
        self.num_of_places=num_of_plac
        self.training_data=self.__prepareTrainingData(places,num_of_plac)
        print self.training_data
        
    def train(self):
        
        self.__trainHMM(self.training_data)
        
    def predict(self,place,timestamp):
        
        new_place=self.__prepare_place(place)
        
        index=np.argmax(self.transition_matrix[new_place,:])
        
        result=None
        for key in self.places_indexes:
            if self.places_indexes[key]==index:
                result=key
        return result
        
    def __prepareTrainingData(self,places,num_of_places):
        
        allplaces = []
        for location_event in places:
            if location_event.place!=None:
                new_place=self.__prepare_place(location_event.place)
                allplaces.append(new_place)
#                 current_timestamp=location_event.timestamp
#                 new_feature_vector=self.__prepare_features(location_event.place,current_timestamp)
#                 new_place=self.__prepare_place(location_event.place)
#                 if previous_feature_vector!=None and previous_place!=None and location_event.place.name!=previous_place.name:
#                     counter+=1
#                     print previous_feature_vector
#                     print location_event.place.name
#                     for i in range(1):
#                         allplaces.append(new_place)
#                 previous_feature_vector=new_feature_vector
#                 previous_place=location_event.place
#                 self.last_visit_map[location_event.place]=current_timestamp
                
#         previous_feature_vector=None
#         previous_place=None
#         probiability_of_static=float(counter)/float(len(places))
#         probiability_of_static=1
#         for location_event in places:
#             if location_event.place!=None:
#                 current_timestamp=location_event.timestamp
#                 new_feature_vector=self.__prepare_features(location_event.place,current_timestamp)
#                 new_place=self.__prepare_place(location_event.place)
#                 rand=random.random()
#                 if previous_feature_vector!=None and rand<=probiability_of_static:
#                     counter+=1
#                     print new_feature_vector
#                     print location_event.place.name
#                     for i in range(1):
#                         allplaces.append(new_place)
#                 previous_feature_vector=new_feature_vector
#                 previous_place=new_place
#                 self.last_visit_map[location_event.place]=current_timestamp
        return allplaces
        

        
    def __prepare_place(self,place):
        
        if place!=None:
            if place.name in self.places_indexes:
                return self.places_indexes[place.name]
            
            self.places_indexes[place.name]=self.global_place_index
            self.global_place_index+=1
            return self.places_indexes[place.name]
        else:
            return None
            
#         means = [(-10,-10),(2,4),(30,10)]
#         cov = [diag([1,1]), diag([0.5,1.2]), diag([1.5,0.7])]
#         alldata = ClassificationDataSet(2, 1, nb_classes=3)
#         for n in xrange(400):
#             for klass in range(3):
#                 input = multivariate_normal(means[klass],cov[klass])
#                 alldata.addSample(input, [klass])
         
           
    def __prepareTransitions(self):
        """
        Removes probabilities of the transition to the same state
        """
        self.transition_matrix=self.markovModel._get_transmat()[:];
        for i in range(len(self.transition_matrix)):
            index=np.argmax(self.transition_matrix[i,:])
            if index==i:
                self.transition_matrix[i,index]=0

        
    
    def __trainHMM(self,train_data):
        
        emissionMatrix=np.identity(self.num_of_places)
        print self.num_of_places
        self.markovModel =hmm.MultinomialHMM(self.num_of_places,params="stmc",init_params="stmc")
        self.markovModel._set_emissionprob(emissionMatrix)
        
        self.markovModel.fit([train_data])
        self.markovModel.predict(train_data)
        self.__prepareTransitions()
        print self.markovModel.score(train_data)
        print self.markovModel.transmat_
        print self.places_indexes
        print self.markovModel.sample(100)
        print self.markovModel._get_emissionprob()
        
        
        
        
        