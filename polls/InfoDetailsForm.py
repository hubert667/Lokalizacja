from django import forms
from polls.models import *
from django.forms.extras.widgets import SelectDateWidget
from datetime import date, timedelta

class InfoDetailsForm(forms.Form):

    ChooseUser=forms.ModelChoiceField(queryset=[],label='Choose user')
    CHOICES=[('locations','Show location on map'),('locationStatic','Show only static locations on map'),('clusters','show clusters on map'),
         ('activity','show activity list'),('locationList','show location list')]
    ChooseTask= forms.ChoiceField(choices=CHOICES, initial='locations', widget=forms.RadioSelect())
    #ShowClustersOnMap = forms.BooleanField(required=False)
    #ShowActivitiesList=forms.BooleanField(required=False)
    #ShowLocationsList=forms.BooleanField(required=False)
    start_time=forms.DateTimeField(initial=date.today()-timedelta(days=7))
    end_time=forms.DateTimeField(initial=date.today)
   
    def __init__(self, *args, **kwargs):
        super(InfoDetailsForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].widget = SelectDateWidget()
        self.fields['end_time'].widget = SelectDateWidget()
        """
        queryset = kwargs.pop('queryset', None)
        if queryset:
        self.fields['ChooseUser'].queryset = queryset
       """
            
