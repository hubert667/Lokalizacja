from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
     # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/map/
    
    url(r'^form/$', views.detailsForm, name='detailsForm'),
    
    """
    url(r'^(?P<poll_id>\d+)/map/$', views.draw, name='map'),
     # ex: /polls/5/map/
    url(r'^(?P<user_id>\d+)/centers/$', views.drawCenters, name='mapCenter'),
    # ex: /polls/5/map/
    url(r'^users/$', views.userChoice, name='userChoice'),
    
    url(r'^drawUser/$', views.drawUser, name='drawUser'),
    """
    
)
