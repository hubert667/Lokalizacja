# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

#Obosolete: only foor SDCF 
class Lokalizacja(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True) # Field name made lowercase.
    x = models.CharField(max_length=20, blank=True)
    y = models.CharField(max_length=20, blank=True)
    accuracy = models.CharField(max_length=20, blank=True)
    user = models.IntegerField()
    metoda = models.CharField(max_length=20, blank=True)
    ts = models.CharField(max_length=20)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.x
    class Meta:
        db_table = 'lokalizacja'
        
class Clusters(models.Model):
    x = models.CharField(max_length=20, blank=True)
    y = models.CharField(max_length=20, blank=True)
    name=models.CharField(max_length=255, blank=True)
    user = models.CharField(max_length=255, blank=True)
    ts = models.CharField(max_length=20)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.x
    class Meta:
        db_table = 'clusters'
        
class Users(models.Model):
    device_id = models.CharField(max_length=255, blank=True)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.device_id
    class Meta:
        db_table = 'Users'
       

class Locations(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True) # Field renamed because it started with '_'.
    timestamp = models.FloatField(blank=True, null=True)
    device_id = models.CharField(max_length=255, blank=True)
    double_latitude = models.FloatField(blank=True, null=True)
    double_longitude = models.FloatField(blank=True, null=True)
    double_bearing = models.FloatField(blank=True, null=True)
    double_speed = models.FloatField(blank=True, null=True)
    double_altitude = models.FloatField(blank=True, null=True)
    provider = models.TextField(blank=True)
    accuracy = models.FloatField(blank=True, null=True)
    label = models.TextField(blank=True)
    class Meta:
        db_table = 'locations'


class PluginGoogleActivityRecognition(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True) # Field renamed because it started with '_'.
    timestamp = models.FloatField(blank=True, null=True)
    device_id = models.CharField(max_length=255, blank=True)
    activity_name = models.TextField(blank=True)
    activity_type = models.IntegerField(blank=True, null=True)
    confidence = models.IntegerField(blank=True, null=True)
    activities = models.TextField(blank=True)
    class Meta:
        db_table = 'plugin_google_activity_recognition'
