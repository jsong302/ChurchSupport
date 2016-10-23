from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# class Church(models.Model):
#     user_id = models.ForeignKey(Auth.User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)
#     start = models.TimeField()
#     end = models.TimeField()
#     day = models.PositiveSmallIntegerField()
#     address1 = models.CharField(max_length=50)
#     address2 = models.CharField(max_length=50)
#     city = models.CharField(max_length=50)
#     state = models.CharField(max_length=50)
#     zip = models.CharField(max_length=50)
#     date_created = models.DateTimeField(auto_now_add=True )
#     last_modified = models.DateTimeField(auto_now=True)
#
# class Volunteer(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     first_name = models.TextField(max_length=50)
#     last_name = models.TextField(max_length=50)
#     date_created = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)

class requestDenomination(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=50)


#class Request(models.Model):