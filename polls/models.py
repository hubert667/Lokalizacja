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
    user = models.IntegerField()
    ts = models.CharField(max_length=20)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.x
    class Meta:
        db_table = 'clusters'
