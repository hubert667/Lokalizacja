from django.shortcuts import render
from polls.models import *
from django.http import HttpResponse
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

def drawCenters(request):
    ClusterData()
    latest_poll_list = Clusters.objects.all()
    context = {'locations': latest_poll_list}
    return render(request, 'polls/wizualizacja.html', context)
