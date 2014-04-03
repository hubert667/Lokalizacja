from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
     # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<poll_id>\d+)/$', views.wypisz, name='detail'),
    # ex: /polls/5/map/
    url(r'^(?P<poll_id>\d+)/map/$', views.draw, name='map'),
     # ex: /polls/5/map/
    url(r'centers/$', views.drawCenters, name='mapCenter'),
)
