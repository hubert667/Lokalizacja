from polls.models import *
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import clustering
import places
from InfoDetailsForm import *
import calendar
import datetime
from datetime import timedelta
import operator
import PredictingPlaces

def index(request):
    return HttpResponse("Wrong address")

predictor=PredictingPlaces.PredictingFramework()

def printActivities(request,user_id,time_start,time_end):
    activity_list = PluginGoogleActivityRecognition.objects.filter(device_id=user_id,timestamp__gte=time_start,timestamp__lte=time_end)
    activity_times=[]
    time_change = timedelta(hours=2)
    for activity in activity_list:
        new_activity=activity
        new_activity.timestamp= datetime.datetime.fromtimestamp(activity.timestamp / 1e3)+time_change
        activity_times.append(new_activity)
    context = {'locations': activity_times}
    return render(request, 'polls/activityPrint.html', context)


def printLocations(request,user_id,time_start,time_end):
    
    placesToUser(user_id,time_start,time_end)
    
    places_base=places.placesMap(user_id)
    [places_list,success_rate]=places_base.GetUserPlaces(time_start, time_end,predictor)
    print "predicted correctly in "+str(100*success_rate)+"% cases"
    context = {'placesMap': places_list}
    return render(request, 'polls/placesPrint.html', context)

def trainPredictor(request,user_id,time_start,time_end):
    
    placesToUser(user_id,time_start,time_end)
    #placesToUser(user_id,None,None)
    
    predictor.train(user_id,time_start, time_end)
    places_base=places.placesMap(user_id)
    
    [places_list,success_rate]=places_base.GetUserPlaces(time_start, time_end,predictor)
    print "predicted correctly in "+str(100*success_rate)+"% cases"
    context = {'placesMap': places_list}
    return render(request, 'polls/placesPrint.html', context)

def drawAware(request,user_id,time_start,time_end,static=False):
    if static:
        latest_poll_list=clustering.GetStaticLocations(user_id, time_start, time_end)
    else:
        latest_poll_list = Locations.objects.filter(device_id=user_id,timestamp__gte=time_start,timestamp__lte=time_end)
    context = {'locations': latest_poll_list}
    return render(request, 'polls/locationsMap.html', context)



def drawCentersAware(request,user_id,time_start,time_end):
    clusterData(user_id,time_start,time_end)
    latest_poll_list = Clusters.objects.filter(device_id=user_id)
    context = {'locations': latest_poll_list}
    #print latest_poll_list
    return render(request, 'polls/clustersDraw.html', context)

def clusterData(user_id,time_start,time_end):
    #clustering.ClusterDataAware(user_id,time_start,time_end)
    clustering.SmartClusterData(user_id,time_start,time_end)
    
def placesToUser(user_id,time_start,time_end):
 
    places_base=places.placesMap(user_id)
    places_base.doMapping(time_start,time_end)   

    
def detailsForm(request):
   
    userList=Users.objects.all()
    if(len(userList)==0):
        generateUsers()   
    userList=Users.objects.all()
    if request.method == 'POST':
        form = InfoDetailsForm(request.POST) 
        form.fields['ChooseUser'].queryset=userList
        if form.is_valid(): 
            selected_choice = form.cleaned_data['ChooseUser']
            user_id=selected_choice.device_id
            choose=form.cleaned_data['ChooseTask']
            dateStart=1000*calendar.timegm(form.cleaned_data['start_time'].utctimetuple())
            dateEnd=1000*calendar.timegm(form.cleaned_data['end_time'].utctimetuple())+timedelta(days=1).total_seconds()*1000
            print choose
            if choose=="locations":
                return drawAware(request,user_id,dateStart,dateEnd)
            elif choose=="locationStatic":
                return drawAware(request,user_id,dateStart,dateEnd,static=True)
            elif choose=="trainPredictor":
                return trainPredictor(request,user_id,dateStart,dateEnd)
            elif choose=="clusters":
                return drawCentersAware(request,user_id,dateStart,dateEnd)
            elif choose=="activity":  
                return printActivities(request,user_id,dateStart,dateEnd)
            elif choose=="locationList":
                return printLocations(request,user_id,dateStart,dateEnd)
           
    else:
        form = InfoDetailsForm() # An unbound form
        form.fields['ChooseUser'].queryset=userList
    
    return render(request, 'polls/form.html', {
        'form': form,
    })
    
def generateUsers():
    userData=Locations.objects.values('device_id').distinct()
    for i in range(len(userData)):
        p,created = Users.objects.get_or_create(device_id=userData[i]["device_id"])
        p.save()
