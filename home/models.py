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
    zipcode = models.CharField(max_length=6, null=True)
    x_lat = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    y_long = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    church_area1 = models.CharField(max_length=50, null=True, blank=True)
    church_area2 = models.CharField(max_length=50, null=True, blank=True)
    approval = models.PositiveSmallIntegerField(default=0)

class Volunteer(models.Model):
    def __unicode__(self):
        return 'Volunteer: ' + self.user.first_name
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True)
    address1 = models.CharField(max_length=50, null=True)
    address2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=6, null=True)
    church_name = models.CharField(max_length=50, null=True)
    church_contact = models.CharField(max_length=50, null=True)
    church_phone = models.CharField(max_length=20, null=True)
    approval = models.PositiveSmallIntegerField(default=0)
    level = models.PositiveSmallIntegerField(null=True, default=5)

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
    def __unicode__(self):
        return 'Church: ' + self.church.name + ' Category: ' + self.category.name
    category = models.ForeignKey(Min_Category, on_delete=models.CASCADE)
    church = models.ForeignKey(Church, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, blank=True, null=True)
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)
    students = models.PositiveIntegerField(null=True)
    day = models.PositiveSmallIntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)


