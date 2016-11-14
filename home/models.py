from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Church(models.Model):
    def __unicode__(self):
        return 'Church: ' + self.name
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    number = models.CharField(max_length=20, null=True)
    address1 = models.CharField(max_length=50, null=True)
    address2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zip = models.CharField(max_length=6, null=True)

class Volunteer(models.Model):
    def __unicode__(self):
        return 'Volunteer: ' + self.user.name
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True)
    approved = models.BooleanField(default=False)
    level = models.PositiveSmallIntegerField(null=True)

class Min_Group(models.Model):
    def __unicode__(self):
        return 'Group: ' + self.name
    name = models.CharField(max_length=50, null=True)

class Min_Category(models.Model):
    def __unicode__(self):
        return 'Category: ' + self.name
    group = models.ForeignKey(Min_Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)

class Help(models.Model):
    category = models.ForeignKey(Min_Category, on_delete=models.CASCADE)
    church = models.ForeignKey(Church, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, blank=True, null=True)
    start =  models.TimeField(null=True)
    end = models.TimeField(null=True)
    day = models.PositiveSmallIntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)

