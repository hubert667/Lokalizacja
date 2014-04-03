from polls.models import *
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from clustering import *

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

def wypisz(request,poll_id):
    latest_poll_list = Lokalizacja.objects.all()[:poll_id]
    context = {'locations': latest_poll_list}
    return render(request, 'polls/wypisz.html', context)


def draw(request,poll_id):
    latest_poll_list = Lokalizacja.objects.all()[:poll_id]
    context = {'locations': latest_poll_list}
    return render(request, 'polls/wizualizacja.html', context)

def drawCenters(request,user_id):
    ClusterData(user_id)
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
