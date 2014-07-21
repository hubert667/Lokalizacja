from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
    
    # ex: /polls/form
    url(r'^form/', views.detailsForm, name='detailsForm'),
    
    url(r'^$', views.index, name='index'),
    

    
)
