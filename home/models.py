from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import MySQLdb

# Create your models here.

APPROVAL_CHOICES = (
    (0, 'Unapproved'),
    (1, 'Approved')
)

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
    x_lat = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, editable=False)
    y_long = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, editable=False)
    church_area1 = models.CharField(max_length=50, null=True, blank=True)
    church_area2 = models.CharField(max_length=50, null=True, blank=True)
    approval = models.PositiveSmallIntegerField(default=0, choices=APPROVAL_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        super(Church, self).save(*args, **kwargs)
        db = MySQLdb.connect("cso.cb9o8fk82u6u.us-east-1.rds.amazonaws.com", "admin", "noz8VER8!!!", "CSO")
        cursor = db.cursor()
        sql = "SELECT * FROM zipcode WHERE zip=" + self.zipcode
        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            self.x_lat = results[4]
            self.y_long = results[5]
        except:
            print "Error: unable to fetch data"
        super(Church, self).save(*args, **kwargs)

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
    approval = models.PositiveSmallIntegerField(default=0, choices=APPROVAL_CHOICES)
    level = models.PositiveSmallIntegerField(null=True, default=5)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)

class Min_Group(models.Model):
    def __unicode__(self):
        return 'Group: ' + self.name
    name = models.CharField(max_length=50, null=True)

class Min_Category(models.Model):
    def __unicode__(self):
        return 'Category: ' + self.name
    group = models.ForeignKey(Min_Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)

class Interest(models.Model):
    def __unicode__(self):
        return 'Volunteer: ' + self.volunteer.name + ' Category: ' + self.category.name
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    category = models.ForeignKey(Min_Category, on_delete=models.CASCADE)

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

class Help_Request(models.Model):
    def __unicode__(self):
        return self.help.church.name + ": " + self.help.category.group.name + " " + self.help.category.name
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    help = models.ForeignKey(Help, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)