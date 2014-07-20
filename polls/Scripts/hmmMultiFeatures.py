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
from polls.Scripts.hmm import hmmModel
import polls.constans

class hmmMultiFeaturesModel(hmmModel):
    
    day_parts=3
    tuple_cache=[]
    
    def __init__(self, places,num_of_plac):
        self.num_of_places=num_of_plac
        self.training_data=self.__prepareTrainingData(places,num_of_plac)
        #print np.shape(self.training_data)
    
    def train(self):
        
        self.__trainHMM(self.training_data)
        
    def predict(self,place,timestamp):
        
        current_state=self.__prepare_place(place,timestamp,False)
        if current_state==None:
            return None
        index=np.argmax(self.transition_matrix[current_state,:])
        
        result=self.__get_place(index)
        return result
        
    def __prepareTrainingData(self,places,num_of_places):
        
        allplaces = []
        for location_event in places:
            if location_event.place!=None:
                index=self.__prepare_place(location_event.place,location_event.timestamp)
                allplaces.append(index)
                self.__add_to_cache(index)
        return np.array(allplaces)
        
    def __add_to_cache(self,current_tuple):
        
        if current_tuple not in self.tuple_cache:
            self.tuple_cache.append(current_tuple)
        
    def __prepare_place(self,place,current_timestamp,generate_new=True):
        
        if place==None:
            return None
        new_place=place.name
        new_time= datetime.datetime.fromtimestamp(current_timestamp / 1e3)+polls.constans.time_change
        current_day_part=int((max(0,(new_time.hour-6))*self.day_parts)/18)
        tuple_data=(new_place,current_day_part)
        
        if tuple_data in self.places_indexes:
            return self.places_indexes[tuple_data]
        if generate_new==False:
            for day_part_artificial in range(self.day_parts):
                tuple_data=(new_place,day_part_artificial)
                if tuple_data in self.places_indexes:
                    return self.places_indexes[tuple_data]
            return None
        else:
            self.places_indexes[tuple_data]=self.global_place_index
            print self.global_place_index
            self.global_place_index+=1
            return self.places_indexes[tuple_data]
        
    def __get_place(self,index):
        
        result=None
        for key in self.places_indexes:
            if self.places_indexes[key]==index:
                result= key[0]
        return result
           
    def __prepareTransitions(self):
        """
        Removes probabilities of the transition to the same state
        """
        self.transition_matrix=self.markovModel._get_transmat()[:]
        #print "przed"+str(self.transition_matrix)
        for i in range(len(self.transition_matrix)):
            for index in range(len(self.transition_matrix)):
                place1=self.__get_place(i)
                place2=self.__get_place(index)
                if place1==place2:
                    self.transition_matrix[i,index]=0
        
    def __trainHMM(self,train_data):
    
        #self.markovModel =hmm.GaussianHMM(len(self.tuple_cache),'full')
        local_num_of_places=len(self.tuple_cache)
        emissionMatrix=np.identity(local_num_of_places)
        self.markovModel =hmm.MultinomialHMM(local_num_of_places,params="stmc",init_params="stmc")
        self.markovModel._set_emissionprob(emissionMatrix)
        
        self.markovModel.fit([train_data])
        self.markovModel.predict(train_data)
        self.__prepareTransitions()
        print self.markovModel.score(train_data)
        print self.transition_matrix
        print self.places_indexes

        
        
        
        
        
        