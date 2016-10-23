from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Church(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    number = models.CharField(max_length=20, null=True)
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)
    day = models.PositiveSmallIntegerField()
    address1 = models.CharField(max_length=50, null=True)
    address2 = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zip = models.CharField(max_length=50, null=True)
    peopleNeeded = models.PositiveSmallIntegerField(default=0)
    helped = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=20, null=True)
    approved = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)


class Denomination(models.Model):
    name = models.TextField(max_length=50, null=True)

class Ministry(models.Model):
    name = models.TextField(max_length=50, null=True)