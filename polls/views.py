from polls.models import *
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from clustering import *
from InfoDetailsForm import *
import calendar
import datetime

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

def printActivities(request,user_id,time_start,time_end):
    activity_list = PluginGoogleActivityRecognition.objects.filter(device_id=user_id,timestamp__gte=time_start,timestamp__lte=time_end)
    activity_times=[]
    for activity in activity_list:
        new_activity=activity
        new_activity.timestamp= datetime.datetime.fromtimestamp(activity.timestamp / 1e3)
        activity_times.append(new_activity)
    context = {'locations': activity_times}
    return render(request, 'polls/activityPrint.html', context)


def draw(request,poll_id):
    latest_poll_list = Lokalizacja.objects.all()[:poll_id]
    context = {'locations': latest_poll_list}
    return render(request, 'polls/wizualizacja.html', context)

def drawAware(request,user_id):
    latest_poll_list = Locations.objects.filter(device_id=user_id)
    context = {'locations': latest_poll_list}
    return render(request, 'polls/locationsMap.html', context)

def drawCenters(request,user_id):
    ClusterData(user_id)
    latest_poll_list = Clusters.objects.filter(user=user_id)
    context = {'locations': latest_poll_list}
    return render(request, 'polls/clustersDraw.html', context)

def drawCentersAware(request,user_id):
    ClusterDataAware(user_id)
    latest_poll_list = Clusters.objects.filter(user=user_id)
    context = {'locations': latest_poll_list}
    return render(request, 'polls/clustersDraw.html', context)

def userChoice(request):
    users=[6,7]
    context = {'users': users}
    return render(request, 'polls/userChoice.html', context)

def drawUser(request):
    selected_choice = request.POST['choice']
    selected_choice=int(selected_choice)
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return drawCenters(request,selected_choice)
    #return HttpResponseRedirect(reverse('polls:users'))
    
def detailsForm(request):
   
    #generateUsers()   
    userList=Users.objects.all()
    if request.method == 'POST': # If the form has been submitted...
        # ContactForm was defined in the the previous section
        form = InfoDetailsForm(request.POST) # A form bound to the POST data
        form.fields['ChooseUser'].queryset=userList
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            selected_choice = form.cleaned_data['ChooseUser']
            user_id=selected_choice.device_id
            cluster=form.cleaned_data['ShowClusters']
            activities=form.cleaned_data['ShowActivities']
            dateStart=1000*calendar.timegm(form.cleaned_data['start_time'].utctimetuple())
            dateEnd=1000*calendar.timegm(form.cleaned_data['end_time'].utctimetuple())
            if activities:
                return printActivities(request,user_id,dateStart,dateEnd)
            else:
                if cluster:
                    return drawCentersAware(request,user_id)
                else:
                    return drawAware(request,user_id)
           
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
